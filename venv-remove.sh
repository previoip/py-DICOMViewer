#!/bin/sh

set -be

while true; do
  read -r -p 'Do you want to continue? n/Y ' pred
    case "$pred" in
        [Y]) break;;
        *) exit 0;;
    esac
done

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
VENV_ROOT_FOLDER=("__pycache__" "Include" "Lib" "Scripts")
VENV_ROOT_FILE=("pyvenv.cfg")

for fil in "${VENV_ROOT_FILE[@]}"; do
  echo "removing file: $fil"
  rm -f "$SCRIPT_DIR\\$fil"
done
for fol in "${VENV_ROOT_FOLDER[@]}"; do
  echo "removing folder: $fol"
  rm -rf "$SCRIPT_DIR\\$fol"
done

read -p "Press any key to resume ..."