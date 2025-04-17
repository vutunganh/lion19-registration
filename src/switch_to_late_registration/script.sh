#!/usr/bin/env sh

set -eu

DEPLOY_SCRIPT_NAME="deploy.sh"
configuration_file="$1"
path_to_deploy_script="$2"

sed -i -s 's|regular = 13000|regular = 15000|' "$configuration_file"
sed -i -s 's|student = 11000|student = 13000|' "$configuration_file"

cd "$path_to_deploy_script"
bash "$DEPLOY_SCRIPT_NAME"
