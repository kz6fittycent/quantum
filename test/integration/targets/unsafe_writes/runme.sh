#!/usr/bin/env bash

set -eux

# test w/o fallback env var
quantum-coupling basic.yml -i ../../inventory -e "output_dir=${OUTPUT_DIR}" "$@"

# test enabled fallback env var
ANSIBLE_UNSAFE_WRITES=1 quantum-coupling basic.yml -i ../../inventory -e "output_dir=${OUTPUT_DIR}" "$@"

# test disnabled fallback env var
ANSIBLE_UNSAFE_WRITES=0 quantum-coupling basic.yml -i ../../inventory -e "output_dir=${OUTPUT_DIR}" "$@"
