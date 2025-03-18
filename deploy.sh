#!/bin/bash
set -e

if [ "$HOSTNAME" != nikam -o "$USER" != lion19 ] ; then
    echo "Run me as lion19@nikam, please"
    exit 1
fi

DEST=~/registration
. $DEST/venv/bin/activate
uv build
uv pip install --force-reinstall dist/registration_app-0.1.0.tar.gz

if [ -e $DEST/var/uwsgi.fifo ] ; then
    echo "Reloading uwsgi"
    echo r >$DEST/var/uwsgi.fifo || true
else
    echo "Restarting uwsgi"
    systemctl --user restart registration_app
fi

