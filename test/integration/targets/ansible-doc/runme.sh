#!/usr/bin/env bash

set -eux
quantum-coupling test.yml -i inventory "$@"
