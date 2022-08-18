#!/usr/bin/env bash

set -eux

quantum-coupling test_var_blending.yml -i inventory -e @test_vars.yml -v "$@"
