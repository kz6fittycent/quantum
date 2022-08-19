#!/usr/bin/env bash

set -ux

quantum-coupling -i ../../inventory coupling.yml -e "output_dir=${OUTPUT_DIR}" -v "$@"
