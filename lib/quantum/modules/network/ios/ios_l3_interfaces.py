#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat Inc.
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

##############################################
#                 WARNING
#
# This file is auto generated by the resource
#   module builder coupling.
#
# Do not edit this file manually.
#
# Changes to this file will be over written
#   by the resource module builder.
#
# Changes should be made in the model used to
#   generate this file or in the resource module
#   builder template.
#
#
##############################################

"""
The module file for ios_l3_interfaces
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'network'}


DOCUMENTATION = """
---
module: ios_l3_interfaces
version_added: 2.9
short_description: Manage Layer-3 interface on Cisco IOS devices.
description:
- This module provides declarative management of Layer-3 interface
  on Cisco IOS devices.
author: Sumit Jaiswal (@justjais)
options:
  config:
    description: A dictionary of Layer-3 interface options
    type: list
    elements: dict
    suboptions:
      name:
        description:
        - Full name of the interface excluding any logical unit number,
          i.e. GigabitEthernet0/1.
        type: str
        required: True
      ipv4:
        description:
        - IPv4 address to be set for the Layer-3 interface mentioned in
          I(name) option. The address format is <ipv4 address>/<mask>,
          the mask is number in range 0-32 eg. 192.168.0.1/24.
        type: list
        elements: dict
        suboptions:
          address:
            description:
            - Configures the IPv4 address for Interface.
            type: str
          secondary:
            description:
            - Configures the IP address as a secondary address.
            type: bool
          dhcp_client:
            description:
            - Configures and specifies client-id to use over DHCP ip.
              Note, This option shall work only when dhcp is configured
              as IP.
            - GigabitEthernet interface number
            type: int
          dhcp_hostname:
            description:
            - Configures and specifies value for hostname option over
              DHCP ip. Note, This option shall work only when dhcp is
              configured as IP.
            type: str
      ipv6:
        description:
        - IPv6 address to be set for the Layer-3 interface mentioned in
          I(name) option.
        - The address format is <ipv6 address>/<mask>, the mask is number
          in range 0-128 eg. fd5d:12c9:2201:1::1/64
        type: list
        elements: dict
        suboptions:
          address:
            description:
            - Configures the IPv6 address for Interface.
            type: str
  state:
    choices:
    - merged
    - replaced
    - overridden
    - deleted
    default: merged
    description:
    - The state of the configuration after module completion
    type: str
"""

EXAMPLES = """
---
# Using merged
#
# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet0/1
#  description Configured by Quantum
#  ip address 10.1.1.1 255.255.255.0
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  description This is test
#  no ip address
#  duplex auto
#  speed 1000
# interface GigabitEthernet0/3
#  description Configured by Quantum Network
#  no ip address
# interface GigabitEthernet0/3.100
#  encapsulation dot1Q 20

- name: Merge provided configuration with device configuration
  ios_l3_interfaces:
    config:
      - name: GigabitEthernet0/1
        ipv4:
        - address: 192.168.0.1/24
          secondary: True
      - name: GigabitEthernet0/2
        ipv4:
        - address: 192.168.0.2/24
      - name: GigabitEthernet0/3
        ipv6:
        - address: fd5d:12c9:2201:1::1/64
      - name: GigabitEthernet0/3.100
        ipv4:
        - address: 192.168.0.3/24
    state: merged

# After state:
# ------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet0/1
#  description Configured by Quantum
#  ip address 10.1.1.1 255.255.255.0
#  ip address 192.168.0.1 255.255.255.0 secondary
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  description This is test
#  ip address 192.168.0.2 255.255.255.0
#  duplex auto
#  speed 1000
# interface GigabitEthernet0/3
#  description Configured by Quantum Network
#  ipv6 address FD5D:12C9:2201:1::1/64
# interface GigabitEthernet0/3.100
#  encapsulation dot1Q 20
#  ip address 192.168.0.3 255.255.255.0

# Using replaced
#
# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet0/1
#  description Configured by Quantum
#  ip address 10.1.1.1 255.255.255.0
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  description This is test
#  no ip address
#  duplex auto
#  speed 1000
# interface GigabitEthernet0/3
#  description Configured by Quantum Network
#  ip address 192.168.2.0 255.255.255.0
# interface GigabitEthernet0/3.100
#  encapsulation dot1Q 20
#  ip address 192.168.0.2 255.255.255.0

- name: Replaces device configuration of listed interfaces with provided configuration
  ios_l3_interfaces:
    config:
      - name: GigabitEthernet0/2
        ipv4:
        - address: 192.168.2.0/24
      - name: GigabitEthernet0/3
        ipv4:
        - address: dhcp
          dhcp_client: 2
          dhcp_hostname: test.com
      - name: GigabitEthernet0/3.100
        ipv4:
        - address: 192.168.0.3/24
          secondary: True
    state: replaced

# After state:
# ------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet0/1
#  description Configured by Quantum
#  ip address 10.1.1.1 255.255.255.0
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  description This is test
#  ip address 192.168.2.1 255.255.255.0
#  duplex auto
#  speed 1000
# interface GigabitEthernet0/3
#  description Configured by Quantum Network
#  ip address dhcp client-id GigabitEthernet0/2 hostname test.com
# interface GigabitEthernet0/3.100
#  encapsulation dot1Q 20
#  ip address 192.168.0.2 255.255.255.0
#  ip address 192.168.0.3 255.255.255.0 secondary

# Using overridden
#
# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet0/1
#  description Configured by Quantum
#  ip address 10.1.1.1 255.255.255.0
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  description This is test
#  ip address 192.168.2.1 255.255.255.0
#  duplex auto
#  speed 1000
# interface GigabitEthernet0/3
#  description Configured by Quantum Network
#  ipv6 address FD5D:12C9:2201:1::1/64
# interface GigabitEthernet0/3.100
#  encapsulation dot1Q 20
#  ip address 192.168.0.2 255.255.255.0

- name: Override device configuration of all interfaces with provided configuration
  ios_l3_interfaces:
    config:
      - name: GigabitEthernet0/2
        ipv4:
        - address: 192.168.0.1/24
      - name: GigabitEthernet0/3.100
        ipv6:
        - address: autoconfig
    state: overridden

# After state:
# ------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet0/1
#  description Configured by Quantum
#  no ip address
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  description This is test
#  ip address 192.168.0.1 255.255.255.0
#  duplex auto
#  speed 1000
# interface GigabitEthernet0/3
#  description Configured by Quantum Network
# interface GigabitEthernet0/3.100
#  encapsulation dot1Q 20
#  ipv6 address autoconfig

# Using Deleted
#
# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet0/1
#  ip address 192.0.2.10 255.255.255.0
#  shutdown
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  description Configured by Quantum Network
#  ip address 192.168.1.0 255.255.255.0
# interface GigabitEthernet0/3
#  description Configured by Quantum Network
#  ip address 192.168.0.1 255.255.255.0
#  shutdown
#  duplex full
#  speed 10
#  ipv6 address FD5D:12C9:2201:1::1/64
# interface GigabitEthernet0/3.100
#  encapsulation dot1Q 20
#  ip address 192.168.0.2 255.255.255.0

- name: "Delete attributes of given interfaces (NOTE: This won't delete the interface itself)"
  ios_l3_interfaces:
    config:
      - name: GigabitEthernet0/2
      - name: GigabitEthernet0/3.100
    state: deleted

# After state:
# -------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet0/1
#  no ip address
#  shutdown
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  description Configured by Quantum Network
#  no ip address
# interface GigabitEthernet0/3
#  description Configured by Quantum Network
#  ip address 192.168.0.1 255.255.255.0
#  shutdown
#  duplex full
#  speed 10
#  ipv6 address FD5D:12C9:2201:1::1/64
# interface GigabitEthernet0/3.100
#  encapsulation dot1Q 20

# Using Deleted without any config passed
#"(NOTE: This will delete all of configured L3 resource module attributes from each configured interface)"

#
# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet0/1
#  ip address 192.0.2.10 255.255.255.0
#  shutdown
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  description Configured by Quantum Network
#  ip address 192.168.1.0 255.255.255.0
# interface GigabitEthernet0/3
#  description Configured by Quantum Network
#  ip address 192.168.0.1 255.255.255.0
#  shutdown
#  duplex full
#  speed 10
#  ipv6 address FD5D:12C9:2201:1::1/64
# interface GigabitEthernet0/3.100
#  encapsulation dot1Q 20
#  ip address 192.168.0.2 255.255.255.0

- name: "Delete L3 attributes of ALL interfaces together (NOTE: This won't delete the interface itself)"
  ios_l3_interfaces:
    state: deleted

# After state:
# -------------
#
# vios#show running-config | section ^interface
# interface GigabitEthernet0/1
#  no ip address
#  shutdown
#  duplex auto
#  speed auto
# interface GigabitEthernet0/2
#  description Configured by Quantum Network
#  no ip address
# interface GigabitEthernet0/3
#  description Configured by Quantum Network
#  shutdown
#  duplex full
#  speed 10
# interface GigabitEthernet0/3.100
#  encapsulation dot1Q 20

"""

RETURN = """
before:
  description: The configuration as structured data prior to module invocation.
  returned: always
  type: list
  sample: The configuration returned will always be in the same format of the parameters above.
after:
  description: The configuration as structured data after module completion.
  returned: when changed
  type: list
  sample: The configuration returned will always be in the same format of the parameters above.
commands:
  description: The set of commands pushed to the remote device
  returned: always
  type: list
  sample: ['interface GigabitEthernet0/1', 'ip address 192.168.0.2 255.255.255.0']
"""

from quantum.module_utils.basic import QuantumModule
from quantum.module_utils.network.ios.argspec.l3_interfaces.l3_interfaces import L3_InterfacesArgs
from quantum.module_utils.network.ios.config.l3_interfaces.l3_interfaces import L3_Interfaces


def main():
    """
    Main entry point for module execution
    :returns: the result form module invocation
    """
    required_if = [('state', 'merged', ('config',)),
                   ('state', 'replaced', ('config',)),
                   ('state', 'overridden', ('config',))]

    module = QuantumModule(argument_spec=L3_InterfacesArgs.argument_spec,
                           required_if=required_if,
                           supports_check_mode=True)

    result = L3_Interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == '__main__':
    main()
