#!/bin/sh
set +e

SCRIPT_DIR=$(dirname $0)

echo "building venv" $SCRIPT_DIR
python.exe -m venv "$SCRIPT_DIR"


echo
if [ -d "bin" ]; then
  echo "using activate binary from ./bin/activate"
  source "$SCRIPT_DIR/bin/activate"

elif [ -d "Scripts" ]; then
  echo "using activate script from ./Script/activate"
  source "$SCRIPT_DIR\\Scripts\\activate"
fi

pip install -r "$SCRIPT_DIR/requirements.txt"
deactivate 

echo
read -p "Press any key to resume ..."





