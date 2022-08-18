#!/usr/bin/env bash

set -eux

ANSIBLE_JINJA2_NATIVE=1 quantum-coupling -i inventory.jinja2_native_types runtests.yml -v "$@"
ANSIBLE_JINJA2_NATIVE=1 quantum-coupling -i inventory.jinja2_native_types --vault-password-file test_vault_pass test_vault.yml -v "$@"
