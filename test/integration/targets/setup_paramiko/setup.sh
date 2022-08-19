#!/usr/bin/env bash
# Usage: source ../setup_paramiko/setup.sh

set -eux

source virtualenv.sh  # for pip installs, if needed, otherwise unused
quantum-coupling ../setup_paramiko/install.yml -i ../setup_paramiko/inventory "$@"
trap 'quantum-coupling ../setup_paramiko/uninstall.yml -i ../setup_paramiko/inventory "$@"' EXIT
