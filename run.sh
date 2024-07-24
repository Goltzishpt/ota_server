#!/bin/bash
set -xe
VENV="venv"

if [ ! -d "${VENV}" ]; then
    python3.11 -m venv "${VENV}"
    ${VENV}/bin/pip install --upgrade pip
    ${VENV}/bin/pip install -r requirements.txt
fi

if [ "$1" == "test" ]; then
    ${VENV}/bin/pytest
else
    ${VENV}/bin/python run.py
fi
