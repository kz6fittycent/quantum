#!/usr/bin/env bash

set -eux

quantum-coupling test_include_file_noop.yml -i inventory "$@"
