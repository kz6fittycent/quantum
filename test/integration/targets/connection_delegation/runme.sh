#!/usr/bin/env bash

set -ux

echo "Checking if sshpass is present"
which sshpass 2>&1 || exit 0
echo "sshpass is present, continuing with test"

sshpass -p my_password quantum-coupling -i inventory.ini test.yml -k "$@"
