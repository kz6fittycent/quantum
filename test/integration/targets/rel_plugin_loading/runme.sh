#!/usr/bin/env bash

set -eux

ANSIBLE_INVENTORY_ENABLED=notyaml quantum-coupling subdir/play.yml -i notyaml.yml "$@"
