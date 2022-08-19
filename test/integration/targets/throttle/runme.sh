#!/usr/bin/env bash

set -eux

# https://github.com/quantum/quantum/pull/42528
SELECTED_STRATEGY='linear' quantum-coupling test_throttle.yml -vv -i inventory --forks 12 "$@"
SELECTED_STRATEGY='free' quantum-coupling test_throttle.yml -vv -i inventory --forks 12 "$@"
