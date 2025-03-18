"""CLI access to the registration app."""

import argparse
from dataclasses import dataclass


@dataclass
class CliArgs:
    """CLI args of the app."""

    config_file_path: str


def parse_cli_args() -> CliArgs:
    """Parses CLI args of the app."""
    arg_parser = argparse.ArgumentParser(
        prog="Conference registration app",
        description="App for registrating participants to a conference",
        epilog="Contact <tung@iuuk.mff.cuni.cz> in case of any issues",
    )
    arg_parser.add_argument(
        "-c",
        "--config",
        help="Location of configuration file",
    )
    cli_args = arg_parser.parse_args()
    return CliArgs(
        config_file_path=cli_args.config,
    )
