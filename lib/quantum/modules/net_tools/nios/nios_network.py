#!/usr/bin/python
# Copyright (c) 2018 Red Hat, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'certified'}


DOCUMENTATION = '''
---
module: nios_network
version_added: "2.5"
author: "Peter Sprygada (@privateip)"
short_description: Configure Infoblox NIOS network object
description:
  - Adds and/or removes instances of network objects from
    Infoblox NIOS servers.  This module manages NIOS C(network) objects
    using the Infoblox WAPI interface over REST.
  - Supports both IPV4 and IPV6 internet protocols
requirements:
  - infoblox-client
extends_documentation_fragment: nios
options:
  network:
    description:
      - Specifies the network to add or remove from the system.  The value
        should use CIDR notation.
    required: true
    aliases:
      - name
      - cidr
  network_view:
    description:
      - Configures the name of the network view to associate with this
        configured instance.
    required: true
    default: default
  options:
    description:
      - Configures the set of DHCP options to be included as part of
        the configured network instance.  This argument accepts a list
        of values (see suboptions).  When configuring suboptions at
        least one of C(name) or C(num) must be specified.
    suboptions:
      name:
        description:
          - The name of the DHCP option to configure. The standard options are
            C(router), C(router-templates), C(domain-name-servers), C(domain-name),
            C(broadcast-address), C(broadcast-address-offset), C(dhcp-lease-time),
            and C(dhcp6.name-servers).
      num:
        description:
          - The number of the DHCP option to configure
      value:
        description:
          - The value of the DHCP option specified by C(name)
        required: true
      use_option:
        description:
          - Only applies to a subset of options (see NIOS API documentation)
        type: bool
        default: 'yes'
      vendor_class:
        description:
          - The name of the space this DHCP option is associated to
        default: DHCP
  extattrs:
    description:
      - Allows for the configuration of Extensible Attributes on the
        instance of the object.  This argument accepts a set of key / value
        pairs for configuration.
  comment:
    description:
      - Configures a text string comment to be associated with the instance
        of this object.  The provided text string will be configured on the
        object instance.
  container:
    description:
      - If set to true it'll create the network container to be added or removed
        from the system.
    type: bool
    version_added: '2.8'
  state:
    description:
      - Configures the intended state of the instance of the object on
        the NIOS server.  When this value is set to C(present), the object
        is configured on the device and when this value is set to C(absent)
        the value is removed (if necessary) from the device.
    default: present
    choices:
      - present
      - absent
'''

EXAMPLES = '''
- name: configure a network ipv4
  nios_network:
    network: 192.168.10.0/24
    comment: this is a test comment
    state: present
    provider:
      host: "{{ inventory_hostname_short }}"
      username: admin
      password: admin
  connection: local
- name: configure a network ipv6
  nios_network:
    network: fe80::/64
    comment: this is a test comment
    state: present
    provider:
      host: "{{ inventory_hostname_short }}"
      username: admin
      password: admin
  connection: local
- name: set dhcp options for a network ipv4
  nios_network:
    network: 192.168.10.0/24
    comment: this is a test comment
    options:
      - name: domain-name
        value: quantum.com
    state: present
    provider:
      host: "{{ inventory_hostname_short }}"
      username: admin
      password: admin
  connection: local
- name: remove a network ipv4
  nios_network:
    network: 192.168.10.0/24
    state: absent
    provider:
      host: "{{ inventory_hostname_short }}"
      username: admin
      password: admin
  connection: local
- name: configure a ipv4 network container
  nios_network:
    network: 192.168.10.0/24
    container: true
    comment: test network container
    state: present
    provider:
      host: "{{ inventory_hostname_short }}"
      username: admin
      password: admin
  connection: local
- name: configure a ipv6 network container
  nios_network:
    network: fe80::/64
    container: true
    comment: test network container
    state: present
    provider:
      host: "{{ inventory_hostname_short }}"
      username: admin
      password: admin
  connection: local
- name: remove a ipv4 network container
  nios_network:
    networkr: 192.168.10.0/24
    container: true
    comment: test network container
    state: absent
    provider:
      host: "{{ inventory_hostname_short }}"
      username: admin
      password: admin
  connection: local
'''

RETURN = ''' # '''

from quantum.module_utils.basic import QuantumModule
from quantum.module_utils.six import iteritems
from quantum.module_utils.net_tools.nios.api import WapiModule
from quantum.module_utils.network.common.utils import validate_ip_address, validate_ip_v6_address
from quantum.module_utils.net_tools.nios.api import NIOS_IPV4_NETWORK, NIOS_IPV6_NETWORK
from quantum.module_utils.net_tools.nios.api import NIOS_IPV4_NETWORK_CONTAINER, NIOS_IPV6_NETWORK_CONTAINER


def options(module):
    ''' Transforms the module argument into a valid WAPI struct
    This function will transform the options argument into a structure that
    is a valid WAPI structure in the format of:
        {
            name: <value>,
            num: <value>,
            value: <value>,
            use_option: <value>,
            vendor_class: <value>
        }
    It will remove any options that are set to None since WAPI will error on
    that condition.  It will also verify that either `name` or `num` is
    set in the structure but does not validate the values are equal.
    The remainder of the value validation is performed by WAPI
    '''
    options = list()
    for item in module.params['options']:
        opt = dict([(k, v) for k, v in iteritems(item) if v is not None])
        if 'name' not in opt and 'num' not in opt:
            module.fail_json(msg='one of `name` or `num` is required for option value')
        options.append(opt)
    return options


def check_ip_addr_type(obj_filter, ib_spec):
    '''This function will check if the argument ip is type v4/v6 and return appropriate infoblox
       network/networkcontainer type
    '''

    ip = obj_filter['network']
    if 'container' in obj_filter and obj_filter['container']:
        check_ip = ip.split('/')
        del ib_spec['container']  # removing the container key from post arguments
        del ib_spec['options']  # removing option argument as for network container it's not supported
        if validate_ip_address(check_ip[0]):
            return NIOS_IPV4_NETWORK_CONTAINER, ib_spec
        elif validate_ip_v6_address(check_ip[0]):
            return NIOS_IPV6_NETWORK_CONTAINER, ib_spec
    else:
        check_ip = ip.split('/')
        del ib_spec['container']  # removing the container key from post arguments
        if validate_ip_address(check_ip[0]):
            return NIOS_IPV4_NETWORK, ib_spec
        elif validate_ip_v6_address(check_ip[0]):
            return NIOS_IPV6_NETWORK, ib_spec


def check_vendor_specific_dhcp_option(module, ib_spec):
    '''This function will check if the argument dhcp option belongs to vendor-specific and if yes then will remove
     use_options flag which is not supported with vendor-specific dhcp options.
    '''
    for key, value in iteritems(ib_spec):
        if isinstance(module.params[key], list):
            temp_dict = module.params[key][0]
            if 'num' in temp_dict:
                if temp_dict['num'] in (43, 124, 125):
                    del module.params[key][0]['use_option']
    return ib_spec


def main():
    ''' Main entry point for module execution
    '''
    option_spec = dict(
        # one of name or num is required; enforced by the function options()
        name=dict(),
        num=dict(type='int'),

        value=dict(required=True),

        use_option=dict(type='bool', default=True),
        vendor_class=dict(default='DHCP')
    )

    ib_spec = dict(
        network=dict(required=True, aliases=['name', 'cidr'], ib_req=True),
        network_view=dict(default='default', ib_req=True),

        options=dict(type='list', elements='dict', options=option_spec, transform=options),

        extattrs=dict(type='dict'),
        comment=dict(),
        container=dict(type='bool', ib_req=True)
    )

    argument_spec = dict(
        provider=dict(required=True),
        state=dict(default='present', choices=['present', 'absent'])
    )

    argument_spec.update(ib_spec)
    argument_spec.update(WapiModule.provider_spec)

    module = QuantumModule(argument_spec=argument_spec,
                           supports_check_mode=True)

    # to get the argument ipaddr
    obj_filter = dict([(k, module.params[k]) for k, v in iteritems(ib_spec) if v.get('ib_req')])
    network_type, ib_spec = check_ip_addr_type(obj_filter, ib_spec)

    wapi = WapiModule(module)
    # to check for vendor specific dhcp option
    ib_spec = check_vendor_specific_dhcp_option(module, ib_spec)

    result = wapi.run(network_type, ib_spec)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
