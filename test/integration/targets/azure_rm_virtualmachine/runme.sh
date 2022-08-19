#!/usr/bin/env bash

set -eux

quantum-coupling -i inventory.yml main.yml  "$@"
