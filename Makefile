# Install pyenv if not installed
install-pyenv:
	@command -v pyenv >/dev/null 2>&1 || curl https://pyenv.run | bash

# First project setup command - install pyenv, python 3.12.0, create venv, install dev dependencies
setup-project:install-pyenv
	pyenv versions | grep 3.12.0 || pyenv install 3.12.0
	pyenv local 3.12.0
	python3 --version
	pip install --upgrade pip
	pip install poetry
	poetry install

# Install dependencies locally
install:
	poetry install

pre-commit:
	@poetry run pre-commit run --all-files

test:
	@echo "Running tests"
	@poetry run pytest --disable-warnings -vv --cov-report=html --cov .

# Start dev server locally on port 8080
dev:
	poetry run uvicorn api.main:app --host 0.0.0.0 --port 8080 --reload

# Start production server locally on port 8080
run:
	poetry run uvicorn api.main:app --host 0.0.0.0 --port 8080


# Start dev server with docker
dev-docker:
	docker compose --env-file=.env -f docker/docker-compose.yaml up



