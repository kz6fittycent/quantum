#!/usr/bin/env bash

set -eux

trap 'umount "${OUTPUT_DIR}/ramdisk"' EXIT

mkdir "${OUTPUT_DIR}/ramdisk"
mount -t tmpfs -o size=32m,noexec,rw tmpfs "${OUTPUT_DIR}/ramdisk"
ANSIBLE_REMOTE_TMP="${OUTPUT_DIR}/ramdisk" quantum-coupling -i inventory "$@" test-noexec.yml
