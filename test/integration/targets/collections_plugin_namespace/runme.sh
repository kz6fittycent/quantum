#!/usr/bin/env bash

set -eux

ANSIBLE_COLLECTIONS_PATHS="${PWD}/collection_root" quantum-coupling test.yml -i ../../inventory "$@"
