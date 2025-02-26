"""STOC registration app."""

import importlib.resources as resources

from bottle import Bottle, TEMPLATE_PATH

app = Bottle()
with resources.path("gnu_cauldron_reg", "views") as p:
    print(p)
    TEMPLATE_PATH.insert(0, p.as_posix())
