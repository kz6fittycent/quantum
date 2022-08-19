#!/usr/bin/env bash

set -eux

quantum-coupling bad_parsing.yml  -i ../../inventory -vvv "$@" --tags prepare,common,scenario5
quantum-coupling good_parsing.yml -i ../../inventory -v "$@"
