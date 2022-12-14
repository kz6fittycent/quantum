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
module: fortios_system_central_management
short_description: Configure central management in Fortinet's FortiOS and FortiGate.
description:
    - This module is able to configure a FortiGate or FortiOS (FOS) device by allowing the
      user to set and modify system feature and central_management category.
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
    system_central_management:
        description:
            - Configure central management.
        default: null
        type: dict
        suboptions:
            allow_monitor:
                description:
                    - Enable/disable allowing the central management server to remotely monitor this FortiGate
                type: str
                choices:
                    - enable
                    - disable
            allow_push_configuration:
                description:
                    - Enable/disable allowing the central management server to push configuration changes to this FortiGate.
                type: str
                choices:
                    - enable
                    - disable
            allow_push_firmware:
                description:
                    - Enable/disable allowing the central management server to push firmware updates to this FortiGate.
                type: str
                choices:
                    - enable
                    - disable
            allow_remote_firmware_upgrade:
                description:
                    - Enable/disable remotely upgrading the firmware on this FortiGate from the central management server.
                type: str
                choices:
                    - enable
                    - disable
            enc_algorithm:
                description:
                    - Encryption strength for communications between the FortiGate and central management.
                type: str
                choices:
                    - default
                    - high
                    - low
            fmg:
                description:
                    - IP address or FQDN of the FortiManager.
                type: str
            fmg_source_ip:
                description:
                    - IPv4 source address that this FortiGate uses when communicating with FortiManager.
                type: str
            fmg_source_ip6:
                description:
                    - IPv6 source address that this FortiGate uses when communicating with FortiManager.
                type: str
            include_default_servers:
                description:
                    - Enable/disable inclusion of public FortiGuard servers in the override server list.
                type: str
                choices:
                    - enable
                    - disable
            mode:
                description:
                    - Central management mode.
                type: str
                choices:
                    - normal
                    - backup
            schedule_config_restore:
                description:
                    - Enable/disable allowing the central management server to restore the configuration of this FortiGate.
                type: str
                choices:
                    - enable
                    - disable
            schedule_script_restore:
                description:
                    - Enable/disable allowing the central management server to restore the scripts stored on this FortiGate.
                type: str
                choices:
                    - enable
                    - disable
            serial_number:
                description:
                    - Serial number.
                type: str
            server_list:
                description:
                    - Additional servers that the FortiGate can use for updates (for AV, IPS, updates) and ratings (for web filter and antispam ratings)
                      servers.
                type: list
                suboptions:
                    addr_type:
                        description:
                            - Indicate whether the FortiGate communicates with the override server using an IPv4 address, an IPv6 address or a FQDN.
                        type: str
                        choices:
                            - ipv4
                            - ipv6
                            - fqdn
                    fqdn:
                        description:
                            - FQDN address of override server.
                        type: str
                    id:
                        description:
                            - ID.
                        required: true
                        type: int
                    server_address:
                        description:
                            - IPv4 address of override server.
                        type: str
                    server_address6:
                        description:
                            - IPv6 address of override server.
                        type: str
                    server_type:
                        description:
                            - FortiGuard service type.
                        type: str
                        choices:
                            - update
                            - rating
            type:
                description:
                    - Central management type.
                type: str
                choices:
                    - fortimanager
                    - fortiguard
                    - none
            vdom:
                description:
                    - Virtual domain (VDOM) name to use when communicating with FortiManager. Source system.vdom.name.
                type: str
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
  - name: Configure central management.
    fortios_system_central_management:
      host:  "{{ host }}"
      username: "{{ username }}"
      password: "{{ password }}"
      vdom:  "{{ vdom }}"
      https: "False"
      system_central_management:
        allow_monitor: "enable"
        allow_push_configuration: "enable"
        allow_push_firmware: "enable"
        allow_remote_firmware_upgrade: "enable"
        enc_algorithm: "default"
        fmg: "<your_own_value>"
        fmg_source_ip: "<your_own_value>"
        fmg_source_ip6: "<your_own_value>"
        include_default_servers: "enable"
        mode: "normal"
        schedule_config_restore: "enable"
        schedule_script_restore: "enable"
        serial_number: "<your_own_value>"
        server_list:
         -
            addr_type: "ipv4"
            fqdn: "<your_own_value>"
            id:  "19"
            server_address: "<your_own_value>"
            server_address6: "<your_own_value>"
            server_type: "update"
        type: "fortimanager"
        vdom: "<your_own_value> (source system.vdom.name)"
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


def filter_system_central_management_data(json):
    option_list = ['allow_monitor', 'allow_push_configuration', 'allow_push_firmware',
                   'allow_remote_firmware_upgrade', 'enc_algorithm', 'fmg',
                   'fmg_source_ip', 'fmg_source_ip6', 'include_default_servers',
                   'mode', 'schedule_config_restore', 'schedule_script_restore',
                   'serial_number', 'server_list', 'type',
                   'vdom']
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


def system_central_management(data, fos):
    vdom = data['vdom']
    system_central_management_data = data['system_central_management']
    filtered_data = underscore_to_hyphen(filter_system_central_management_data(system_central_management_data))

    return fos.set('system',
                   'central-management',
                   data=filtered_data,
                   vdom=vdom)


def is_successful_status(status):
    return status['status'] == "success" or \
        status['http_method'] == "DELETE" and status['http_status'] == 404


def fortios_system(data, fos):

    if data['system_central_management']:
        resp = system_central_management(data, fos)

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
        "system_central_management": {
            "required": False, "type": "dict", "default": None,
            "options": {
                "allow_monitor": {"required": False, "type": "str",
                                  "choices": ["enable", "disable"]},
                "allow_push_configuration": {"required": False, "type": "str",
                                             "choices": ["enable", "disable"]},
                "allow_push_firmware": {"required": False, "type": "str",
                                        "choices": ["enable", "disable"]},
                "allow_remote_firmware_upgrade": {"required": False, "type": "str",
                                                  "choices": ["enable", "disable"]},
                "enc_algorithm": {"required": False, "type": "str",
                                  "choices": ["default", "high", "low"]},
                "fmg": {"required": False, "type": "str"},
                "fmg_source_ip": {"required": False, "type": "str"},
                "fmg_source_ip6": {"required": False, "type": "str"},
                "include_default_servers": {"required": False, "type": "str",
                                            "choices": ["enable", "disable"]},
                "mode": {"required": False, "type": "str",
                         "choices": ["normal", "backup"]},
                "schedule_config_restore": {"required": False, "type": "str",
                                            "choices": ["enable", "disable"]},
                "schedule_script_restore": {"required": False, "type": "str",
                                            "choices": ["enable", "disable"]},
                "serial_number": {"required": False, "type": "str"},
                "server_list": {"required": False, "type": "list",
                                "options": {
                                    "addr_type": {"required": False, "type": "str",
                                                  "choices": ["ipv4", "ipv6", "fqdn"]},
                                    "fqdn": {"required": False, "type": "str"},
                                    "id": {"required": True, "type": "int"},
                                    "server_address": {"required": False, "type": "str"},
                                    "server_address6": {"required": False, "type": "str"},
                                    "server_type": {"required": False, "type": "str",
                                                    "choices": ["update", "rating"]}
                                }},
                "type": {"required": False, "type": "str",
                         "choices": ["fortimanager", "fortiguard", "none"]},
                "vdom": {"required": False, "type": "str"}

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

            is_error, has_changed, result = fortios_system(module.params, fos)
        else:
            module.fail_json(**FAIL_SOCKET_MSG)
    else:
        try:
            from fortiosapi import FortiOSAPI
        except ImportError:
            module.fail_json(msg="fortiosapi module is required")

        fos = FortiOSAPI()

        login(module.params, fos)
        is_error, has_changed, result = fortios_system(module.params, fos)
        fos.logout()

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Error in repo", meta=result)


if __name__ == '__main__':
    main()
