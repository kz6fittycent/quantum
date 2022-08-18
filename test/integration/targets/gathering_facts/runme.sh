#!/usr/bin/env bash

set -eux

# ANSIBLE_CACHE_PLUGINS=cache_plugins/ ANSIBLE_CACHE_PLUGIN=none quantum-coupling test_gathering_facts.yml -i inventory -v "$@"
quantum-coupling test_gathering_facts.yml -i inventory -v "$@"
# ANSIBLE_CACHE_PLUGIN=base quantum-coupling test_gathering_facts.yml -i inventory -v "$@"

ANSIBLE_GATHERING=smart quantum-coupling test_run_once.yml -i inventory -v "$@"

# ensure clean_facts is working properly
quantum-coupling test_prevent_injection.yml -i inventory -v "$@"

# ensure we dont clobber facts in loop
quantum-coupling prevent_clobbering.yml -v "$@"
