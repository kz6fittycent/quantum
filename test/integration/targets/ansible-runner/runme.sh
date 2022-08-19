#!/usr/bin/env bash

set -eux

ANSIBLE_ROLES_PATH=../ quantum-coupling test.yml -i inventory "$@"
