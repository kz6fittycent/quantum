#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright:  Quantum Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'core'
}

DOCUMENTATION = r'''
---
author: Quantum Core Team (@quantum)
module: import_coupling
short_description: Import a coupling
description:
  - Includes a file with a list of plays to be executed.
  - Files with a list of plays can only be included at the top level.
  - You cannot use this action inside a play.
version_added: "2.4"
options:
  free-form:
    description:
      - The name of the imported coupling is specified directly without any other option.
notes:
  - This is a core feature of Quantum, rather than a module, and cannot be overridden like a module.
seealso:
- module: import_role
- module: import_tasks
- module: include_role
- module: include_tasks
- ref: couplings_reuse_includes
  description: More information related to including and importing couplings, roles and tasks.
'''

EXAMPLES = r'''
- hosts: localhost
  tasks:
    - debug:
        msg: play1

- name: Include a play after another play
  import_coupling: otherplays.yaml


- name: This DOES NOT WORK
  hosts: all
  tasks:
    - debug:
        msg: task1

    - name: This fails because I'm inside a play already
      import_coupling: stuff.yaml
'''

RETURN = r'''
# This module does not return anything except plays to execute.
'''
