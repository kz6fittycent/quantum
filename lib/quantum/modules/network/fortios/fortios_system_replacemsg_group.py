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
module: fortios_system_replacemsg_group
short_description: Configure replacement message groups in Fortinet's FortiOS and FortiGate.
description:
    - This module is able to configure a FortiGate or FortiOS (FOS) device by allowing the
      user to set and modify system feature and replacemsg_group category.
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
    state:
        description:
            - Indicates whether to create or remove the object.
        type: str
        required: true
        choices:
            - present
            - absent
    system_replacemsg_group:
        description:
            - Configure replacement message groups.
        default: null
        type: dict
        suboptions:
            admin:
                description:
                    - Replacement message table entries.
                type: list
                suboptions:
                    buffer:
                        description:
                            - Message string.
                        type: str
                    format:
                        description:
                            - Format flag.
                        type: str
                        choices:
                            - none
                            - text
                            - html
                            - wml
                    header:
                        description:
                            - Header flag.
                        type: str
                        choices:
                            - none
                            - http
                            - 8bit
                    msg_type:
                        description:
                            - Message type.
                        type: str
            alertmail:
                description:
                    - Replacement message table entries.
                type: list
                suboptions:
                    buffer:
                        description:
                            - Message string.
                        type: str
                    format:
                        description:
                            - Format flag.
                        type: str
                        choices:
                            - none
                            - text
                            - html
                            - wml
                    header:
                        description:
                            - Header flag.
                        type: str
                        choices:
                            - none
                            - http
                            - 8bit
                    msg_type:
                        description:
                            - Message type.
                        type: str
            auth:
                description:
                    - Replacement message table entries.
                type: list
                suboptions:
                    buffer:
                        description:
                            - Message string.
                        type: str
                    format:
                        description:
                            - Format flag.
                        type: str
                        choices:
                            - none
                            - text
                            - html
                            - wml
                    header:
                        description:
                            - Header flag.
                        type: str
                        choices:
                            - none
                            - http
                            - 8bit
                    msg_type:
                        description:
                            - Message type.
                        type: str
            comment:
                description:
                    - Comment.
                type: str
            custom_message:
                description:
                    - Replacement message table entries.
                type: list
                suboptions:
                    buffer:
                        description:
                            - Message string.
                        type: str
                    format:
                        description:
                            - Format flag.
                        type: str
                        choices:
                            - none
                            - text
                            - html
                            - wml
                    header:
                        description:
                            - Header flag.
                        type: str
                        choices:
                            - none
                            - http
                            - 8bit
                    msg_type:
                        description:
                            - Message type.
                        type: str
            device_detection_portal:
                description:
                    - Replacement message table entries.
                type: list
                suboptions:
                    buffer:
                        description:
                            - Message string.
                        type: str
                    format:
                        description:
                            - Format flag.
                        type: str
                        choices:
                            - none
                            - text
                            - html
                            - wml
                    header:
                        description:
                            - Header flag.
                        type: str
                        choices:
                            - none
                            - http
                            - 8bit
                    msg_type:
                        description:
                            - Message type.
                        type: str
            ec:
                description:
                    - Replacement message table entries.
                type: list
                suboptions:
                    buffer:
                        description:
                            - Message string.
                        type: str
                    format:
                        description:
                            - Format flag.
                        type: str
                        choices:
                            - none
                            - text
                            - html
                            - wml
                    header:
                        description:
                            - Header flag.
                        type: str
                        choices:
                            - none
                            - http
                            - 8bit
                    msg_type:
                        description:
                            - Message type.
                        type: str
            fortiguard_wf:
                description:
                    - Replacement message table entries.
                type: list
                suboptions:
                    buffer:
                        description:
                            - Message string.
                        type: str
                    format:
                        description:
                            - Format flag.
                        type: str
                        choices:
                            - none
                            - text
                            - html
                            - wml
                    header:
                        description:
                            - Header flag.
                        type: str
                        choices:
                            - none
                            - http
                            - 8bit
                    msg_type:
                        description:
                            - Message type.
                        type: str
            ftp:
                description:
                    - Replacement message table entries.
                type: list
                suboptions:
                    buffer:
                        description:
                            - Message string.
                        type: str
                    format:
                        description:
                            - Format flag.
                        type: str
                        choices:
                            - none
                            - text
                            - html
                            - wml
                    header:
                        description:
                            - Header flag.
                        type: str
                        choices:
                            - none
                            - http
                            - 8bit
                    msg_type:
                        description:
                            - Message type.
                        type: str
            group_type:
                description:
                    - Group type.
                type: str
                choices:
                    - default
                    - utm
                    - auth
                    - ec
            http:
                description:
                    - Replacement message table entries.
                type: list
                suboptions:
                    buffer:
                        description:
                            - Message string.
                        type: str
                    format:
                        description:
                            - Format flag.
                        type: str
                        choices:
                            - none
                            - text
                            - html
                            - wml
                    header:
                        description:
                            - Header flag.
                        type: str
                        choices:
                            - none
                            - http
                            - 8bit
                    msg_type:
                        description:
                            - Message type.
                        type: str
            icap:
                description:
                    - Replacement message table entries.
                type: list
                suboptions:
                    buffer:
                        description:
                            - Message string.
                        type: str
                    format:
                        description:
                            - Format flag.
                        type: str
                        choices:
                            - none
                            - text
                            - html
                            - wml
                    header:
                        description:
                            - Header flag.
                        type: str
                        choices:
                            - none
                            - http
                            - 8bit
                    msg_type:
                        description:
                            - Message type.
                        type: str
            mail:
                description:
                    - Replacement message table entries.
                type: list
                suboptions:
                    buffer:
                        description:
                            - Message string.
                        type: str
                    format:
                        description:
                            - Format flag.
                        type: str
                        choices:
                            - none
                            - text
                            - html
                            - wml
                    header:
                        description:
                            - Header flag.
                        type: str
                        choices:
                            - none
                            - http
                            - 8bit
                    msg_type:
                        description:
                            - Message type.
                        type: str
            nac_quar:
                description:
                    - Replacement message table entries.
                type: list
                suboptions:
                    buffer:
                        description:
                            - Message string.
                        type: str
                    format:
                        description:
                            - Format flag.
                        type: str
                        choices:
                            - none
                            - text
                            - html
                            - wml
                    header:
                        description:
                            - Header flag.
                        type: str
                        choices:
                            - none
                            - http
                            - 8bit
                    msg_type:
                        description:
                            - Message type.
                        type: str
            name:
                description:
                    - Group name.
                required: true
                type: str
            nntp:
                description:
                    - Replacement message table entries.
                type: list
                suboptions:
                    buffer:
                        description:
                            - Message string.
                        type: str
                    format:
                        description:
                            - Format flag.
                        type: str
                        choices:
                            - none
                            - text
                            - html
                            - wml
                    header:
                        description:
                            - Header flag.
                        type: str
                        choices:
                            - none
                            - http
                            - 8bit
                    msg_type:
                        description:
                            - Message type.
                        type: str
            spam:
                description:
                    - Replacement message table entries.
                type: list
                suboptions:
                    buffer:
                        description:
                            - Message string.
                        type: str
                    format:
                        description:
                            - Format flag.
                        type: str
                        choices:
                            - none
                            - text
                            - html
                            - wml
                    header:
                        description:
                            - Header flag.
                        type: str
                        choices:
                            - none
                            - http
                            - 8bit
                    msg_type:
                        description:
                            - Message type.
                        type: str
            sslvpn:
                description:
                    - Replacement message table entries.
                type: list
                suboptions:
                    buffer:
                        description:
                            - Message string.
                        type: str
                    format:
                        description:
                            - Format flag.
                        type: str
                        choices:
                            - none
                            - text
                            - html
                            - wml
                    header:
                        description:
                            - Header flag.
                        type: str
                        choices:
                            - none
                            - http
                            - 8bit
                    msg_type:
                        description:
                            - Message type.
                        type: str
            traffic_quota:
                description:
                    - Replacement message table entries.
                type: list
                suboptions:
                    buffer:
                        description:
                            - Message string.
                        type: str
                    format:
                        description:
                            - Format flag.
                        type: str
                        choices:
                            - none
                            - text
                            - html
                            - wml
                    header:
                        description:
                            - Header flag.
                        type: str
                        choices:
                            - none
                            - http
                            - 8bit
                    msg_type:
                        description:
                            - Message type.
                        type: str
            utm:
                description:
                    - Replacement message table entries.
                type: list
                suboptions:
                    buffer:
                        description:
                            - Message string.
                        type: str
                    format:
                        description:
                            - Format flag.
                        type: str
                        choices:
                            - none
                            - text
                            - html
                            - wml
                    header:
                        description:
                            - Header flag.
                        type: str
                        choices:
                            - none
                            - http
                            - 8bit
                    msg_type:
                        description:
                            - Message type.
                        type: str
            webproxy:
                description:
                    - Replacement message table entries.
                type: list
                suboptions:
                    buffer:
                        description:
                            - Message string.
                        type: str
                    format:
                        description:
                            - Format flag.
                        type: str
                        choices:
                            - none
                            - text
                            - html
                            - wml
                    header:
                        description:
                            - Header flag.
                        type: str
                        choices:
                            - none
                            - http
                            - 8bit
                    msg_type:
                        description:
                            - Message type.
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
  - name: Configure replacement message groups.
    fortios_system_replacemsg_group:
      host:  "{{ host }}"
      username: "{{ username }}"
      password: "{{ password }}"
      vdom:  "{{ vdom }}"
      https: "False"
      state: "present"
      system_replacemsg_group:
        admin:
         -
            buffer: "<your_own_value>"
            format: "none"
            header: "none"
            msg_type: "<your_own_value>"
        alertmail:
         -
            buffer: "<your_own_value>"
            format: "none"
            header: "none"
            msg_type: "<your_own_value>"
        auth:
         -
            buffer: "<your_own_value>"
            format: "none"
            header: "none"
            msg_type: "<your_own_value>"
        comment: "Comment."
        custom_message:
         -
            buffer: "<your_own_value>"
            format: "none"
            header: "none"
            msg_type: "<your_own_value>"
        device_detection_portal:
         -
            buffer: "<your_own_value>"
            format: "none"
            header: "none"
            msg_type: "<your_own_value>"
        ec:
         -
            buffer: "<your_own_value>"
            format: "none"
            header: "none"
            msg_type: "<your_own_value>"
        fortiguard_wf:
         -
            buffer: "<your_own_value>"
            format: "none"
            header: "none"
            msg_type: "<your_own_value>"
        ftp:
         -
            buffer: "<your_own_value>"
            format: "none"
            header: "none"
            msg_type: "<your_own_value>"
        group_type: "default"
        http:
         -
            buffer: "<your_own_value>"
            format: "none"
            header: "none"
            msg_type: "<your_own_value>"
        icap:
         -
            buffer: "<your_own_value>"
            format: "none"
            header: "none"
            msg_type: "<your_own_value>"
        mail:
         -
            buffer: "<your_own_value>"
            format: "none"
            header: "none"
            msg_type: "<your_own_value>"
        nac_quar:
         -
            buffer: "<your_own_value>"
            format: "none"
            header: "none"
            msg_type: "<your_own_value>"
        name: "default_name_65"
        nntp:
         -
            buffer: "<your_own_value>"
            format: "none"
            header: "none"
            msg_type: "<your_own_value>"
        spam:
         -
            buffer: "<your_own_value>"
            format: "none"
            header: "none"
            msg_type: "<your_own_value>"
        sslvpn:
         -
            buffer: "<your_own_value>"
            format: "none"
            header: "none"
            msg_type: "<your_own_value>"
        traffic_quota:
         -
            buffer: "<your_own_value>"
            format: "none"
            header: "none"
            msg_type: "<your_own_value>"
        utm:
         -
            buffer: "<your_own_value>"
            format: "none"
            header: "none"
            msg_type: "<your_own_value>"
        webproxy:
         -
            buffer: "<your_own_value>"
            format: "none"
            header: "none"
            msg_type: "<your_own_value>"
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


def filter_system_replacemsg_group_data(json):
    option_list = ['admin', 'alertmail', 'auth',
                   'comment', 'custom_message', 'device_detection_portal',
                   'ec', 'fortiguard_wf', 'ftp',
                   'group_type', 'http', 'icap',
                   'mail', 'nac_quar', 'name',
                   'nntp', 'spam', 'sslvpn',
                   'traffic_quota', 'utm', 'webproxy']
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


def system_replacemsg_group(data, fos):
    vdom = data['vdom']
    state = data['state']
    system_replacemsg_group_data = data['system_replacemsg_group']
    filtered_data = underscore_to_hyphen(filter_system_replacemsg_group_data(system_replacemsg_group_data))

    if state == "present":
        return fos.set('system',
                       'replacemsg-group',
                       data=filtered_data,
                       vdom=vdom)

    elif state == "absent":
        return fos.delete('system',
                          'replacemsg-group',
                          mkey=filtered_data['name'],
                          vdom=vdom)


def is_successful_status(status):
    return status['status'] == "success" or \
        status['http_method'] == "DELETE" and status['http_status'] == 404


def fortios_system(data, fos):

    if data['system_replacemsg_group']:
        resp = system_replacemsg_group(data, fos)

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
        "state": {"required": True, "type": "str",
                  "choices": ["present", "absent"]},
        "system_replacemsg_group": {
            "required": False, "type": "dict", "default": None,
            "options": {
                "admin": {"required": False, "type": "list",
                          "options": {
                              "buffer": {"required": False, "type": "str"},
                              "format": {"required": False, "type": "str",
                                         "choices": ["none", "text", "html",
                                                     "wml"]},
                              "header": {"required": False, "type": "str",
                                         "choices": ["none", "http", "8bit"]},
                              "msg_type": {"required": False, "type": "str"}
                          }},
                "alertmail": {"required": False, "type": "list",
                              "options": {
                                  "buffer": {"required": False, "type": "str"},
                                  "format": {"required": False, "type": "str",
                                             "choices": ["none", "text", "html",
                                                         "wml"]},
                                  "header": {"required": False, "type": "str",
                                             "choices": ["none", "http", "8bit"]},
                                  "msg_type": {"required": False, "type": "str"}
                              }},
                "auth": {"required": False, "type": "list",
                         "options": {
                             "buffer": {"required": False, "type": "str"},
                             "format": {"required": False, "type": "str",
                                        "choices": ["none", "text", "html",
                                                    "wml"]},
                             "header": {"required": False, "type": "str",
                                        "choices": ["none", "http", "8bit"]},
                             "msg_type": {"required": False, "type": "str"}
                         }},
                "comment": {"required": False, "type": "str"},
                "custom_message": {"required": False, "type": "list",
                                   "options": {
                                       "buffer": {"required": False, "type": "str"},
                                       "format": {"required": False, "type": "str",
                                                  "choices": ["none", "text", "html",
                                                              "wml"]},
                                       "header": {"required": False, "type": "str",
                                                  "choices": ["none", "http", "8bit"]},
                                       "msg_type": {"required": False, "type": "str"}
                                   }},
                "device_detection_portal": {"required": False, "type": "list",
                                            "options": {
                                                "buffer": {"required": False, "type": "str"},
                                                "format": {"required": False, "type": "str",
                                                           "choices": ["none", "text", "html",
                                                                       "wml"]},
                                                "header": {"required": False, "type": "str",
                                                           "choices": ["none", "http", "8bit"]},
                                                "msg_type": {"required": False, "type": "str"}
                                            }},
                "ec": {"required": False, "type": "list",
                       "options": {
                           "buffer": {"required": False, "type": "str"},
                           "format": {"required": False, "type": "str",
                                      "choices": ["none", "text", "html",
                                                  "wml"]},
                           "header": {"required": False, "type": "str",
                                      "choices": ["none", "http", "8bit"]},
                           "msg_type": {"required": False, "type": "str"}
                       }},
                "fortiguard_wf": {"required": False, "type": "list",
                                  "options": {
                                      "buffer": {"required": False, "type": "str"},
                                      "format": {"required": False, "type": "str",
                                                 "choices": ["none", "text", "html",
                                                             "wml"]},
                                      "header": {"required": False, "type": "str",
                                                 "choices": ["none", "http", "8bit"]},
                                      "msg_type": {"required": False, "type": "str"}
                                  }},
                "ftp": {"required": False, "type": "list",
                        "options": {
                            "buffer": {"required": False, "type": "str"},
                            "format": {"required": False, "type": "str",
                                       "choices": ["none", "text", "html",
                                                   "wml"]},
                            "header": {"required": False, "type": "str",
                                       "choices": ["none", "http", "8bit"]},
                            "msg_type": {"required": False, "type": "str"}
                        }},
                "group_type": {"required": False, "type": "str",
                               "choices": ["default", "utm", "auth",
                                           "ec"]},
                "http": {"required": False, "type": "list",
                         "options": {
                             "buffer": {"required": False, "type": "str"},
                             "format": {"required": False, "type": "str",
                                        "choices": ["none", "text", "html",
                                                    "wml"]},
                             "header": {"required": False, "type": "str",
                                        "choices": ["none", "http", "8bit"]},
                             "msg_type": {"required": False, "type": "str"}
                         }},
                "icap": {"required": False, "type": "list",
                         "options": {
                             "buffer": {"required": False, "type": "str"},
                             "format": {"required": False, "type": "str",
                                        "choices": ["none", "text", "html",
                                                    "wml"]},
                             "header": {"required": False, "type": "str",
                                        "choices": ["none", "http", "8bit"]},
                             "msg_type": {"required": False, "type": "str"}
                         }},
                "mail": {"required": False, "type": "list",
                         "options": {
                             "buffer": {"required": False, "type": "str"},
                             "format": {"required": False, "type": "str",
                                        "choices": ["none", "text", "html",
                                                    "wml"]},
                             "header": {"required": False, "type": "str",
                                        "choices": ["none", "http", "8bit"]},
                             "msg_type": {"required": False, "type": "str"}
                         }},
                "nac_quar": {"required": False, "type": "list",
                             "options": {
                                 "buffer": {"required": False, "type": "str"},
                                 "format": {"required": False, "type": "str",
                                            "choices": ["none", "text", "html",
                                                        "wml"]},
                                 "header": {"required": False, "type": "str",
                                            "choices": ["none", "http", "8bit"]},
                                 "msg_type": {"required": False, "type": "str"}
                             }},
                "name": {"required": True, "type": "str"},
                "nntp": {"required": False, "type": "list",
                         "options": {
                             "buffer": {"required": False, "type": "str"},
                             "format": {"required": False, "type": "str",
                                        "choices": ["none", "text", "html",
                                                    "wml"]},
                             "header": {"required": False, "type": "str",
                                        "choices": ["none", "http", "8bit"]},
                             "msg_type": {"required": False, "type": "str"}
                         }},
                "spam": {"required": False, "type": "list",
                         "options": {
                             "buffer": {"required": False, "type": "str"},
                             "format": {"required": False, "type": "str",
                                        "choices": ["none", "text", "html",
                                                    "wml"]},
                             "header": {"required": False, "type": "str",
                                        "choices": ["none", "http", "8bit"]},
                             "msg_type": {"required": False, "type": "str"}
                         }},
                "sslvpn": {"required": False, "type": "list",
                           "options": {
                               "buffer": {"required": False, "type": "str"},
                               "format": {"required": False, "type": "str",
                                          "choices": ["none", "text", "html",
                                                      "wml"]},
                               "header": {"required": False, "type": "str",
                                          "choices": ["none", "http", "8bit"]},
                               "msg_type": {"required": False, "type": "str"}
                           }},
                "traffic_quota": {"required": False, "type": "list",
                                  "options": {
                                      "buffer": {"required": False, "type": "str"},
                                      "format": {"required": False, "type": "str",
                                                 "choices": ["none", "text", "html",
                                                             "wml"]},
                                      "header": {"required": False, "type": "str",
                                                 "choices": ["none", "http", "8bit"]},
                                      "msg_type": {"required": False, "type": "str"}
                                  }},
                "utm": {"required": False, "type": "list",
                        "options": {
                            "buffer": {"required": False, "type": "str"},
                            "format": {"required": False, "type": "str",
                                       "choices": ["none", "text", "html",
                                                   "wml"]},
                            "header": {"required": False, "type": "str",
                                       "choices": ["none", "http", "8bit"]},
                            "msg_type": {"required": False, "type": "str"}
                        }},
                "webproxy": {"required": False, "type": "list",
                             "options": {
                                 "buffer": {"required": False, "type": "str"},
                                 "format": {"required": False, "type": "str",
                                            "choices": ["none", "text", "html",
                                                        "wml"]},
                                 "header": {"required": False, "type": "str",
                                            "choices": ["none", "http", "8bit"]},
                                 "msg_type": {"required": False, "type": "str"}
                             }}

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
