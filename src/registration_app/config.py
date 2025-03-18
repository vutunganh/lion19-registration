"""App configuration."""

import logging
import os
import tomllib
from dataclasses import dataclass
from pathlib import Path

from registration_app.app import app
from registration_app.cli import parse_cli_args


logger = logging.getLogger(__name__)


@dataclass
class AppArgs:
    config_file_path: str
    auto_run: bool = False

    def __post_init__(self):
        logger.info(f"Using config file '{self.config_file_path}'")


def load_app_config(config_path: str) -> None:
    with Path(config_path).open("rb") as f:
        app_config = tomllib.load(f)
    app_config = {"registration_app": app_config}
    app.config.load_dict(app_config)
    print(app.config)


def load_app_args() -> AppArgs:
    cauldron_config_env = "REGISTRATION_APP_CONFIG"
    if cauldron_config_env in os.environ:
        return AppArgs(
            config_file_path=os.environ[cauldron_config_env],
            auto_run=False,
        )
    cli_args = parse_cli_args()
    return AppArgs(
        config_file_path=cli_args.config_file_path,
        auto_run=True,
    )
