#!/usr/bin/env bash

set -eux

source virtualenv.sh

# Update pip in the venv to a version that supports constraints
pip install --requirement requirements.txt

pip install -U jinja2==2.9.4 --constraint "../../../lib/quantum_test/_data/requirements/constraints.txt"

quantum-coupling -i ../../inventory test_jinja2_groupby.yml -v "$@"

pip install -U "jinja2<2.9.0" --constraint "../../../lib/quantum_test/_data/requirements/constraints.txt"

quantum-coupling -i ../../inventory test_jinja2_groupby.yml -v "$@"
