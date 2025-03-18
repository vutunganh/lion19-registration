"""Conference registration app."""

import importlib.resources as resources

from registration_app import APP_NAME

from bottle import Bottle, TEMPLATE_PATH

app = Bottle()
with resources.path(APP_NAME, "views") as p:
    TEMPLATE_PATH.insert(0, p.as_posix())
