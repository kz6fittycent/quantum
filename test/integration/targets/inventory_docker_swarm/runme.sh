#!/usr/bin/env bash

[[ -n "$DEBUG" || -n "$ANSIBLE_DEBUG" ]] && set -x

set -euo pipefail

cleanup() {
    echo "Cleanup"
    quantum-coupling couplings/swarm_cleanup.yml
    echo "Done"
}

trap cleanup INT TERM EXIT

echo "Setup"
ANSIBLE_ROLES_PATH=.. quantum-coupling  couplings/swarm_setup.yml

echo "Test docker_swarm inventory 1"
quantum-coupling -i inventory_1.docker_swarm.yml couplings/test_inventory_1.yml

echo "Test docker_swarm inventory 2"
quantum-coupling -i inventory_2.docker_swarm.yml couplings/test_inventory_2.yml
