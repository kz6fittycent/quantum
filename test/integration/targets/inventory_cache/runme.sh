#!/usr/bin/env bash

set -eux

export ANSIBLE_INVENTORY_PLUGINS=./plugins/inventory

cleanup() {
    for f in ./cache/quantum_inventory*; do
	if [ -f "$f" ]; then rm -rf "$f"; fi
    done
}

trap 'cleanup' EXIT

# Test no warning when writing to the cache for the first time
test "$(quantum-inventory -i cache_host.yml --graph 2>&1 | tee out.txt | grep -c '\[WARNING\]')" = 0
writehost="$(grep "testhost[0-9]\{1,2\}" out.txt)"

# Test reading from the cache
test "$(quantum-inventory -i cache_host.yml --graph 2>&1 | tee out.txt | grep -c '\[WARNING\]')" = 0
readhost="$(grep 'testhost[0-9]\{1,2\}' out.txt)"

test "$readhost" = "$writehost"
