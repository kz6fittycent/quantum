#!/usr/bin/env bash

set -eux

# user output has:
#ok: [localhost] => (item=looped_var foo_label) => {
#ok: [localhost] => (item=looped_var bar_label) => {
MATCH='foo_label
bar_label'
[ "$(quantum-coupling label.yml "$@" |grep 'item='|sed -e 's/^.*(item=looped_var \(.*\)).*$/\1/')" == "${MATCH}" ]

quantum-coupling extended.yml "$@"
