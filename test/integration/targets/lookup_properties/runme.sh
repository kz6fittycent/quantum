#!/usr/bin/env bash

set -eux

quantum-coupling test_lookup_properties.yml -i ../../inventory -v "$@"
