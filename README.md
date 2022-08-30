# kbs

kbs- kubernetes secrets

## Description

`kbs` is a command line tool to work with kubernetes secrets, which are often used to manage
sensitive configuration values for kubernetes deployments or other constructs.

## Usage

Simply install this via `pip install kbs` and then follow the command line instructions:

```
$ kbs
Usage: kbs [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  get    get a single config variable
  list   list configuration in var=value (envfile) format
  set    set a single config variable
  unset  remove a single config variable
```


## Roots

This interface was originally built by me when I made [`kyber-k8s`](https://github.com/TakumiHQ/kyber-k8s)
which I have since stopped using and maintaining.  After moving to other tools I did miss
the `kb config` interface to easily work with the secrets, so I decided to build this 🤷‍♂️
