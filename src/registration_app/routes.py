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
    form = RegistrationForm()
    return {"form": form}


@app.post("/")  # pyright: ignore
@jinja2_view("home.html.jinja")
def register():
    form = RegistrationForm(request.forms)  # pyright: ignore
    if not form.validate():
        return {"form": form}
    registration_result = participant.register_participant(form)
    return {"form": form, "registration_result": registration_result}


@app.get("/payment-callback")  # pyright: ignore
@jinja2_view("payment_callback.html.jinja")
def payment_callback():
    res = participant.validate_payment(request.url)
    return {"res": res}


@app.route(r"/static/<filepath:path>")  # pyright: ignore
def serve_static_file(filepath: str):
    with resources.path(APP_NAME, "static") as p:
        return static_file(filepath, p.as_posix())


@app.route(r"/images/<filepath:path>")  # pyright: ignore
def serve_images(filepath: str):
    with resources.path(APP_NAME, "static") as p:
        return static_file(filepath, (p / "images").as_posix())


@app.route(r"/liba/<filepath:path>")  # pyright: ignore
def serve_liba(filepath: str):
    with resources.path(APP_NAME, "static") as p:
        return static_file(filepath, (p / "liba").as_posix())
