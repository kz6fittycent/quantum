#!/usr/bin/env bash

set -eux

quantum-coupling delegate_facts.yml -i inventory "$@"
