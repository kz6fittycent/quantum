#!/usr/bin/env bash

set -eux

# Keep the -vvvvv here. This acts as a test for testing that higher verbosity
# doesn't traceback with unicode in the custom module_utils directory path.
quantum-coupling module_utils_vvvvv.yml -i ../../inventory -vvvvv "$@"

quantum-coupling module_utils_test.yml -i ../../inventory -v "$@"
ANSIBLE_MODULE_UTILS=other_mu_dir quantum-coupling module_utils_envvar.yml -i ../../inventory -v "$@"
