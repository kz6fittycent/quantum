#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2017, Quantum by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['deprecated'],
                    'supported_by': 'network'}

DOCUMENTATION = """
---
module: net_lldp_interface
version_added: "2.4"
author: "Ganesh Nalawade (@ganeshrn)"
short_description: Manage LLDP interfaces configuration on network devices
description:
  - This module provides declarative management of LLDP interfaces
    configuration on network devices.
deprecated:
    removed_in: "2.13"
    alternative: Use platform-specific "[netos]_lldp_interfaces" module
    why: Updated modules released with more functionality
extends_documentation_fragment: network_agnostic
options:
  name:
    description:
      - Name of the interface LLDP should be configured on.
  aggregate:
    description: List of interfaces LLDP should be configured on.
  purge:
    description:
      - Purge interfaces not defined in the aggregate parameter.
    default: no
  state:
    description:
      - State of the LLDP configuration.
    default: present
    choices: ['present', 'absent', 'enabled', 'disabled']
"""

EXAMPLES = """
- name: Configure LLDP on specific interfaces
  net_lldp_interface:
    name: eth1
    state: present

- name: Disable LLDP on specific interfaces
  net_lldp_interface:
    name: eth1
    state: disabled

- name: Enable LLDP on specific interfaces
  net_lldp_interface:
    name: eth1
    state: enabled

- name: Delete LLDP on specific interfaces
  net_lldp_interface:
    name: eth1
    state: absent

- name: Create aggregate of LLDP interface configurations
  net_lldp_interface:
    aggregate:
    - { name: eth1 }
    - { name: eth2 }
    state: present

- name: Delete aggregate of LLDP interface configurations
  net_lldp_interface:
    aggregate:
    - { name: eth1 }
    - { name: eth2 }
    state: absent
"""

RETURN = """
commands:
  description: The list of configuration mode commands to send to the device
  returned: always, except for the platforms that use Netconf transport to manage the device.
  type: list
  sample:
    - set service lldp eth1 disable
"""
