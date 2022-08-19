#!/usr/bin/env bash

set -eux

quantum testhost -i ../../inventory -m include_vars -a 'dir/inc.yml' "$@"
quantum testhost -i ../../inventory -m include_vars -a 'dir=dir' "$@"
