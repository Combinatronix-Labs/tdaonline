# TDA Online
This application is a web app that is meant provide a service to compute persistence data given data formatted a certain way. It also is source of learning material on Topological Data Analysis (TDA).

This application is a Flask application which uses Flask's built-in templating schema for the `html` called Jinja2.

## Setup Local Development

### Install Python
Install python [here](https://www.python.org/downloads/). Version `3.8` should work just fine. 

OS built-in versions may not properly run this project. For example, Ubuntu comes with a version of python, but it will not properly install the development evnvironment for running the application. Make sure to install a separate copy if you do not have one.

### Setup Virtual Environment
The previously menctioned version of Python and any newer version comes with the module `venv` which is used to create vertual environment. Virtual environments are meant to isolate a version of Python that will have install modules only for the project. This way, versions of dependencies that are only relevant to the project will stay the same and will not be effected by modules installed in your global copy of python.

With your global copy of Python that was installed in the previous step and a terminal with working directory set to the root directory of this project, run `python -m venv .venv`. After running the command, you will notice that there is a new directory created with the name `.venv`.

More information on `venv` can be found here [here](https://docs.python.org/3.8/tutorial/venv.html).

### Activate Virtual Environment
To access the virtual environment in your terminal session, you must activate it. To activate it, run:
- On Windows, `.venv\Scripts\activate.bat`
- On Mac or Unix, `source .venv/bin/activate`

After activating the virtual environment, you will notice that your terminal line will now start with `(.venv)...` which indicates that any `python` or `pip` commands will not be using the global ones but the ones found in `.venv` somewhere.

### Install Dependencies

To install dependencies to your newly activated virtual environment or to update your installed modules that others may have added to this project, run `pip install -r requirements.txt`.

Make sure your virtual environment is activated when you do so.

### Save Dependencies

Whenever you wish to add dependencies to this repository, run `pip freeze > requirements.txt`.

Make sure your virtual environment is activated when you do so.

### Install `libmagic`

This flask app uses a package called `python-magic` which uses a library called `libmagic` on the machine. Follow instructions to install `libmagic` [here](https://pypi.org/project/python-magic/) in the `python-magic` pipy package page.

Make sure your virtual environment is activated when you do so.

## Run The Flask App

### Run in Development & Debug Mode

In your machine's commandline terminal, run `FLASK_DEBUG=1 FLASK_ENV=development flask run` while inside the `flask` directory of this repository.

Make sure your virtual environment is activated when you do so.

### Run in Production Mode

In your machine's commandline terminal, run `flask run` while inside the `flask` directory of this repository.

Make sure your virtual environment is activated when you do so.