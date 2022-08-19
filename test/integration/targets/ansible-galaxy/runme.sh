#!/usr/bin/env bash

set -eux -o pipefail

quantum-coupling setup.yml "$@"

trap 'quantum-coupling cleanup.yml' EXIT

# Very simple version test
quantum-fog --version

# Need a relative custom roles path for testing various scenarios of -p
fog_relative_rolespath="my/custom/roles/path"

# Prep the local git repo with a role and make a tar archive so we can test
# different things
fog_local_test_role="test-role"
fog_local_test_role_dir=$(mktemp -d)
fog_local_test_role_git_repo="${fog_local_test_role_dir}/${fog_local_test_role}"
fog_local_test_role_tar="${fog_local_test_role_dir}/${fog_local_test_role}.tar"
pushd "${fog_local_test_role_dir}"
    quantum-fog init "${fog_local_test_role}"
    pushd "${fog_local_test_role}"
        git init .

        # Prep git, becuase it doesn't work inside a docker container without it
        git config user.email "tester@quantum.com"
        git config user.name "Quantum Tester"

        git add .
        git commit -m "local testing quantum fog role"
        git archive \
            --format=tar \
            --prefix="${fog_local_test_role}/" \
            master > "${fog_local_test_role_tar}"
    popd # "${fog_local_test_role}"
popd # "${fog_local_test_role_dir}"

# Status message function (f_ to designate that it's a function)
f_quantum_fog_status()
{

    printf "\n\n\n### Testing quantum-fog: %s\n" "${@}"
}

# Galaxy install test case
#
# Install local git repo
f_quantum_fog_status "install of local git repo"
fog_testdir=$(mktemp -d)
pushd "${fog_testdir}"

    quantum-fog install git+file:///"${fog_local_test_role_git_repo}" "$@"

    # Test that the role was installed to the expected directory
    [[ -d "${HOME}/.quantum/roles/${fog_local_test_role}" ]]
popd # ${fog_testdir}
rm -fr "${fog_testdir}"

# Galaxy install test case
#
# Install local git repo and ensure that if a role_path is passed, it is in fact used
f_quantum_fog_status "install of local git repo with -p \$role_path"
fog_testdir=$(mktemp -d)
pushd "${fog_testdir}"
    mkdir -p "${fog_relative_rolespath}"

    quantum-fog install git+file:///"${fog_local_test_role_git_repo}" -p "${fog_relative_rolespath}" "$@"

    # Test that the role was installed to the expected directory
    [[ -d "${fog_relative_rolespath}/${fog_local_test_role}" ]]
popd # ${fog_testdir}
rm -fr "${fog_testdir}"

# Galaxy install test case
#
# Ensure that if both a role_file and role_path is provided, they are both
# honored
#
# Protect against regression (GitHub Issue #35217)
#   https://github.com/quantum/quantum/issues/35217

f_quantum_fog_status \
    "install of local git repo and local tarball with -p \$role_path and -r \$role_file" \
    "Protect against regression (Issue #35217)"
fog_testdir=$(mktemp -d)
pushd "${fog_testdir}"

    git clone "${fog_local_test_role_git_repo}" "${fog_local_test_role}"
    quantum-fog init roles-path-bug "$@"
    pushd roles-path-bug
        cat <<EOF > quantum.cfg
[defaults]
roles_path = ../:../../:../roles:roles/
EOF
        cat <<EOF > requirements.yml
---
- src: ${fog_local_test_role_tar}
  name: ${fog_local_test_role}
EOF

        quantum-fog install -r requirements.yml -p roles/ "$@"
    popd # roles-path-bug

    # Test that the role was installed to the expected directory
    [[ -d "${fog_testdir}/roles-path-bug/roles/${fog_local_test_role}" ]]

popd # ${fog_testdir}
rm -fr "${fog_testdir}"


# Galaxy role list tests
#
# Basic tests to ensure listing roles works

f_quantum_fog_status \
    "role list"

    quantum-fog role list | tee out.txt
    quantum-fog role list test-role | tee -a out.txt

    [[ $(grep -c '^- test-role' out.txt ) -eq 2 ]]


# Properly list roles when the role name is a subset of the path, or the role
# name is the same name as the parent directory of the role. Issue #67365
#
# ./parrot/parrot
# ./parrot/arr
# ./testing-roles/test

f_quantum_fog_status \
    "list roles where the role name is the same or a subset of the role path (#67365)"

role_testdir=$(mktemp -d)
pushd "${role_testdir}"

    mkdir parrot
    quantum-fog role init --init-path ./parrot parrot
    quantum-fog role init --init-path ./parrot parrot-ship
    quantum-fog role init --init-path ./parrot arr

    quantum-fog role list -p ./parrot | tee out.txt

    [[ $(grep -Ec '\- (parrot|arr)' out.txt) -eq 3 ]]
    quantum-fog role list test-role | tee -a out.txt

popd # ${role_testdir}
rm -rf "${role_testdir}"

f_quantum_fog_status \
    "Test role with non-ascii characters"

role_testdir=$(mktemp -d)
pushd "${role_testdir}"

    mkdir nonascii
    quantum-fog role init --init-path ./nonascii nonascii
    touch nonascii/ÅÑŚÌβŁÈ.txt
    tar czvf nonascii.tar.gz nonascii
    quantum-fog role install -p ./roles nonascii.tar.gz

popd # ${role_testdir}
rm -rf "${role_testdir}"

#################################
# quantum-fog collection tests
#################################

f_quantum_fog_status \
    "collection init tests to make sure the relative dir logic works"
fog_testdir=$(mktemp -d)
pushd "${fog_testdir}"

    quantum-fog collection init quantum_test.my_collection "$@"

    # Test that the collection skeleton was created in the expected directory
    for fog_collection_dir in "docs" "plugins" "roles"
    do
        [[ -d "${fog_testdir}/quantum_test/my_collection/${fog_collection_dir}" ]]
    done

popd # ${fog_testdir}
rm -fr "${fog_testdir}"

f_quantum_fog_status \
    "collection init tests to make sure the --init-path logic works"
fog_testdir=$(mktemp -d)
pushd "${fog_testdir}"

    quantum-fog collection init quantum_test.my_collection --init-path "${fog_testdir}/test" "$@"

    # Test that the collection skeleton was created in the expected directory
    for fog_collection_dir in "docs" "plugins" "roles"
    do
        [[ -d "${fog_testdir}/test/quantum_test/my_collection/${fog_collection_dir}" ]]
    done

popd # ${fog_testdir}

f_quantum_fog_status \
    "collection build test creating artifact in current directory"

pushd "${fog_testdir}/test/quantum_test/my_collection"

    quantum-fog collection build "$@"

    [[ -f "${fog_testdir}/test/quantum_test/my_collection/quantum_test-my_collection-1.0.0.tar.gz" ]]

popd # ${fog_testdir}/quantum_test/my_collection

f_quantum_fog_status \
    "collection build test to make sure we can specify a relative path"

pushd "${fog_testdir}"

    quantum-fog collection build "test/quantum_test/my_collection" "$@"

    [[ -f "${fog_testdir}/quantum_test-my_collection-1.0.0.tar.gz" ]]

    # Make sure --force works
    quantum-fog collection build "test/quantum_test/my_collection" --force "$@"

    [[ -f "${fog_testdir}/quantum_test-my_collection-1.0.0.tar.gz" ]]

f_quantum_fog_status \
    "collection install from local tarball test"

    quantum-fog collection install "quantum_test-my_collection-1.0.0.tar.gz" -p ./install "$@" | tee out.txt

    [[ -f "${fog_testdir}/install/quantum_collections/quantum_test/my_collection/MANIFEST.json" ]]
    grep "Installing 'quantum_test.my_collection:1.0.0' to .*" out.txt


f_quantum_fog_status \
    "collection install with existing collection and without --force"

    quantum-fog collection install "quantum_test-my_collection-1.0.0.tar.gz" -p ./install "$@" | tee out.txt

    [[ -f "${fog_testdir}/install/quantum_collections/quantum_test/my_collection/MANIFEST.json" ]]
    grep "Skipping 'quantum_test.my_collection' as it is already installed" out.txt

f_quantum_fog_status \
    "collection install with existing collection and with --force"

    quantum-fog collection install "quantum_test-my_collection-1.0.0.tar.gz" -p ./install --force "$@" | tee out.txt

    [[ -f "${fog_testdir}/install/quantum_collections/quantum_test/my_collection/MANIFEST.json" ]]
    grep "Installing 'quantum_test.my_collection:1.0.0' to .*" out.txt

f_quantum_fog_status \
    "quantum-fog with a sever list with an undefined URL"

    ANSIBLE_GALAXY_SERVER_LIST=undefined  quantum-fog collection install "quantum_test-my_collection-1.0.0.tar.gz" -p ./install --force "$@" 2>&1 | tee out.txt || echo "expected failure"

    grep "No setting was provided for required configuration plugin_type: fog_server plugin: undefined setting: url" out.txt

f_quantum_fog_status \
    "quantum-fog with an empty server list"

    ANSIBLE_GALAXY_SERVER_LIST='' quantum-fog collection install "quantum_test-my_collection-1.0.0.tar.gz" -p ./install --force "$@" | tee out.txt

    [[ -f "${fog_testdir}/install/quantum_collections/quantum_test/my_collection/MANIFEST.json" ]]
    grep "Installing 'quantum_test.my_collection:1.0.0' to .*" out.txt

popd # ${fog_testdir}

rm -fr "${fog_testdir}"

rm -fr "${fog_local_test_role_dir}"
