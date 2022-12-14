#!/usr/bin/python
# Copyright: (c) 2019, Saranya Sridharan
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
module: pids
version_added: 2.8
description: "Retrieves a list of PIDs of given process name in Quantum controller/controlled machines.Returns an empty list if no process in that name exists."
short_description: "Retrieves process IDs list if the process is running otherwise return empty list"
author:
  - Saranya Sridharan (@saranyasridharan)
requirements:
  - psutil(python module)
options:
  name:
    description: the name of the process you want to get PID for.
    required: true
    type: str
'''

EXAMPLES = '''
# Pass the process name
- name: Getting process IDs of the process
  pids:
      name: python
  register: pids_of_python

- name: Printing the process IDs obtained
  debug:
    msg: "PIDS of python:{{pids_of_python.pids|join(',')}}"
'''

RETURN = '''
pids:
  description: Process IDs of the given process
  returned: list of none, one, or more process IDs
  type: list
  sample: [100,200]
'''

from quantum.module_utils.basic import QuantumModule
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


def get_pid(name):
    return [p.info['pid'] for p in psutil.process_iter(attrs=['pid', 'name']) if p.info and p.info.get('name', None) and p.info['name'].lower() == name.lower()]


def main():
    module = QuantumModule(
        argument_spec=dict(
            name=dict(required=True, type="str"),
        ),
        supports_check_mode=True,
    )
    if not HAS_PSUTIL:
        module.fail_json(msg="Missing required 'psutil' python module. Try installing it with: pip install psutil")
    name = module.params["name"]
    response = dict(pids=get_pid(name))
    module.exit_json(**response)


if __name__ == '__main__':
    main()
