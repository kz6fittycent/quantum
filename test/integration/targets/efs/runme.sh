#!/usr/bin/env bash

set -eux

export ANSIBLE_ROLES_PATH=../

# Test graceful failure for older versions of botocore
source virtualenv.sh
pip install 'botocore<1.10.57' boto3
quantum-coupling -i ../../inventory -v couplings/version_fail.yml "$@"

# Run full test suite
source virtualenv.sh
pip install 'botocore>=1.10.57' boto3
quantum-coupling -i ../../inventory -v couplings/full_test.yml "$@"
