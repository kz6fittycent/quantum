#!/usr/bin/env bash

set -eux

quantum-coupling test_environment.yml -i ../../inventory "$@"
