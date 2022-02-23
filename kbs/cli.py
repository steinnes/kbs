import os
import sys

import click
import pykube

from .secret import Secret

kube_api = None


@click.group()
def cli():
    global kube_api
    config = pykube.KubeConfig.from_file("~/.kube/config")
    kube_api = pykube.HTTPClient(config)


@cli.command("list")
@click.argument("secret")
def list(secret):
    """list configuration in var=value (envfile) format"""
    global kube_api
    try:
        cfg = Secret.objects(kube_api).get_by_name(secret)
    except pykube.exceptions.ObjectDoesNotExist:
        click.echo(
            f"Could not find secret object named '{secret}' in the current kubectl context"
        )
        sys.exit(1)

    for key in sorted(cfg.keys()):
        click.echo("{}={}".format(key, cfg[key]))


@cli.command("get")
@click.argument("secret")
@click.argument("key")
def get(secret, key):
    """get a single config variable"""
    global kube_api
    try:
        cfg = Secret.objects(kube_api).get_by_name(secret)
    except pykube.exceptions.ObjectDoesNotExist:
        click.echo(
            f"Could not find secret object named '{secret}' in the current kubectl context"
        )
        sys.exit(1)

    if key not in cfg:
        click.echo("No var found for `{}.{}`".format(secret, key))
        return
    click.echo(cfg[key])


@cli.command("set")
@click.argument("secret")
@click.argument("key")
@click.argument("value")
def set(secret, key, value):
    """set a single config variable"""
    global kube_api
    try:
        cfg = Secret.objects(kube_api).get_by_name(secret)
    except pykube.exceptions.ObjectDoesNotExist:
        click.echo(
            f"Could not find secret object named '{secret}' in the current kubectl context"
        )
        sys.exit(1)

    cfg[key] = value
    cfg.update()


@cli.command("unset")
@click.argument("secret")
@click.argument("key")
def unset(secret, key):
    """remove a single config variable"""
    global kube_api
    try:
        cfg = Secret.objects(kube_api).get_by_name(secret)
    except pykube.exceptions.ObjectDoesNotExist:
        click.echo(
            f"Could not find secret object named '{secret}' in the current kubectl context"
        )
        sys.exit(1)

    if click.confirm(
        "Do you wish to delete config variable {}.{} with value of `{}`".format(
            secret, key, cfg[key]
        )
    ):
        del cfg[key]
        cfg.update()


@cli.command("envdir")
@click.argument("secret")
@click.argument("target_dir")
def envdir(secret, target_dir):
    global kube_api
    try:
        cfg = Secret.objects(kube_api).get_by_name(secret)
    except pykube.exceptions.ObjectDoesNotExist:
        click.echo(
            f"Could not find secret object named '{secret}' in the current kubectl context"
        )
        sys.exit(1)

    cfg = Secret.objects(kube_api).get_or_none(secret)
    target_dir = os.path.abspath(target_dir)
    if not click.confirm(
        "found {} vars, will write to `{}/*`".format(len(cfg), target_dir)
    ):
        click.echo("Exiting..")
        sys.exit(1)

    if not os.path.exists(target_dir):
        click.echo("{} did not exists, creating".format(target_dir))
        os.mkdir(target_dir)
    else:
        if os.path.exists(target_dir) and not os.path.isdir(target_dir):
            click.echo(
                "{} exists but isn't a directory, unable to continue".format(target_dir)
            )
            sys.exit(2)
    # config.write_envdir(cfg, target_dir)


@cli.command("load")
@click.argument("secret")
@click.argument("source")
def load(secret, source):
    source = os.path.abspath(source)
    global kube_api
    try:
        cfg = Secret.objects(kube_api).get_by_name(secret)  # noqa
    except pykube.exceptions.ObjectDoesNotExist:
        click.echo(
            f"Could not find secret object named '{secret}' in the current kubectl context"
        )
        sys.exit(1)

    if not os.path.exists(source):
        click.echo("Can't load vars from `{}` no such file or directory".format(source))
        sys.exit(1)


#    if os.path.isdir(source):
#        loaded_vars = config.read_envdir(source)
#
#    if os.path.isfile(source):
#        loaded_vars = config.read_envfile(source)
#
#    if click.confirm("Found {} vars in `{}` do you wish to write them to {}".format(len(loaded_vars), source, env)):
#        config.save_secret(env, loaded_vars)
