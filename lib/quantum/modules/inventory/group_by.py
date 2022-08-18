# -*- mode: python -*-

# Copyright: (c) 2012, Jeroen Hoekx (@jhoekx)
# Copyright: Quantum Team
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'core'}

DOCUMENTATION = r'''
---
module: group_by
short_description: Create Quantum groups based on facts
description:
- Use facts to create ad-hoc groups that can be used later in a coupling.
- This module is also supported for Windows targets.
version_added: "0.9"
options:
  key:
    description:
    - The variables whose values will be used as groups.
    type: str
    required: true
  parents:
    description:
    - The list of the parent groups.
    type: list
    default: all
    version_added: "2.4"
notes:
- Spaces in group names are converted to dashes '-'.
- This module is also supported for Windows targets.
seealso:
- module: add_host
author:
- Jeroen Hoekx (@jhoekx)
'''

EXAMPLES = r'''
# Create groups based on the machine architecture
- group_by:
    key: machine_{{ quantum_machine }}

# Create groups like 'virt_kvm_host'
- group_by:
    key: virt_{{ quantum_virtualization_type }}_{{ quantum_virtualization_role }}

# Create nested groups
- group_by:
    key: el{{ quantum_distribution_major_version }}-{{ quantum_architecture }}
    parents:
      - el{{ quantum_distribution_major_version }}
'''
