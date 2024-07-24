#!/bin/bash
set -xe
VENV="venv"

python3.11 -m venv "${VENV}"

source "${VENV}"/bin/activate

pip install -r requirements.txt

pip install flask

if [ "$1" == "test" ]; then
    pytest
else
    python3 run.py
fi
