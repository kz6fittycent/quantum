#!/usr/bin/env bash

set -eux

quantum-coupling traceback.yml -i inventory "$@"
