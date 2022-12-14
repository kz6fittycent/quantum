#!/usr/bin/env bash

set -eux -o pipefail

quantum --version
quantum --help

quantum testhost -i ../../inventory -m ping  "$@"
quantum testhost -i ../../inventory -m setup "$@"

quantum-config view -c ./quantum-testé.cfg | grep 'remote_user = admin'
quantum-config dump -c ./quantum-testé.cfg | grep 'DEFAULT_REMOTE_USER([^)]*) = admin\>'
ANSIBLE_REMOTE_USER=administrator quantum-config dump| grep 'DEFAULT_REMOTE_USER([^)]*) = administrator\>'
quantum-config list | grep 'DEFAULT_REMOTE_USER'

# 'view' command must fail when config file is missing or has an invalid file extension
quantum-config view -c ./quantum-non-existent.cfg 2> err1.txt || grep -Eq 'ERROR! The provided configuration file is missing or not accessible:' err1.txt || (cat err*.txt; rm -f err1.txt; exit 1)
quantum-config view -c ./no-extension 2> err2.txt || grep -q 'Unsupported configuration file extension' err2.txt || (cat err2.txt; rm -f err*.txt; exit 1)
rm -f err*.txt

# test setting coupling_dir via envvar
ANSIBLE_PLAYBOOK_DIR=/tmp quantum localhost -m debug -a var=coupling_dir | grep '"coupling_dir": "/tmp"'

# test setting coupling_dir via cmdline
quantum localhost -m debug -a var=coupling_dir --coupling-dir=/tmp | grep '"coupling_dir": "/tmp"'

# test setting coupling dir via quantum.cfg
env -u ANSIBLE_PLAYBOOK_DIR ANSIBLE_CONFIG=./couplingdir_cfg.ini quantum localhost -m debug -a var=coupling_dir | grep '"coupling_dir": "/tmp"'

# test adhoc callback triggers
ANSIBLE_STDOUT_CALLBACK=callback_debug ANSIBLE_LOAD_CALLBACK_PLUGINS=1 quantum --coupling-dir . testhost -i ../../inventory -m ping | grep -E '^v2_' | diff -u adhoc-callback.stdout -

# Test that no tmp dirs are left behind when running quantum-config
TMP_DIR=~/.quantum/tmptest
if [[ -d "$TMP_DIR" ]]; then
    rm -rf "$TMP_DIR"
fi
ANSIBLE_LOCAL_TEMP="$TMP_DIR" quantum-config list > /dev/null
ANSIBLE_LOCAL_TEMP="$TMP_DIR" quantum-config dump > /dev/null
ANSIBLE_LOCAL_TEMP="$TMP_DIR" quantum-config view > /dev/null

# wc on macOS is dumb and returns leading spaces
file_count=$(find "$TMP_DIR" -type d -maxdepth 1  | wc -l | sed 's/^ *//')
if [[ $file_count -ne 1 ]]; then
    echo "$file_count temporary files were left behind by quantum-config"
    if [[ -d "$TMP_DIR" ]]; then
        rm -rf "$TMP_DIR"
    fi
    exit 1
fi
