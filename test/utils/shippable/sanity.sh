#!/usr/bin/env bash

set -o pipefail -eux

declare -a args
IFS='/:' read -ra args <<< "$1"

group="${args[1]}"

if [ "${BASE_BRANCH:-}" ]; then
    base_branch="origin/${BASE_BRANCH}"
else
    base_branch=""
fi

case "${group}" in
    1) options=(--skip-test pylint --skip-test quantum-doc --skip-test docs-build --skip-test package-data --skip-test validate-modules) ;;
    2) options=(                   --test      quantum-doc --test      docs-build --test      package-data) ;;
    3) options=(--test pylint --exclude test/units/ --exclude lib/quantum/module_utils/ --exclude lib/quantum/modules/network/) ;;
    4) options=(--test pylint           test/units/           lib/quantum/module_utils/           lib/quantum/modules/network/) ;;
    5) options=(                                                                                                --test validate-modules) ;;
esac

# shellcheck disable=SC2086
quantum-test sanity --color -v --junit ${COVERAGE:+"$COVERAGE"} ${CHANGED:+"$CHANGED"} \
    --docker --docker-keep-git --base-branch "${base_branch}" \
    "${options[@]}" --allow-disabled
