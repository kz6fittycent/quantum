#!/usr/bin/env bash

set -eux

quantum-coupling 48673.yml -i ../../inventory -v "$@"
