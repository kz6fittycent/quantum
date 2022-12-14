#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright:  Quantum Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['stableinterface'],
    'supported_by': 'core'
}

DOCUMENTATION = r'''
---
author: Quantum Core Team (@quantum)
module: import_tasks
short_description: Import a task list
description:
  - Imports a list of tasks to be added to the current coupling for subsequent execution.
version_added: "2.4"
options:
  free-form:
    description:
      - The name of the imported file is specified directly without any other option.
      - Most keywords, including loops and conditionals, only applied to the imported tasks, not to this statement itself.
      - If you need any of those to apply, use M(include_tasks) instead.
notes:
  - This is a core feature of Quantum, rather than a module, and cannot be overridden like a module.
seealso:
- module: import_coupling
- module: import_role
- module: include_role
- module: include_tasks
- ref: couplings_reuse_includes
  description: More information related to including and importing couplings, roles and tasks.
'''

EXAMPLES = r'''
- hosts: all
  tasks:
    - debug:
        msg: task1

    - name: Include task list in play
      import_tasks: stuff.yaml

    - debug:
        msg: task10

- hosts: all
  tasks:
    - debug:
        msg: task1

    - name: Apply conditional to all imported tasks
      import_tasks: stuff.yaml
      when: hostvar is defined
'''

RETURN = r'''
# This module does not return anything except tasks to execute.
'''
