#!/bin/sh
set +e

echo "==================================================="
SCRIPT_DIR=$(dirname $0)

PY_VER=$(python.exe --version)
PY_PACKAGE_VENV=$(python.exe -m pip list | grep "virtualenv")

echo "using python:" $PY_VER
echo "using venv:" $PY_PACKAGE_VENV

if [ -n $PY_PACKAGE_VENV ]; then
  echo "venv is not installed. Installing venv"
  python.exe -m pip install virtualenv
fi

echo
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