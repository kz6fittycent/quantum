#!/usr/bin/env bash

set -eux

quantum-coupling main.yml -i inventory "$@"
