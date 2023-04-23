#!/bin/sh

set +e

SAMPLE_URL="https://medimodel.com/wp-content/uploads/2021/03/2_skull_ct.zip"
SAMPLE_FNAME=$( basename $SAMPLE_URL .zip)

mkdir -vp tempstorage
if [ -d tempstorage/$SAMPLE_FNAME ]; then
  echo "downloading sample"
  echo
  curl -o tempstorage/$SAMPLE_FNAME.zip $SAMPLE_URL 
fi

mkdir -vp tempstorage/$SAMPLE_FNAME
unzip -d tempstorage/$SAMPLE_FNAME tempstorage/$SAMPLE_FNAME.zip 
read -p "Press any key to resume ..."