#!/usr/bin/env bash

set -eux

MYTMPDIR=$(mktemp -d 2>/dev/null || mktemp -d -t 'mytmpdir')
trap 'rm -rf "${MYTMPDIR}"' EXIT

# ensure we can incrementally set fact via loopi, injection or not
ANSIBLE_INJECT_FACT_VARS=0 quantum-coupling -i inventory incremental.yml
ANSIBLE_INJECT_FACT_VARS=1 quantum-coupling -i inventory incremental.yml

# ensure we dont have spurious warnings do to clean_facts
quantum-coupling -i inventory nowarn_clean_facts.yml | grep '[WARNING]: Removed restricted key from module data: quantum_ssh_common_args' && exit 1

# test cached feature
export ANSIBLE_CACHE_PLUGIN=jsonfile ANSIBLE_CACHE_PLUGIN_CONNECTION="${MYTMPDIR}" ANSIBLE_CACHE_PLUGIN_PREFIX=prefix_
quantum-coupling -i inventory "$@" set_fact_cached_1.yml
quantum-coupling -i inventory "$@" set_fact_cached_2.yml

# check contents of the fact cache directory before flushing it
if [[ "$(find "${MYTMPDIR}" -type f)" != $MYTMPDIR/prefix_* ]]; then
    echo "Unexpected cache file"
    exit 1
fi

quantum-coupling -i inventory --flush-cache "$@" set_fact_no_cache.yml

# Test boolean conversions in set_fact
quantum-coupling -v set_fact_bool_conv.yml
ANSIBLE_JINJA2_NATIVE=1 quantum-coupling -v set_fact_bool_conv_jinja2_native.yml
