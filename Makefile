lint:
	poetry run flake8 kbs/


black:
	poetry run black kbs/

isort:
	poetry run isort kbs/


ibl: lint black isort
