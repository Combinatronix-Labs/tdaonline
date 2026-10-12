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

### UI Design

Design attempt #3, the dark simplex blackboard design, is the default for all
pages. No design setting is needed for production. If a deployment already sets
`UI_DESIGN_ATTEMPT`, remove that override or set it to `3` to use the selected
design. Unrecognized values also use attempt #3.

Attempts #1 and #2 remain available for comparison. From the `flask` directory,
run each command in a separate terminal with your virtual environment activated:

```sh
UI_DESIGN_ATTEMPT=1 flask run --port 5001
UI_DESIGN_ATTEMPT=2 flask run --port 5002
UI_DESIGN_ATTEMPT=3 flask run --port 5004
```

Attempt #1 uses a green poster style; attempt #2 uses a simplex field notebook
style. These settings change presentation without changing page text or analysis
behavior.

The selected design uses system sans-serif fonts, larger reading text, visible
keyboard focus, a skip link, named controls and tables, and finite decorative
animation. Charts distinguish dimensions with marker shapes and line patterns
as well as contrasting colors. Accessibility checks target
[WCAG 2.2 Level AA](https://www.w3.org/TR/WCAG22/), including narrow layouts,
doubled text size, and custom text spacing. These checks are not a formal
conformance certification; test production content with assistive technology
before making a compliance claim. If image CAPTCHA is enabled, it still needs
an accessible alternative that does not depend on vision.

### Add Terms & Privacy Content

Legal document content is managed separately from Git. Before deployment, create
`flask/legal_content/` and add `privacy.html` and `terms.html`. This directory is
ignored by Git; the tracked page templates contain only the shared page layout.

Save each document as a UTF-8 HTML fragment containing its headings, text, and
links, without an outer `<html>` or `<body>` tag. These files are trusted content
managed by the site operator and are rendered as HTML, without interpreting
Jinja expressions. Editing a file updates the page on its next request.
Keep the supplied documents' heading structure, table headers, and named links
when editing them so screen-reader navigation remains available.

To keep the documents outside the checkout (for example, in a deployment-mounted
directory), set `LEGAL_CONTENT_DIR` to that directory's absolute path before
starting Flask. In production, put this setting in the service or container's
environment so the app receives it on startup:

```sh
export LEGAL_CONTENT_DIR=/srv/tdaonline/legal_content
```

The directory must contain the same two filenames. A fresh checkout does not
include the documents; copy them from your deployment's legal content source.
If a document is missing, its page displays an unavailable notice instead of a
server error. Back up these files separately from the repository.

### Run in Development & Debug Mode

In your machine's commandline terminal, run `FLASK_DEBUG=1 FLASK_ENV=development flask run` while inside the `flask` directory of this repository.

Make sure your virtual environment is activated when you do so.

### Run in Production Mode

In your machine's commandline terminal, run `flask run` while inside the `flask` directory of this repository.

Make sure your virtual environment is activated when you do so.
