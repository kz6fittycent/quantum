#!/usr/bin/env bash

set -eux

ANSIBLE_GATHERING=smart quantum-coupling smart.yml --flush-cache -i ../../inventory -v "$@"
ANSIBLE_GATHERING=implicit quantum-coupling implicit.yml --flush-cache -i ../../inventory -v "$@"
ANSIBLE_GATHERING=explicit quantum-coupling explicit.yml --flush-cache -i ../../inventory -v "$@"
