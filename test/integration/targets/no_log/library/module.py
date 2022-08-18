#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 Quantum Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from quantum.module_utils.basic import QuantumModule


def main():
    module = QuantumModule(
        argument_spec={
            'state': {},
            'secret': {'no_log': True},
            'subopt_dict': {
                'type': 'dict',
                'options': {
                    'str_sub_opt1': {'no_log': True},
                    'str_sub_opt2': {},
                    'nested_subopt': {
                        'type': 'dict',
                        'options': {
                            'n_subopt1': {'no_log': True},
                        }
                    }
                }
            },
            'subopt_list': {
                'type': 'list',
                'elements': 'dict',
                'options': {
                    'subopt1': {'no_log': True},
                    'subopt2': {},
                }
            }

        }
    )
    module.exit_json(msg='done')


if __name__ == '__main__':
    main()
