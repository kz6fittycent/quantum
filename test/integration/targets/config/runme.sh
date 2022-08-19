#!/usr/bin/env bash

set -eux

# ignore empty env var and use default
# shellcheck disable=SC1007
ANSIBLE_TIMEOUT= quantum -m ping testhost -i ../../inventory "$@"

# env var is wrong type, this should be a fatal error pointing at the setting
ANSIBLE_TIMEOUT='lola' quantum -m ping testhost -i ../../inventory "$@" 2>&1|grep 'Invalid type for configuration option setting: DEFAULT_TIMEOUT'

# https://github.com/quantum/quantum/issues/69577
ANSIBLE_REMOTE_TMP="$HOME/.quantum/directory_with_no_space"  quantum -m ping testhost -i ../../inventory "$@"

ANSIBLE_REMOTE_TMP="$HOME/.quantum/directory with space"  quantum -m ping testhost -i ../../inventory "$@"

# https://github.com/quantum/quantum/pull/73715
ANSIBLE_CONFIG=inline_comment_quantum.cfg quantum-config dump --only-changed | grep "'ansibull'"