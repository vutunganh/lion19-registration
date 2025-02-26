"""Routes of the app."""

import importlib.resources as resources

from gnu_cauldron_reg.app import app
from gnu_cauldron_reg.forms.registration import RegistrationForm
from gnu_cauldron_reg.service import participant

from bottle import jinja2_view, request, static_file


@app.route("/")
@jinja2_view("home.html.jinja")
def home():
    return {"request": request}


@app.route("/registration")
@jinja2_view("registration.html.jinja")
def show_registration_form():
    form = RegistrationForm()
    return {"form": form}


@app.post("/registration")
@jinja2_view("registration.html.jinja")
def register_participant():
    form = RegistrationForm(request.forms)
    if not form.validate():
        return {"form": form}
    registration_result = participant.register_participant(form)
    return {"form": form, "registration_result": registration_result}


@app.route(r"/static/<filepath:path>")
def serve_static_file(filepath: str):
    with resources.path("gnu_cauldron_reg", "static") as p:
        return static_file(filepath, p.as_posix())
