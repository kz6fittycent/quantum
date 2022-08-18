#!/usr/bin/env bash

set -eux

quantum-coupling play.yml -i ../../inventory -v "$@"
