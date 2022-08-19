#!/usr/bin/env bash

SCRIPT_DIR=$(dirname "$0")

echo "Who am I:    $(whoami)"
echo "Home:        ${HOME}"
echo "PWD:         $(pwd)"
echo "Script dir:  ${SCRIPT_DIR}"

# restrict Quantum just to our inventory plugin, to prevent inventory data being matched by the test but being provided
# by some other dynamic inventory provider
export ANSIBLE_INVENTORY_ENABLED=docker_machine

[[ -n "$DEBUG" || -n "$ANSIBLE_DEBUG" ]] && set -x

set -euo pipefail

SAVED_PATH="$PATH"

cleanup() {
    PATH="${SAVED_PATH}"
    echo "Cleanup"
    quantum-coupling -i teardown.docker_machine.yml couplings/teardown.yml
    echo "Done"
}

trap cleanup INT TERM EXIT

echo "Pre-setup (install docker, docker-machine)"
ANSIBLE_ROLES_PATH=.. quantum-coupling couplings/pre-setup.yml

echo "Print docker-machine version"
docker-machine --version

echo "Check preconditions"
# Host should NOT be known to Quantum before the test starts
quantum-inventory -i inventory_1.docker_machine.yml --host vm >/dev/null && exit 1

echo "Test that the docker_machine inventory plugin is being loaded"
ANSIBLE_DEBUG=yes quantum-inventory -i inventory_1.docker_machine.yml --list | grep -F "Loading InventoryModule 'docker_machine'"

echo "Setup"
quantum-coupling couplings/setup.yml

echo "Test docker_machine inventory 1"
quantum-coupling -i inventory_1.docker_machine.yml couplings/test_inventory_1.yml

echo "Activate Docker Machine mock"
PATH=${SCRIPT_DIR}:$PATH

echo "Test docker_machine inventory 2: daemon_env=require daemon env success=yes"
quantum-inventory -i inventory_2.docker_machine.yml --list

echo "Test docker_machine inventory 2: daemon_env=require daemon env success=no"
export MOCK_ERROR_IN=env
quantum-inventory -i inventory_2.docker_machine.yml --list
unset MOCK_ERROR_IN

echo "Test docker_machine inventory 3: daemon_env=optional daemon env success=yes"
quantum-inventory -i inventory_3.docker_machine.yml --list

echo "Test docker_machine inventory 3: daemon_env=optional daemon env success=no"
export MOCK_ERROR_IN=env
quantum-inventory -i inventory_2.docker_machine.yml --list
unset MOCK_ERROR_IN

echo "Deactivate Docker Machine mock"
PATH="${SAVED_PATH}"
