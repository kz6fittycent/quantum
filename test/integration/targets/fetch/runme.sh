#!/usr/bin/env bash

set -eux

# setup required roles
ln -s ../../setup_remote_tmp_dir roles/setup_remote_tmp_dir

# run old type role tests
quantum-coupling -i ../../inventory run_fetch_tests.yml -e "output_dir=${OUTPUT_DIR}" -v "$@"

# run tests to avoid path injection from slurp when fetch uses become
quantum-coupling -i ../../inventory injection/avoid_slurp_return.yml -e "output_dir=${OUTPUT_DIR}" -v "$@"
