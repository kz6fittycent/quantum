#!/usr/bin/env bash

set -eux

quantum-coupling check_mode.yml -i ../../inventory -v --check "$@"
quantum-coupling check_mode-on-cli.yml -i ../../inventory -v --check "$@"
quantum-coupling check_mode-not-on-cli.yml -i ../../inventory -v "$@"
