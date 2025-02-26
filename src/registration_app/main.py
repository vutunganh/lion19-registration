"""Main for the registration app."""

import logging

import gnu_cauldron_reg.api
import gnu_cauldron_reg.routes # noqa: F401
from gnu_cauldron_reg.app import app
from gnu_cauldron_reg.config import load_app_args, load_app_config
from gnu_cauldron_reg.db.connection import perform_migrations, register_enums

from bottle import run

logging.basicConfig(datefmt="%Y-%m-%d %H:%M:%S")

app_args = load_app_args()
load_app_config(app_args.config_file_path)

perform_migrations(app.config["stoc_registration.Database.connection"])
register_enums(app.config["stoc_registration.Database.connection"])

if app_args.auto_run:
    run(app, host="127.0.0.1", port=8080)
