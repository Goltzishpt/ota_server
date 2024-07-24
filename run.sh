#!/bin/bash
set -xe
VENV="venv"

python3.11 -m venv "${VENV}"

source "${VENV}"/bin/activate
pip show flask

pip install -r requirements.txt

pip install flask

#export $(grep -v '^#' .env | xargs)

if [ "$1" == "test" ]; then
    pytest
else
    python3 run.py
fi
