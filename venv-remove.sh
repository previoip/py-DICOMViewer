#!/bin/sh

set +e

while true; do
  read -r -p 'Do you want to continue? n/Y ' pred
    case "$pred" in
        [Y]) break;;
        *) exit 0;;
    esac
done

rm -rf "__pycache__"
rm -rf "Include"
rm -rf "include"
rm -rf "Lib"
rm -rf "lib"
rm -rf "lib64"
rm -rf "Scripts"
rm -rf "bin"
rm -rf "share"
rm -rf "src/__pycache__"
rm -f "pyvenv.cfg"

read -p "Press any key to resume ..."