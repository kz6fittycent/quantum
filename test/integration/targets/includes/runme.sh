#!/usr/bin/env bash

set -eux

quantum-coupling test_includes.yml -i ../../inventory "$@"
