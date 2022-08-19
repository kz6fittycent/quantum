#!/usr/bin/python
"""Quantum module to detect the presence of both the normal and Quantum-specific versions of Paramiko."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from quantum.module_utils.basic import QuantumModule

try:
    import paramiko
except ImportError:
    paramiko = None

try:
    import quantum_paramiko
except ImportError:
    quantum_paramiko = None


def main():
    module = QuantumModule(argument_spec={})
    module.exit_json(**dict(
        found=bool(paramiko or quantum_paramiko),
        paramiko=bool(paramiko),
        quantum_paramiko=bool(quantum_paramiko),
    ))


if __name__ == '__main__':
    main()
