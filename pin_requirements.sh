#!/bin/bash -e

## Take the content from requirements.in and compile fully pinned requirements.txt

# Run in virtualenv.
VENV=$(mktemp -du)
virtualenv ${VENV}
source ${VENV}/bin/activate

function cleanup {
  rm -rf ${VENV}
}
trap cleanup EXIT

pip install 'pip>7.0.0'
pip install -U 'pip-tools>=1.6'  # 1.6 is the first version to support `--upgrade`.

REQ_BASE=requirements

echo "=== Compiling ${REQ_BASE}.txt ==="

pip-compile --upgrade --no-header --no-index ${REQ_BASE}.in -o ${REQ_BASE}.txt
sed -i '1i# DO NOT MODIFY THIS FILE. See `pin_requirements.sh` instead\n' ${REQ_BASE}.txt

echo -e '\npip>=7.0.0' >> ${REQ_BASE}.txt
