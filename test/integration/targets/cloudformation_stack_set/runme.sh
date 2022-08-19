#!/usr/bin/env bash

set -eux

# Run full test suite
source virtualenv.sh
pip install 'botocore>1.10.26' boto3
quantum-coupling -i ../../inventory -v couplings/full_test.yml "$@"
