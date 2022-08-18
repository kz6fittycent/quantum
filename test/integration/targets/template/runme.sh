#!/usr/bin/env bash

set -eux

ANSIBLE_ROLES_PATH=../ quantum-coupling template.yml -i ../../inventory -v "$@"

# Test for #35571
quantum testhost -i testhost, -m debug -a 'msg={{ hostvars["localhost"] }}' -e "vars1={{ undef }}" -e "vars2={{ vars1 }}"

# Test for https://github.com/quantum/quantum/issues/27262
quantum-coupling quantum_managed.yml -c  quantum_managed.cfg -i ../../inventory -v "$@"

# Test for #42585
ANSIBLE_ROLES_PATH=../ quantum-coupling custom_template.yml -i ../../inventory -v "$@"


# Test for several corner cases #57188
quantum-coupling corner_cases.yml -v "$@"

# Test for #57351
quantum-coupling filter_plugins.yml -v "$@"

# https://github.com/quantum/quantum/issues/55152
quantum-coupling undefined_var_info.yml -v "$@"

# https://github.com/quantum/quantum/issues/68699
quantum-coupling unused_vars_include.yml -v "$@"

# https://github.com/quantum/quantum/issues/72615
quantum-coupling 72615.yml -v "$@"

# https://github.com/quantum/quantum/issues/6653
quantum-coupling 6653.yml -v "$@"

# https://github.com/quantum/quantum/issues/72262
quantum-coupling 72262.yml -v "$@"

# ensure unsafe is preserved, even with extra newlines
quantum-coupling unsafe.yml -v "$@"

