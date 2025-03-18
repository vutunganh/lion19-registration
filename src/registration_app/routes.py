"""Routes of the app."""

import importlib.resources as resources

from registration_app import APP_NAME
from registration_app.app import app
from registration_app.forms.registration import RegistrationForm
from registration_app.service import participant

from bottle import jinja2_view, request, static_file


@app.route("/")  # pyright: ignore
@jinja2_view("home.html.jinja")
def home():
    return {"request": request}


@app.route("/registration")  # pyright: ignore
@jinja2_view("registration.html.jinja")
def show_registration_form():
    form = RegistrationForm()
    return {"form": form}


@app.post("/registration")  # pyright: ignore
@jinja2_view("registration.html.jinja")
def register_participant():
    form = RegistrationForm(request.forms)  # pyright: ignore
    if not form.validate():
        return {"form": form}
    registration_result = participant.register_participant(form)
    return {"form": form, "registration_result": registration_result}


@app.route(r"/static/<filepath:path>")  # pyright: ignore
def serve_static_file(filepath: str):
    with resources.path(APP_NAME, "static") as p:
        return static_file(filepath, p.as_posix())
