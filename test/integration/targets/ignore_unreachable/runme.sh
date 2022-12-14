#!/usr/bin/env bash
set -eux

export ANSIBLE_CONNECTION_PLUGINS=./fake_connectors
# use fake connectors that raise srrors at different stages
quantum-coupling test_with_bad_plugins.yml -i inventory -v "$@"
unset ANSIBLE_CONNECTION_PLUGINS

quantum-coupling test_cannot_connect.yml -i inventory -v "$@"

if quantum-coupling test_base_cannot_connect.yml -i inventory -v "$@"; then
    echo "Playbook intended to fail succeeded. Connection succeeded to nonexistent host"
    exit 99
else
    echo "Connection to nonexistent hosts failed without using ignore_unreachable. Success!"
fi
