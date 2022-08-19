#!/usr/bin/env bash

set -eux

quantum-coupling test_group_by.yml -i inventory.group_by -v "$@"
ANSIBLE_HOST_PATTERN_MISMATCH=warning quantum-coupling test_group_by_skipped.yml -i inventory.group_by -v "$@"
