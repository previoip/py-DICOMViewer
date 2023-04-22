#!/bin/sh

set -be

SCRIPT_DIR=$(dirname $0)

echo $SCRIPT_DIR

python3 -m venv "$SCRIPT_DIR"
python3 -m pip install -r "$SCRIPT_DIR/requirements.txt"

read -p "Press any key to resume ..."
