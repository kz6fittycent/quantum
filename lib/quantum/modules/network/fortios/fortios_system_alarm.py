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
module: fortios_system_alarm
short_description: Configure alarm in Fortinet's FortiOS and FortiGate.
description:
    - This module is able to configure a FortiGate or FortiOS (FOS) device by allowing the
      user to set and modify system feature and alarm category.
      Examples include all parameters and values need to be adjusted to datasources before usage.
      Tested with FOS v6.0.5
version_added: "2.9"
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
    system_alarm:
        description:
            - Configure alarm.
        default: null
        type: dict
        suboptions:
            audible:
                description:
                    - Enable/disable audible alarm.
                type: str
                choices:
                    - enable
                    - disable
            groups:
                description:
                    - Alarm groups.
                type: list
                suboptions:
                    admin_auth_failure_threshold:
                        description:
                            - Admin authentication failure threshold.
                        type: int
                    admin_auth_lockout_threshold:
                        description:
                            - Admin authentication lockout threshold.
                        type: int
                    decryption_failure_threshold:
                        description:
                            - Decryption failure threshold.
                        type: int
                    encryption_failure_threshold:
                        description:
                            - Encryption failure threshold.
                        type: int
                    fw_policy_id:
                        description:
                            - Firewall policy ID.
                        type: int
                    fw_policy_id_threshold:
                        description:
                            - Firewall policy ID threshold.
                        type: int
                    fw_policy_violations:
                        description:
                            - Firewall policy violations.
                        type: list
                        suboptions:
                            dst_ip:
                                description:
                                    - Destination IP (0=all).
                                type: str
                            dst_port:
                                description:
                                    - Destination port (0=all).
                                type: int
                            id:
                                description:
                                    - Firewall policy violations ID.
                                required: true
                                type: int
                            src_ip:
                                description:
                                    - Source IP (0=all).
                                type: str
                            src_port:
                                description:
                                    - Source port (0=all).
                                type: int
                            threshold:
                                description:
                                    - Firewall policy violation threshold.
                                type: int
                    id:
                        description:
                            - Group ID.
                        required: true
                        type: int
                    log_full_warning_threshold:
                        description:
                            - Log full warning threshold.
                        type: int
                    period:
                        description:
                            - Time period in seconds (0 = from start up).
                        type: int
                    replay_attempt_threshold:
                        description:
                            - Replay attempt threshold.
                        type: int
                    self_test_failure_threshold:
                        description:
                            - Self-test failure threshold.
                        type: int
                    user_auth_failure_threshold:
                        description:
                            - User authentication failure threshold.
                        type: int
                    user_auth_lockout_threshold:
                        description:
                            - User authentication lockout threshold.
                        type: int
            status:
                description:
                    - Enable/disable alarm.
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
  - name: Configure alarm.
    fortios_system_alarm:
      host:  "{{ host }}"
      username: "{{ username }}"
      password: "{{ password }}"
      vdom:  "{{ vdom }}"
      https: "False"
      system_alarm:
        audible: "enable"
        groups:
         -
            admin_auth_failure_threshold: "5"
            admin_auth_lockout_threshold: "6"
            decryption_failure_threshold: "7"
            encryption_failure_threshold: "8"
            fw_policy_id: "9"
            fw_policy_id_threshold: "10"
            fw_policy_violations:
             -
                dst_ip: "<your_own_value>"
                dst_port: "13"
                id:  "14"
                src_ip: "<your_own_value>"
                src_port: "16"
                threshold: "17"
            id:  "18"
            log_full_warning_threshold: "19"
            period: "20"
            replay_attempt_threshold: "21"
            self_test_failure_threshold: "22"
            user_auth_failure_threshold: "23"
            user_auth_lockout_threshold: "24"
        status: "enable"
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


def filter_system_alarm_data(json):
    option_list = ['audible', 'groups', 'status']
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


def system_alarm(data, fos):
    vdom = data['vdom']
    system_alarm_data = data['system_alarm']
    filtered_data = underscore_to_hyphen(filter_system_alarm_data(system_alarm_data))

    return fos.set('system',
                   'alarm',
                   data=filtered_data,
                   vdom=vdom)


def is_successful_status(status):
    return status['status'] == "success" or \
        status['http_method'] == "DELETE" and status['http_status'] == 404


def fortios_system(data, fos):

    if data['system_alarm']:
        resp = system_alarm(data, fos)

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
        "system_alarm": {
            "required": False, "type": "dict", "default": None,
            "options": {
                "audible": {"required": False, "type": "str",
                            "choices": ["enable", "disable"]},
                "groups": {"required": False, "type": "list",
                           "options": {
                               "admin_auth_failure_threshold": {"required": False, "type": "int"},
                               "admin_auth_lockout_threshold": {"required": False, "type": "int"},
                               "decryption_failure_threshold": {"required": False, "type": "int"},
                               "encryption_failure_threshold": {"required": False, "type": "int"},
                               "fw_policy_id": {"required": False, "type": "int"},
                               "fw_policy_id_threshold": {"required": False, "type": "int"},
                               "fw_policy_violations": {"required": False, "type": "list",
                                                        "options": {
                                                            "dst_ip": {"required": False, "type": "str"},
                                                            "dst_port": {"required": False, "type": "int"},
                                                            "id": {"required": True, "type": "int"},
                                                            "src_ip": {"required": False, "type": "str"},
                                                            "src_port": {"required": False, "type": "int"},
                                                            "threshold": {"required": False, "type": "int"}
                                                        }},
                               "id": {"required": True, "type": "int"},
                               "log_full_warning_threshold": {"required": False, "type": "int"},
                               "period": {"required": False, "type": "int"},
                               "replay_attempt_threshold": {"required": False, "type": "int"},
                               "self_test_failure_threshold": {"required": False, "type": "int"},
                               "user_auth_failure_threshold": {"required": False, "type": "int"},
                               "user_auth_lockout_threshold": {"required": False, "type": "int"}
                           }},
                "status": {"required": False, "type": "str",
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
