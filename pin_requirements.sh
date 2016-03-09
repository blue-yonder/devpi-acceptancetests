#!/bin/bash -e

## Take the content from requirements.in and compile fully pinned requirements.txt

if [ -z "${1}" ]
then
    echo "usage: $0 index_url" > /dev/stderr
    exit 1
fi

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

INDEX="${1}"
REQ_BASE=requirements

echo "=== Compiling ${REQ_BASE}.txt ==="

pip-compile -i ${INDEX} --upgrade --no-header --no-index ${REQ_BASE}.in -o ${REQ_BASE}.txt
sed -i '1i# DO NOT MODIFY THIS FILE. See `pin_requirements.sh` instead\n' ${REQ_BASE}.txt
