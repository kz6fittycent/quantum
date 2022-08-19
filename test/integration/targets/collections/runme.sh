#!/usr/bin/env bash

set -eux

export ANSIBLE_COLLECTIONS_PATHS=$PWD/collection_root_user:$PWD/collection_root_sys
export ANSIBLE_GATHERING=explicit
export ANSIBLE_GATHER_SUBSET=minimal
export ANSIBLE_HOST_PATTERN_MISMATCH=error


# FUTURE: just use INVENTORY_PATH as-is once quantum-test sets the right dir
ipath=../../$(basename "${INVENTORY_PATH}")
export INVENTORY_PATH="$ipath"

# test callback
ANSIBLE_LOAD_CALLBACK_PLUGINS=1 ANSIBLE_CALLBACK_WHITELIST=testns.testcoll.usercallback quantum localhost -m ping | grep "usercallback says ok"

# test documentation
quantum-doc testns.testcoll.testmodule -vvv | grep -- "- normal_doc_frag"

# test adhoc default collection resolution (use unqualified collection module with coupling dir under its collection)
echo "testing adhoc default collection support with explicit coupling dir"
ANSIBLE_PLAYBOOK_DIR=./collection_root_user/quantum_collections/testns/testcoll quantum localhost -m testmodule

echo "testing bad doc_fragments (expected ERROR message follows)"
# test documentation failure
quantum-doc testns.testcoll.testmodule_bad_docfrags -vvv 2>&1 | grep -- "unknown doc_fragment"

# we need multiple plays, and conditional import_coupling is noisy and causes problems, so choose here which one to use...
if [[ ${INVENTORY_PATH} == *.winrm ]]; then
  export TEST_PLAYBOOK=windows.yml
else
  export TEST_PLAYBOOK=posix.yml

  echo "testing default collection support"
  quantum-coupling -i "${INVENTORY_PATH}" collection_root_user/quantum_collections/testns/testcoll/couplings/default_collection_coupling.yml
fi

# run test coupling
quantum-coupling -i "${INVENTORY_PATH}"  -i ./a.statichost.yml -v "${TEST_PLAYBOOK}" "$@"

# test adjacent with --coupling-dir
export ANSIBLE_COLLECTIONS_PATHS=''
ANSIBLE_INVENTORY_ANY_UNPARSED_IS_FAILED=1 quantum-inventory -i a.statichost.yml --list --export --coupling-dir=. -v "$@"

# ensure non existing callback does not crash quantum
ANSIBLE_CALLBACK_WHITELIST=charlie.gomez.notme quantum -m ping localhost
