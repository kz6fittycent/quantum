#!/usr/bin/env bash

set -eux

quantum-coupling test_handler_race.yml -i inventory -v "$@"

