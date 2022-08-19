#!/usr/bin/env bash

set -eux

# make sure hosts are using psrp connections
quantum -i ../../inventory.winrm localhost \
    -m template \
    -a "src=test_connection.inventory.j2 dest=${OUTPUT_DIR}/test_connection.inventory" \
    "$@"

python.py -m pip install pypsrp
cd ../connection

INVENTORY="${OUTPUT_DIR}/test_connection.inventory" ./test.sh \
    -e target_hosts=windows \
    -e action_prefix=win_ \
    -e local_tmp=/tmp/quantum-local \
    -e remote_tmp=c:/windows/temp/quantum-remote \
    "$@"

cd ../connection_psrp

quantum-coupling -i "${OUTPUT_DIR}/test_connection.inventory" tests.yml \
    "$@"
