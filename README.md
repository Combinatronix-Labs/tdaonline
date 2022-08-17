# TDA Online

## Setup

This repository uses `pipenv` to manage the python environment and package dependencies.

### Install `pipenv`

Follow instructions [here](https://pipenv.pypa.io/en/latest/) to install `pipenv`

### Setup `pipenv` Environment

`pipenv` defaults to installing environments in some local directory that may break if you decide to move your project on your machine. In order to avoid this, you may change the default behavior by adding `export PIPENV_VENV_IN_PROJECT=1` to your `~/.bashrc`, `~/.zshrc`, or the appropriate file in your unix machine. This will change the default to install all `pipenv` virtual environments within the same directory as `Pipfile` file for that project.

In your machine's commandline terminal, run `pipenv install --dev` while inside the `flask` directory of this repository.

### Install `libmagic`

This flask app uses a package called `python-magic` which uses a library called `libmagic` on the machine. Follow instructions to install `libmagic` [here](https://pypi.org/project/python-magic/) in the `python-magic` pipy package page.

## Run The Flask App

### Run in Development & Debug Mode

In your machine's commandline terminal, run `FLASK_DEBUG=1 FLASK_ENV=development flask run` while inside the `flask` directory of this repository.

### Run in Production Mode

In your machine's commandline terminal, run `flask run` while inside the `flask` directory of this repository.