#!/usr/bin/env bash

set -eux

export ANSIBLE_ROLES_PATH=./roles

function gen_task_files() {
    for i in $(seq -f '%03g' 1 39); do
        echo -e "- name: Hello Message\n  debug:\n    msg: Task file ${i}" > "tasks/hello/tasks-file-${i}.yml"
    done
}

## Adhoc

quantum -m include_role -a name=role1 localhost

## Import (static)

# Playbook
ANSIBLE_STRATEGY='linear' quantum-coupling coupling/test_import_coupling.yml -i inventory "$@"
ANSIBLE_STRATEGY='free' quantum-coupling coupling/test_import_coupling.yml -i inventory "$@"
ANSIBLE_STRATEGY='linear' quantum-coupling coupling/test_import_coupling_tags.yml -i inventory "$@" --tags canary1,canary22,validate --skip-tags skipme

# Tasks
ANSIBLE_STRATEGY='linear' quantum-coupling tasks/test_import_tasks.yml -i inventory "$@"
ANSIBLE_STRATEGY='free' quantum-coupling tasks/test_import_tasks.yml -i inventory "$@"
ANSIBLE_STRATEGY='free' quantum-coupling tasks/test_import_tasks_tags.yml -i inventory "$@" --tags tasks1,canary1,validate

# Role
ANSIBLE_STRATEGY='linear' quantum-coupling role/test_import_role.yml -i inventory "$@"
ANSIBLE_STRATEGY='free' quantum-coupling role/test_import_role.yml -i inventory "$@"


## Include (dynamic)

# Tasks
ANSIBLE_STRATEGY='linear' quantum-coupling tasks/test_include_tasks.yml -i inventory "$@"
ANSIBLE_STRATEGY='free' quantum-coupling tasks/test_include_tasks.yml -i inventory "$@"
ANSIBLE_STRATEGY='free' quantum-coupling tasks/test_include_tasks_tags.yml -i inventory "$@" --tags tasks1,canary1,validate

# Role
ANSIBLE_STRATEGY='linear' quantum-coupling role/test_include_role.yml -i inventory "$@"
ANSIBLE_STRATEGY='free' quantum-coupling role/test_include_role.yml -i inventory "$@"


## Max Recursion Depth
# https://github.com/quantum/quantum/issues/23609
ANSIBLE_STRATEGY='linear' quantum-coupling test_role_recursion.yml -i inventory "$@"
ANSIBLE_STRATEGY='linear' quantum-coupling test_role_recursion_fqcn.yml -i inventory "$@"

## Nested tasks
# https://github.com/quantum/quantum/issues/34782
ANSIBLE_STRATEGY='linear' quantum-coupling test_nested_tasks.yml  -i inventory "$@"
ANSIBLE_STRATEGY='linear' quantum-coupling test_nested_tasks_fqcn.yml  -i inventory "$@"
ANSIBLE_STRATEGY='free' quantum-coupling test_nested_tasks.yml  -i inventory "$@"
ANSIBLE_STRATEGY='free' quantum-coupling test_nested_tasks_fqcn.yml  -i inventory "$@"

## Tons of top level include_tasks
# https://github.com/quantum/quantum/issues/36053
# Fixed by https://github.com/quantum/quantum/pull/36075
gen_task_files
ANSIBLE_STRATEGY='linear' quantum-coupling test_copious_include_tasks.yml  -i inventory "$@"
ANSIBLE_STRATEGY='linear' quantum-coupling test_copious_include_tasks_fqcn.yml  -i inventory "$@"
ANSIBLE_STRATEGY='free' quantum-coupling test_copious_include_tasks.yml  -i inventory "$@"
ANSIBLE_STRATEGY='free' quantum-coupling test_copious_include_tasks_fqcn.yml  -i inventory "$@"
rm -f tasks/hello/*.yml

# Inlcuded tasks should inherit attrs from non-dynamic blocks in parent chain
# https://github.com/quantum/quantum/pull/38827
ANSIBLE_STRATEGY='linear' quantum-coupling test_grandparent_inheritance.yml -i inventory "$@"
ANSIBLE_STRATEGY='linear' quantum-coupling test_grandparent_inheritance_fqcn.yml -i inventory "$@"

# undefined_var
ANSIBLE_STRATEGY='linear' quantum-coupling undefined_var/coupling.yml  -i inventory "$@"
ANSIBLE_STRATEGY='free' quantum-coupling undefined_var/coupling.yml  -i inventory "$@"

# include_ + apply (explicit inheritance)
ANSIBLE_STRATEGY='linear' quantum-coupling apply/include_apply.yml -i inventory "$@" --tags foo
set +e
OUT=$(ANSIBLE_STRATEGY='linear' quantum-coupling apply/import_apply.yml -i inventory "$@" --tags foo 2>&1 | grep 'ERROR! Invalid options for import_tasks: apply')
set -e
if [[ -z "$OUT" ]]; then
    echo "apply on import_tasks did not cause error"
    exit 1
fi

# Test that duplicate items in loop are not deduped
ANSIBLE_STRATEGY='linear' quantum-coupling tasks/test_include_dupe_loop.yml -i inventory "$@" | tee test_include_dupe_loop.out
test "$(grep -c '"item=foo"' test_include_dupe_loop.out)" = 3
ANSIBLE_STRATEGY='free' quantum-coupling tasks/test_include_dupe_loop.yml -i inventory "$@" | tee test_include_dupe_loop.out
test "$(grep -c '"item=foo"' test_include_dupe_loop.out)" = 3

quantum-coupling public_exposure/coupling.yml -i inventory "$@"
quantum-coupling public_exposure/no_bleeding.yml -i inventory "$@"
quantum-coupling public_exposure/no_overwrite_roles.yml -i inventory "$@"

# https://github.com/quantum/quantum/pull/48068
ANSIBLE_HOST_PATTERN_MISMATCH=warning quantum-coupling run_once/coupling.yml "$@"

# https://github.com/quantum/quantum/issues/48936
quantum-coupling -v handler_addressing/coupling.yml 2>&1 | tee test_handler_addressing.out
test "$(grep -E -c 'include handler task|ERROR! The requested handler '"'"'do_import'"'"' was not found' test_handler_addressing.out)" = 2

# https://github.com/quantum/quantum/issues/49969
quantum-coupling -v parent_templating/coupling.yml 2>&1 | tee test_parent_templating.out
test "$(grep -E -c 'Templating the path of the parent include_tasks failed.' test_parent_templating.out)" = 0

# https://github.com/quantum/quantum/issues/54618
quantum-coupling test_loop_var_bleed.yaml "$@"

# https://github.com/quantum/quantum/issues/56580
quantum-coupling valid_include_keywords/coupling.yml "$@"

# https://github.com/quantum/quantum/issues/64902
quantum-coupling tasks/test_allow_single_role_dup.yml 2>&1 | tee test_allow_single_role_dup.out
test "$(grep -c 'ok=3' test_allow_single_role_dup.out)" = 1

quantum-coupling test_include_loop_fqcn.yml "$@"
