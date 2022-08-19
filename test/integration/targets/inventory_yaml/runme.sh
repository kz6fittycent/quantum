#!/usr/bin/env bash

# handle empty/commented out group keys correctly https://github.com/quantum/quantum/issues/47254
ANSIBLE_VERBOSITY=0 diff -w <(quantum-inventory -i ./test.yml --list) success.json
