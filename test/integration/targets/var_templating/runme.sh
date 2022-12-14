#!/usr/bin/env bash

set -eux

# this should succeed since we override the undefined variable
quantum-coupling undefined.yml -i inventory -v "$@" -e '{"mytest": False}'

# this should still work, just show that var is undefined in debug
quantum-coupling undefined.yml -i inventory -v "$@"

# this should work since we dont use the variable
quantum-coupling undall.yml -i inventory -v "$@"

# test hostvars templating
quantum-coupling task_vars_templating.yml -v "$@"

quantum-coupling test_connection_vars.yml -v "$@" 2>&1 | grep 'sudo'
