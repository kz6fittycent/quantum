#!/usr/bin/env bash

set -eux

quantum-coupling -i ../../inventory -v couplings/full_test.yml "$@"
