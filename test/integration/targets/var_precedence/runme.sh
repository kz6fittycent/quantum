#!/usr/bin/env bash

set -eux

quantum-coupling test_var_precedence.yml -i inventory -v "$@" \
    -e 'extra_var=extra_var' \
    -e 'extra_var_override=extra_var_override'

./quantum-var-precedence-check.py
