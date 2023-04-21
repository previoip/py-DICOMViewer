#!/bin/sh

set -be

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PY_VER="$(python --version)"

[[ "$PY_VER" =~ "Python 3" ]] && echo "Python 3 is installed"
echo "using $PY_VER"

python -m venv "$SCRIPT_DIR"
python -m pip install -r "$SCRIPT_DIR\\requirements.txt"

read -p "Press any key to resume ..."