"""Routes of the app."""

import importlib.resources as resources

from registration_app import APP_NAME
from registration_app.app import app
from registration_app.forms.registration import RegistrationForm
from registration_app.service import participant

from bottle import jinja2_view, request, static_file


@app.route("/")
@jinja2_view("home.html.jinja")
def home():
    return {"request": request}


@app.route(r"/<filepath:path>")
def serve_static_file(filepath: str):
    with resources.path(APP_NAME, "static") as p:
        return static_file(filepath, p.as_posix())
