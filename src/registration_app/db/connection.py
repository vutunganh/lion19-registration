"""Handlers for database connection and migrations."""

import importlib.resources as resources
import logging

from registration_app import APP_NAME
from registration_app.app import app
from registration_app.model.participant import RegistrationFeeType

import psycopg
from bottle import request, response
from psycopg.types.enum import EnumInfo, register_enum
from yoyo import get_backend, read_migrations

logger = logging.getLogger(__name__)


def perform_migrations(connection_str: str):
    logger.info("[DB migrations] Starting")
    db_backend = get_backend(
        # Must do this replacement to use psycopg3 instead of psycopg2.
        # https://ollycope.com/software/yoyo/latest/#connecting-to-a-database
        connection_str.replace("postgresql://", "postgresql+psycopg://"),
    )
    logger.info("[DB migrations] Connected to DB")
    with resources.path(APP_NAME, "db") as f:
        migrations_path = (f / "migrations").as_posix()
        logger.info(f"[DB migrations] Reading migrations from {migrations_path}")
        migrations = read_migrations(migrations_path)
        logger.info("[DB migrations] Successfully read migrations")
        with db_backend.lock():
            db_backend.apply_migrations(db_backend.to_apply(migrations))
    logger.info("[DB migrations] Applied")


def register_enums(connection_str: str):
    db = psycopg.connect(connection_str)
    info = EnumInfo.fetch(db, "registration_fee_type")
    if info is None:
        raise RuntimeError(
            "`registration_fee_type` should be an enum defined in the database but"
            " it could not be found"
        )
    register_enum(info, db, RegistrationFeeType)


@app.hook("before_request")
def open_db():
    try:
        request.db = psycopg.connect(
            app.config["registration_app.Database.connection"],
            autocommit=True,
        )
    except psycopg.Error:
        response.status = 500
        response.body = {"error": "Database connection failed"}
        logger.exception("Connecting to the database failed")


@app.hook("after_request")
def close_db():
    if not hasattr(request, "db"):
        return
    try:
        request.db.close()
    except psycopg.Error:
        logger.exception("Error closing the dabase connection")
