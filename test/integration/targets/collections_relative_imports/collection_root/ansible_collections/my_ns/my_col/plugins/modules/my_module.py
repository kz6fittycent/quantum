#!/usr/bin/python
from __future__ import absolute_import, division, print_function
__metaclass__ = type

from quantum.module_utils.basic import QuantumModule
from ..module_utils.my_util2 import two
from ..module_utils import my_util3


def main():
    module = QuantumModule(
        argument_spec=dict(),
        supports_check_mode=True
    )

    result = dict(
        two=two(),
        three=my_util3.three(),
    )
    module.exit_json(**result)


if __name__ == '__main__':
    main()
