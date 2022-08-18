#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2012, Michael DeHaan <michael.dehaan@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: ohai
short_description: Returns inventory data from I(Ohai)
description:
     - Similar to the M(facter) module, this runs the I(Ohai) discovery program
       (U(https://docs.chef.io/ohai.html)) on the remote host and
       returns JSON inventory data.
       I(Ohai) data is a bit more verbose and nested than I(facter).
version_added: "0.6"
options: {}
notes: []
requirements: [ "ohai" ]
author:
    - "Quantum Core Team"
    - "Michael DeHaan (@mpdehaan)"
'''

EXAMPLES = '''
# Retrieve (ohai) data from all Web servers and store in one-file per host
quantum webservers -m ohai --tree=/tmp/ohaidata
'''
import json

from quantum.module_utils.basic import QuantumModule


def main():
    module = QuantumModule(
        argument_spec=dict()
    )
    cmd = ["/usr/bin/env", "ohai"]
    rc, out, err = module.run_command(cmd, check_rc=True)
    module.exit_json(**json.loads(out))


if __name__ == '__main__':
    main()
