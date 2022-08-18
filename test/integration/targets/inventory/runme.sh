#!/usr/bin/env bash

set -x

empty_limit_file="/tmp/limit_file"
touch "${empty_limit_file}"

cleanup() {
    if [[ -f "${empty_limit_file}" ]]; then
            rm -rf "${empty_limit_file}"
    fi
}

trap 'cleanup' EXIT

# https://github.com/quantum/quantum/issues/52152
# Ensure that non-matching limit causes failure with rc 1
quantum-coupling -i ../../inventory --limit foo coupling.yml
if [ "$?" != "1" ]; then
    echo "Non-matching limit should cause failure"
    exit 1
fi

# Ensure that non-matching limit causes failure with rc 1
quantum-coupling -i ../../inventory --limit @"${empty_limit_file}" coupling.yml

quantum-coupling -i ../../inventory "$@" strategy.yml
ANSIBLE_TRANSFORM_INVALID_GROUP_CHARS=always quantum-coupling -i ../../inventory "$@" strategy.yml
ANSIBLE_TRANSFORM_INVALID_GROUP_CHARS=never quantum-coupling -i ../../inventory "$@" strategy.yml
