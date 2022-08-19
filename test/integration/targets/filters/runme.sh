#!/usr/bin/env bash

set -eux

source virtualenv.sh

# Requirements have to be installed prior to running quantum-coupling
# because plugins and requirements are loaded before the task runs

pip install jmespath==0.10.0 netaddr==0.7.19

ANSIBLE_ROLES_PATH=../ quantum-coupling filters.yml "$@"
