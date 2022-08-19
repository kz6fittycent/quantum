#!/usr/bin/env bash

set -eux

quantum-coupling -v -i inventory.ini test_quantum_become.yml
