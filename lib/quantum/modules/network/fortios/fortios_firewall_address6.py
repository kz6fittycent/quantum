#!/usr/bin/python
from __future__ import (absolute_import, division, print_function)
# Copyright 2019 Fortinet, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

__metaclass__ = type

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'metadata_version': '1.1'}

DOCUMENTATION = '''
---
module: fortios_firewall_address6
short_description: Configure IPv6 firewall addresses in Fortinet's FortiOS and FortiGate.
description:
    - This module is able to configure a FortiGate or FortiOS (FOS) device by allowing the
      user to set and modify firewall feature and address6 category.
      Examples include all parameters and values need to be adjusted to datasources before usage.
      Tested with FOS v6.0.5
version_added: "2.8"
author:
    - Miguel Angel Munoz (@mamunozgonzalez)
    - Nicolas Thomas (@thomnico)
notes:
    - Requires fortiosapi library developed by Fortinet
    - Run as a local_action in your coupling
requirements:
    - fortiosapi>=0.9.8
options:
    host:
        description:
            - FortiOS or FortiGate IP address.
        type: str
        required: false
    username:
        description:
            - FortiOS or FortiGate username.
        type: str
        required: false
    password:
        description:
            - FortiOS or FortiGate password.
        type: str
        default: ""
    vdom:
        description:
            - Virtual domain, among those defined previously. A vdom is a
              virtual instance of the FortiGate that can be configured and
              used as a different unit.
        type: str
        default: root
    https:
        description:
            - Indicates if the requests towards FortiGate must use HTTPS protocol.
        type: bool
        default: true
    ssl_verify:
        description:
            - Ensures FortiGate certificate must be verified by a proper CA.
        type: bool
        default: true
        version_added: 2.9
    state:
        description:
            - Indicates whether to create or remove the object.
              This attribute was present already in previous version in a deeper level.
              It has been moved out to this outer level.
        type: str
        required: false
        choices:
            - present
            - absent
        version_added: 2.9
    firewall_address6:
        description:
            - Configure IPv6 firewall addresses.
        default: null
        type: dict
        suboptions:
            state:
                description:
                    - B(Deprecated)
                    - Starting with Quantum 2.9 we recommend using the top-level 'state' parameter.
                    - HORIZONTALLINE
                    - Indicates whether to create or remove the object.
                type: str
                required: false
                choices:
                    - present
                    - absent
            cache_ttl:
                description:
                    - Minimal TTL of individual IPv6 addresses in FQDN cache.
                type: int
            color:
                description:
                    - Integer value to determine the color of the icon in the GUI (range 1 to 32).
                type: int
            comment:
                description:
                    - Comment.
                type: str
            end_ip:
                description:
                    - "Final IP address (inclusive) in the range for the address (format: xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx)."
                type: str
            fqdn:
                description:
                    - Fully qualified domain name.
                type: str
            host:
                description:
                    - Host Address.
                type: str
            host_type:
                description:
                    - Host type.
                type: str
                choices:
                    - any
                    - specific
            ip6:
                description:
                    - "IPv6 address prefix (format: xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx/xxx)."
                type: str
            list:
                description:
                    - IP address list.
                type: list
                suboptions:
                    ip:
                        description:
                            - IP.
                        required: true
                        type: str
            name:
                description:
                    - Address name.
                required: true
                type: str
            obj_id:
                description:
                    - Object ID for NSX.
                type: str
            sdn:
                description:
                    - SDN.
                type: str
                choices:
                    - nsx
            start_ip:
                description:
                    - "First IP address (inclusive) in the range for the address (format: xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx)."
                type: str
            subnet_segment:
                description:
                    - IPv6 subnet segments.
                type: list
                suboptions:
                    name:
                        description:
                            - Name.
                        required: true
                        type: str
                    type:
                        description:
                            - Subnet segment type.
                        type: str
                        choices:
                            - any
                            - specific
                    value:
                        description:
                            - Subnet segment value.
                        type: str
            tagging:
                description:
                    - Config object tagging
                type: list
                suboptions:
                    category:
                        description:
                            - Tag category. Source system.object-tagging.category.
                        type: str
                    name:
                        description:
                            - Tagging entry name.
                        required: true
                        type: str
                    tags:
                        description:
                            - Tags.
                        type: list
                        suboptions:
                            name:
                                description:
                                    - Tag name. Source system.object-tagging.tags.name.
                                required: true
                                type: str
            template:
                description:
                    - IPv6 address template. Source firewall.address6-template.name.
                type: str
            type:
                description:
                    - Type of IPv6 address object .
                type: str
                choices:
                    - ipprefix
                    - iprange
                    - fqdn
                    - dynamic
                    - template
            uuid:
                description:
                    - Universally Unique Identifier (UUID; automatically assigned but can be manually reset).
                type: str
            visibility:
                description:
                    - Enable/disable the visibility of the object in the GUI.
                type: str
                choices:
                    - enable
                    - disable
'''

EXAMPLES = '''
- hosts: localhost
  vars:
   host: "192.168.122.40"
   username: "admin"
   password: ""
   vdom: "root"
   ssl_verify: "False"
  tasks:
  - name: Configure IPv6 firewall addresses.
    fortios_firewall_address6:
      host:  "{{ host }}"
      username: "{{ username }}"
      password: "{{ password }}"
      vdom:  "{{ vdom }}"
      https: "False"
      state: "present"
      firewall_address6:
        cache_ttl: "3"
        color: "4"
        comment: "Comment."
        end_ip: "<your_own_value>"
        fqdn: "<your_own_value>"
        host: "<your_own_value>"
        host_type: "any"
        ip6: "<your_own_value>"
        list:
         -
            ip: "<your_own_value>"
        name: "default_name_13"
        obj_id: "<your_own_value>"
        sdn: "nsx"
        start_ip: "<your_own_value>"
        subnet_segment:
         -
            name: "default_name_18"
            type: "any"
            value: "<your_own_value>"
        tagging:
         -
            category: "<your_own_value> (source system.object-tagging.category)"
            name: "default_name_23"
            tags:
             -
                name: "default_name_25 (source system.object-tagging.tags.name)"
        template: "<your_own_value> (source firewall.address6-template.name)"
        type: "ipprefix"
        uuid: "<your_own_value>"
        visibility: "enable"
'''

RETURN = '''
build:
  description: Build number of the fortigate image
  returned: always
  type: str
  sample: '1547'
http_method:
  description: Last method used to provision the content into FortiGate
  returned: always
  type: str
  sample: 'PUT'
http_status:
  description: Last result given by FortiGate on last operation applied
  returned: always
  type: str
  sample: "200"
mkey:
  description: Master key (id) used in the last call to FortiGate
  returned: success
  type: str
  sample: "id"
name:
  description: Name of the table used to fulfill the request
  returned: always
  type: str
  sample: "urlfilter"
path:
  description: Path of the table used to fulfill the request
  returned: always
  type: str
  sample: "webfilter"
revision:
  description: Internal revision number
  returned: always
  type: str
  sample: "17.0.2.10658"
serial:
  description: Serial number of the unit
  returned: always
  type: str
  sample: "FGVMEVYYQT3AB5352"
status:
  description: Indication of the operation's result
  returned: always
  type: str
  sample: "success"
vdom:
  description: Virtual domain used
  returned: always
  type: str
  sample: "root"
version:
  description: Version of the FortiGate
  returned: always
  type: str
  sample: "v5.6.3"

'''

from quantum.module_utils.basic import QuantumModule
from quantum.module_utils.connection import Connection
from quantum.module_utils.network.fortios.fortios import FortiOSHandler
from quantum.module_utils.network.fortimanager.common import FAIL_SOCKET_MSG


def login(data, fos):
    host = data['host']
    username = data['username']
    password = data['password']
    ssl_verify = data['ssl_verify']

    fos.debug('on')
    if 'https' in data and not data['https']:
        fos.https('off')
    else:
        fos.https('on')

    fos.login(host, username, password, verify=ssl_verify)


def filter_firewall_address6_data(json):
    option_list = ['cache_ttl', 'color', 'comment',
                   'end_ip', 'fqdn', 'host',
                   'host_type', 'ip6', 'list',
                   'name', 'obj_id', 'sdn',
                   'start_ip', 'subnet_segment', 'tagging',
                   'template', 'type', 'uuid',
                   'visibility']
    dictionary = {}

    for attribute in option_list:
        if attribute in json and json[attribute] is not None:
            dictionary[attribute] = json[attribute]

    return dictionary


def underscore_to_hyphen(data):
    if isinstance(data, list):
        for elem in data:
            elem = underscore_to_hyphen(elem)
    elif isinstance(data, dict):
        new_data = {}
        for k, v in data.items():
            new_data[k.replace('_', '-')] = underscore_to_hyphen(v)
        data = new_data

    return data


def firewall_address6(data, fos):
    vdom = data['vdom']
    if 'state' in data and data['state']:
        state = data['state']
    elif 'state' in data['firewall_address6'] and data['firewall_address6']:
        state = data['firewall_address6']['state']
    else:
        state = True
    firewall_address6_data = data['firewall_address6']
    filtered_data = underscore_to_hyphen(filter_firewall_address6_data(firewall_address6_data))

    if state == "present":
        return fos.set('firewall',
                       'address6',
                       data=filtered_data,
                       vdom=vdom)

    elif state == "absent":
        return fos.delete('firewall',
                          'address6',
                          mkey=filtered_data['name'],
                          vdom=vdom)


def is_successful_status(status):
    return status['status'] == "success" or \
        status['http_method'] == "DELETE" and status['http_status'] == 404


def fortios_firewall(data, fos):

    if data['firewall_address6']:
        resp = firewall_address6(data, fos)

    return not is_successful_status(resp), \
        resp['status'] == "success", \
        resp


def main():
    fields = {
        "host": {"required": False, "type": "str"},
        "username": {"required": False, "type": "str"},
        "password": {"required": False, "type": "str", "default": "", "no_log": True},
        "vdom": {"required": False, "type": "str", "default": "root"},
        "https": {"required": False, "type": "bool", "default": True},
        "ssl_verify": {"required": False, "type": "bool", "default": True},
        "state": {"required": False, "type": "str",
                  "choices": ["present", "absent"]},
        "firewall_address6": {
            "required": False, "type": "dict", "default": None,
            "options": {
                "state": {"required": False, "type": "str",
                          "choices": ["present", "absent"]},
                "cache_ttl": {"required": False, "type": "int"},
                "color": {"required": False, "type": "int"},
                "comment": {"required": False, "type": "str"},
                "end_ip": {"required": False, "type": "str"},
                "fqdn": {"required": False, "type": "str"},
                "host": {"required": False, "type": "str"},
                "host_type": {"required": False, "type": "str",
                              "choices": ["any", "specific"]},
                "ip6": {"required": False, "type": "str"},
                "list": {"required": False, "type": "list",
                         "options": {
                             "ip": {"required": True, "type": "str"}
                         }},
                "name": {"required": True, "type": "str"},
                "obj_id": {"required": False, "type": "str"},
                "sdn": {"required": False, "type": "str",
                        "choices": ["nsx"]},
                "start_ip": {"required": False, "type": "str"},
                "subnet_segment": {"required": False, "type": "list",
                                   "options": {
                                       "name": {"required": True, "type": "str"},
                                       "type": {"required": False, "type": "str",
                                                "choices": ["any", "specific"]},
                                       "value": {"required": False, "type": "str"}
                                   }},
                "tagging": {"required": False, "type": "list",
                            "options": {
                                "category": {"required": False, "type": "str"},
                                "name": {"required": True, "type": "str"},
                                "tags": {"required": False, "type": "list",
                                         "options": {
                                             "name": {"required": True, "type": "str"}
                                         }}
                            }},
                "template": {"required": False, "type": "str"},
                "type": {"required": False, "type": "str",
                         "choices": ["ipprefix", "iprange", "fqdn",
                                     "dynamic", "template"]},
                "uuid": {"required": False, "type": "str"},
                "visibility": {"required": False, "type": "str",
                               "choices": ["enable", "disable"]}

            }
        }
    }

    module = QuantumModule(argument_spec=fields,
                           supports_check_mode=False)

    # legacy_mode refers to using fortiosapi instead of HTTPAPI
    legacy_mode = 'host' in module.params and module.params['host'] is not None and \
                  'username' in module.params and module.params['username'] is not None and \
                  'password' in module.params and module.params['password'] is not None

    if not legacy_mode:
        if module._socket_path:
            connection = Connection(module._socket_path)
            fos = FortiOSHandler(connection)

            is_error, has_changed, result = fortios_firewall(module.params, fos)
        else:
            module.fail_json(**FAIL_SOCKET_MSG)
    else:
        try:
            from fortiosapi import FortiOSAPI
        except ImportError:
            module.fail_json(msg="fortiosapi module is required")

        fos = FortiOSAPI()

        login(module.params, fos)
        is_error, has_changed, result = fortios_firewall(module.params, fos)
        fos.logout()

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Error in repo", meta=result)


if __name__ == '__main__':
    main()
