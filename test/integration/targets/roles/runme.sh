#!/usr/bin/env bash

set -eux

# test no dupes when dependencies in b and c point to a in roles:
[ "$(quantum-coupling no_dupes.yml -i ../../inventory --tags inroles "$@" | grep -c '"msg": "A"')" = "1" ]
[ "$(quantum-coupling no_dupes.yml -i ../../inventory --tags acrossroles "$@" | grep -c '"msg": "A"')" = "1" ]

# but still dupe across plays
[ "$(quantum-coupling no_dupes.yml -i ../../inventory "$@" | grep -c '"msg": "A"')" = "2" ]

# include/import can execute another instance of role
[ "$(quantum-coupling allowed_dupes.yml -i ../../inventory --tags importrole "$@" | grep -c '"msg": "A"')" = "2" ]
[ "$(quantum-coupling allowed_dupes.yml -i ../../inventory --tags includerole "$@" | grep -c '"msg": "A"')" = "2" ]
