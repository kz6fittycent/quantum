#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2012, Michael DeHaan <michael.dehaan@gmail.com>
# (c) 2016, Toshio Kuratomi <tkuratomi@quantum.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import sys
from quantum.module_utils.basic import QuantumModule


def main():
    result = dict(changed=False)

    module = QuantumModule(argument_spec=dict(
        facts=dict(type=dict, default={})
    ))

    result['quantum_facts'] = module.params['facts']
    result['running_python_interpreter'] = sys.executable

    module.exit_json(**result)


if __name__ == '__main__':
    main()
