#!/usr/bin/env bash

set -ux

quantum-coupling -i this,path,has,commas/hosts coupling.yml -v "$@"
