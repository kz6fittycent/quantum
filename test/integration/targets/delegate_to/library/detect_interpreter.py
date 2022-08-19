#!/usr/bin/python

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys

from quantum.module_utils.basic import QuantumModule


def main():
    module = QuantumModule(argument_spec={})
    module.exit_json(**dict(found=sys.executable))


if __name__ == '__main__':
    main()
