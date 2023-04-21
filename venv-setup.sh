#!/bin/sh

set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PY_VER="$(python --version)"

[[ "$PY_VER" =~ "Python 3" ]] && echo "Python 3 is installed"
echo "using $PY_VER"

read -p "Press any key to resume ..."