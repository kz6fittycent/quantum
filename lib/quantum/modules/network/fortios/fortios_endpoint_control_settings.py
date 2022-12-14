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
module: fortios_endpoint_control_settings
short_description: Configure endpoint control settings in Fortinet's FortiOS and FortiGate.
description:
    - This module is able to configure a FortiGate or FortiOS (FOS) device by allowing the
      user to set and modify endpoint_control feature and settings category.
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
    endpoint_control_settings:
        description:
            - Configure endpoint control settings.
        default: null
        type: dict
        suboptions:
            download_custom_link:
                description:
                    - Customized URL for downloading FortiClient.
                type: str
            download_location:
                description:
                    - FortiClient download location (FortiGuard or custom).
                type: str
                choices:
                    - fortiguard
                    - custom
            forticlient_avdb_update_interval:
                description:
                    - Period of time between FortiClient AntiVirus database updates (0 - 24 hours).
                type: int
            forticlient_dereg_unsupported_client:
                description:
                    - Enable/disable deregistering unsupported FortiClient endpoints.
                type: str
                choices:
                    - enable
                    - disable
            forticlient_ems_rest_api_call_timeout:
                description:
                    - FortiClient EMS call timeout in milliseconds (500 - 30000 milliseconds).
                type: int
            forticlient_keepalive_interval:
                description:
                    - Interval between two KeepAlive messages from FortiClient (20 - 300 sec).
                type: int
            forticlient_offline_grace:
                description:
                    - Enable/disable grace period for offline registered clients.
                type: str
                choices:
                    - enable
                    - disable
            forticlient_offline_grace_interval:
                description:
                    - Grace period for offline registered FortiClient (60 - 600 sec).
                type: int
            forticlient_reg_key:
                description:
                    - FortiClient registration key.
                type: str
            forticlient_reg_key_enforce:
                description:
                    - Enable/disable requiring or enforcing FortiClient registration keys.
                type: str
                choices:
                    - enable
                    - disable
            forticlient_reg_timeout:
                description:
                    - FortiClient registration license timeout (days, min = 1, max = 180, 0 means unlimited).
                type: int
            forticlient_sys_update_interval:
                description:
                    - Interval between two system update messages from FortiClient (30 - 1440 min).
                type: int
            forticlient_user_avatar:
                description:
                    - Enable/disable uploading FortiClient user avatars.
                type: str
                choices:
                    - enable
                    - disable
            forticlient_warning_interval:
                description:
                    - Period of time between FortiClient portal warnings (0 - 24 hours).
                type: int
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
  - name: Configure endpoint control settings.
    fortios_endpoint_control_settings:
      host:  "{{ host }}"
      username: "{{ username }}"
      password: "{{ password }}"
      vdom:  "{{ vdom }}"
      https: "False"
      endpoint_control_settings:
        download_custom_link: "<your_own_value>"
        download_location: "fortiguard"
        forticlient_avdb_update_interval: "5"
        forticlient_dereg_unsupported_client: "enable"
        forticlient_ems_rest_api_call_timeout: "7"
        forticlient_keepalive_interval: "8"
        forticlient_offline_grace: "enable"
        forticlient_offline_grace_interval: "10"
        forticlient_reg_key: "<your_own_value>"
        forticlient_reg_key_enforce: "enable"
        forticlient_reg_timeout: "13"
        forticlient_sys_update_interval: "14"
        forticlient_user_avatar: "enable"
        forticlient_warning_interval: "16"
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


def filter_endpoint_control_settings_data(json):
    option_list = ['download_custom_link', 'download_location', 'forticlient_avdb_update_interval',
                   'forticlient_dereg_unsupported_client', 'forticlient_ems_rest_api_call_timeout', 'forticlient_keepalive_interval',
                   'forticlient_offline_grace', 'forticlient_offline_grace_interval', 'forticlient_reg_key',
                   'forticlient_reg_key_enforce', 'forticlient_reg_timeout', 'forticlient_sys_update_interval',
                   'forticlient_user_avatar', 'forticlient_warning_interval']
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


def endpoint_control_settings(data, fos):
    vdom = data['vdom']
    endpoint_control_settings_data = data['endpoint_control_settings']
    filtered_data = underscore_to_hyphen(filter_endpoint_control_settings_data(endpoint_control_settings_data))

    return fos.set('endpoint-control',
                   'settings',
                   data=filtered_data,
                   vdom=vdom)


def is_successful_status(status):
    return status['status'] == "success" or \
        status['http_method'] == "DELETE" and status['http_status'] == 404


def fortios_endpoint_control(data, fos):

    if data['endpoint_control_settings']:
        resp = endpoint_control_settings(data, fos)

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
        "endpoint_control_settings": {
            "required": False, "type": "dict", "default": None,
            "options": {
                "download_custom_link": {"required": False, "type": "str"},
                "download_location": {"required": False, "type": "str",
                                      "choices": ["fortiguard", "custom"]},
                "forticlient_avdb_update_interval": {"required": False, "type": "int"},
                "forticlient_dereg_unsupported_client": {"required": False, "type": "str",
                                                         "choices": ["enable", "disable"]},
                "forticlient_ems_rest_api_call_timeout": {"required": False, "type": "int"},
                "forticlient_keepalive_interval": {"required": False, "type": "int"},
                "forticlient_offline_grace": {"required": False, "type": "str",
                                              "choices": ["enable", "disable"]},
                "forticlient_offline_grace_interval": {"required": False, "type": "int"},
                "forticlient_reg_key": {"required": False, "type": "str", "no_log": True},
                "forticlient_reg_key_enforce": {"required": False, "type": "str",
                                                "choices": ["enable", "disable"]},
                "forticlient_reg_timeout": {"required": False, "type": "int"},
                "forticlient_sys_update_interval": {"required": False, "type": "int"},
                "forticlient_user_avatar": {"required": False, "type": "str",
                                            "choices": ["enable", "disable"]},
                "forticlient_warning_interval": {"required": False, "type": "int"}

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

            is_error, has_changed, result = fortios_endpoint_control(module.params, fos)
        else:
            module.fail_json(**FAIL_SOCKET_MSG)
    else:
        try:
            from fortiosapi import FortiOSAPI
        except ImportError:
            module.fail_json(msg="fortiosapi module is required")

        fos = FortiOSAPI()

        login(module.params, fos)
        is_error, has_changed, result = fortios_endpoint_control(module.params, fos)
        fos.logout()

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Error in repo", meta=result)


if __name__ == '__main__':
    main()
