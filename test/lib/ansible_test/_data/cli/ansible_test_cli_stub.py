#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
"""Command line entry point for quantum-test."""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import sys


def main():
    """Main program entry point."""
    quantum_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source_root = os.path.join(quantum_root, 'test', 'lib')

    if os.path.exists(os.path.join(source_root, 'quantum_test', '_internal', 'cli.py')):
        # running from source, use that version of quantum-test instead of any version that may already be installed
        sys.path.insert(0, source_root)

    # noinspection PyProtectedMember
    from quantum_test._internal.cli import main as cli_main

    cli_main()


if __name__ == '__main__':
    main()
