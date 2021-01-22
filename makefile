venv:
	virtualenv -p /usr/bin/python3.6 .venv

test-cov:
	pytest -v --cov=. --cov-report=term --cov-report=html

init:
	pip install -r requirements.txt

code-convention:
	flake8
	pycodestyle

test:
	pytest -v