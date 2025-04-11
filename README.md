# LION19 registration app

The purpose of this web app is to register [LION19 conference](https://lion19.org) participants.
However, it is written in a way so that it can "easily" re-used for other conferences.

## Developer tools

This project is managed by [uv](https://docs.astral.sh/uv).

We use [bottle.py](https://bottlepy.org/) framework.
It is like [Flask](https://flask.palletsprojects.com/en/stable/) but I find that Flask gets in the way too much.
But we still use [Jinja2](https://jinja.palletsprojects.com/en/stable/).
Additionally on the web app side, we use:
* [GPWebpay library](https://github.com/filias/gpwebpay) for interacting with the payment gate
* [HTTPX](https://www.python-httpx.org/) for making http requests (a more modern variant of [requests](https://docs.python-requests.org/en/latest/index.html). It supports `async` for an example).
* [WTForms](https://wtforms.readthedocs.io/) to not go crazy from HTML forms.

To access the database ([PostgreSQL](https://www.postgresql.org/)), we use raw sql via [psycopg3](https://www.psycopg.org/psycopg3/docs/index.html).
Make sure to use version 3 and not version 2!
Eventually, I would like to use [peewee](https://docs.peewee-orm.com/en/latest/) as a micro-ORM.
We perform database migrations using [yoyo-migrations](https://pypi.org/project/yoyo-migrations/).

We use [pre-commit](https://pre-commit.com/) hooks to make sure that our code is nice!

## Configuration files

This app uses two configuration files.
The reason being that one of the libraries insists on reading the configuration from env, and the author does not have time to have a pull request accepted.
See `config.example.toml` and `example.env` for examples.

One day, I would like to use [Pydantic](https://docs.pydantic.dev/) to validate the configuration file.

## Deployment

The app listens in root.

## How to initialize the app?

These instruction are obtained by reverse-engineering the HALG 2023 version of this app.

1. Create a directory containing the app and its configuration files, e.g. `~/registration`.
1. Copy contents of `init/skeleton` to `~/registration`.
    * `cp -r init/skeleton/* ~/registration/`.
    * At the moment of writing, it should be three directories: `etc`, `var`, `log`.
1. Create a user service using `init/cauldron_reg.service`.
    * Put it in `~/.config/systemd/user/` directory and run `systemctl --user enable --now cauldron_reg`.
    * If using systemd, make sure that the user has `enable-linger` enabled.
1. Create a virtual environment in `~registration` named `venv`.
    * `python3 -m venv ~/registration/venv`.
1. There should now be two config files in `~/registration/etc/`.
    1. One of them is `config.toml`. The configuration is straightforward.
        * In fields that are either private or public keys a base64 encoded key is expected.
        Something like `cat file_with_keys.pub | base64 -w0` should output the right thing.
    3. The second one is `cauldron.uwsgi`.
    Here you need to go to the end where there is a bunch of lines starting with `env = SOMETHING_ALL_CAPS=`.
    This is for setting necessary environment variables.
    Simply put the values after the last `=` sign.
    Avoid values that have a `%` because they get "interpreted" by the configuration language.
    If needed `%%` is one `%`.
1. Run `deploy.sh` once.
