#!/usr/bin/env bash

set -eux

ANSIBLE_ROLES_PATH=../ quantum-coupling setup.yml

python test-cli.py
