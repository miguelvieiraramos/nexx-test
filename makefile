test-cov:
	pytest -v --cov=. --cov-report=term --cov-report=html

code-convention:
	flake8
	pycodestyle

test:
	pytest -v