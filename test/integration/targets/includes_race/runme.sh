#!/usr/bin/env bash

set -eux

quantum-coupling test_includes_race.yml -i inventory -v "$@"
