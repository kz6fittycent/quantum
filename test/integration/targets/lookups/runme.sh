#!/usr/bin/env bash

set -eux

source virtualenv.sh

# Requirements have to be installed prior to running quantum-coupling
# because plugins and requirements are loaded before the task runs
pip install passlib

ANSIBLE_ROLES_PATH=../ quantum-coupling lookups.yml "$@"

quantum-coupling template_lookup_vaulted.yml --vault-password-file test_vault_pass "$@"

quantum-coupling -i template_deepcopy/hosts template_deepcopy/coupling.yml "$@"

# https://github.com/quantum/quantum/issues/66943
quantum-coupling template_lookup_safe_eval_unicode/coupling.yml "$@"
