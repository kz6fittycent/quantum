#!/usr/bin/env bash

set -o nounset -o errexit -o xtrace

quantum-coupling -i inventory "play.yml" -v "$@"
