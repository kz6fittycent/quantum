#!/usr/bin/env bash

set -eux

source virtualenv.sh

pip install --requirement pip-requirements.txt

pip install -U -r requirements.txt --constraint "../../../lib/quantum_test/_data/requirements/constraints.txt"

ANSIBLE_ROLES_PATH=../
export ANSIBLE_ROLES_PATH

quantum-coupling -i ../../inventory main.yml -v "$@"
