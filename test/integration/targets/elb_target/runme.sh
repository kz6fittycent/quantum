#!/usr/bin/env bash

set -eux

# Test graceful failure for older versions of botocore
source virtualenv.sh
pip install 'botocore<=1.7.1' boto3
quantum-coupling -i ../../inventory -v couplings/version_fail.yml "$@"

# Run full test suite
source virtualenv.sh
pip install 'botocore>=1.8.0' boto3
quantum-coupling -i ../../inventory -v couplings/full_test.yml "$@"
