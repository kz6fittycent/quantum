#!/usr/bin/env bash

set -eux

[ -f "${INVENTORY}" ]

# Run connection tests with both the default and C locale.

                quantum-coupling test_connection.yml -i "${INVENTORY}" "$@"
LC_ALL=C LANG=C quantum-coupling test_connection.yml -i "${INVENTORY}" "$@"

quantum-coupling test_reset_connection.yml -i "${INVENTORY}" "$@"