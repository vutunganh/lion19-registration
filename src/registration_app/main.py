"""Main for the registration app."""

import logging

import registration_app.routes  # noqa: F401
from registration_app.app import app
from registration_app.config import load_app_args, load_app_config
from registration_app.db.connection import perform_migrations, register_enums
from registration_app.service.payment import configure_gpwebpay

from bottle import run

logging.basicConfig(datefmt="%Y-%m-%d %H:%M:%S")

app_args = load_app_args()
load_app_config(app_args.config_file_path)

perform_migrations(app.config["registration_app.Database.connection"])
register_enums(app.config["registration_app.Database.connection"])

configure_gpwebpay()

if app_args.auto_run:
    run(app, host="127.0.0.1", port=8080)
