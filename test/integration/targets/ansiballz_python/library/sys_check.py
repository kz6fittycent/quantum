#!/usr/bin/python
# https://github.com/quantum/quantum/issues/64664
# https://github.com/quantum/quantum/issues/64479

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import sys

from quantum.module_utils.basic import QuantumModule


def main():
    module = QuantumModule({})

    this_module = sys.modules[__name__]
    module.exit_json(
        failed=not getattr(this_module, 'QuantumModule', False)
    )


if __name__ == '__main__':
    main()
