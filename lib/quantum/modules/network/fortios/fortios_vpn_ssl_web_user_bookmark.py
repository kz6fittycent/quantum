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
module: fortios_vpn_ssl_web_user_bookmark
short_description: Configure SSL VPN user bookmark in Fortinet's FortiOS and FortiGate.
description:
    - This module is able to configure a FortiGate or FortiOS (FOS) device by allowing the
      user to set and modify vpn_ssl_web feature and user_bookmark category.
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
    vpn_ssl_web_user_bookmark:
        description:
            - Configure SSL VPN user bookmark.
        default: null
        type: dict
        suboptions:
            bookmarks:
                description:
                    - Bookmark table.
                type: list
                suboptions:
                    additional_params:
                        description:
                            - Additional parameters.
                        type: str
                    apptype:
                        description:
                            - Application type.
                        type: str
                        choices:
                            - citrix
                            - ftp
                            - portforward
                            - rdp
                            - smb
                            - ssh
                            - telnet
                            - vnc
                            - web
                    description:
                        description:
                            - Description.
                        type: str
                    folder:
                        description:
                            - Network shared file folder parameter.
                        type: str
                    form_data:
                        description:
                            - Form data.
                        type: list
                        suboptions:
                            name:
                                description:
                                    - Name.
                                required: true
                                type: str
                            value:
                                description:
                                    - Value.
                                type: str
                    host:
                        description:
                            - Host name/IP parameter.
                        type: str
                    listening_port:
                        description:
                            - Listening port (0 - 65535).
                        type: int
                    load_balancing_info:
                        description:
                            - The load balancing information or cookie which should be provided to the connection broker.
                        type: str
                    logon_password:
                        description:
                            - Logon password.
                        type: str
                    logon_user:
                        description:
                            - Logon user.
                        type: str
                    name:
                        description:
                            - Bookmark name.
                        required: true
                        type: str
                    port:
                        description:
                            - Remote port.
                        type: int
                    preconnection_blob:
                        description:
                            - An arbitrary string which identifies the RDP source.
                        type: str
                    preconnection_id:
                        description:
                            - The numeric ID of the RDP source (0-2147483648).
                        type: int
                    remote_port:
                        description:
                            - Remote port (0 - 65535).
                        type: int
                    security:
                        description:
                            - Security mode for RDP connection.
                        type: str
                        choices:
                            - rdp
                            - nla
                            - tls
                            - any
                    server_layout:
                        description:
                            - Server side keyboard layout.
                        type: str
                        choices:
                            - de-de-qwertz
                            - en-gb-qwerty
                            - en-us-qwerty
                            - es-es-qwerty
                            - fr-fr-azerty
                            - fr-ch-qwertz
                            - it-it-qwerty
                            - ja-jp-qwerty
                            - pt-br-qwerty
                            - sv-se-qwerty
                            - tr-tr-qwerty
                            - failsafe
                    show_status_window:
                        description:
                            - Enable/disable showing of status window.
                        type: str
                        choices:
                            - enable
                            - disable
                    sso:
                        description:
                            - Single Sign-On.
                        type: str
                        choices:
                            - disable
                            - static
                            - auto
                    sso_credential:
                        description:
                            - Single sign-on credentials.
                        type: str
                        choices:
                            - sslvpn-login
                            - alternative
                    sso_credential_sent_once:
                        description:
                            - Single sign-on credentials are only sent once to remote server.
                        type: str
                        choices:
                            - enable
                            - disable
                    sso_password:
                        description:
                            - SSO password.
                        type: str
                    sso_username:
                        description:
                            - SSO user name.
                        type: str
                    url:
                        description:
                            - URL parameter.
                        type: str
            custom_lang:
                description:
                    - Personal language. Source system.custom-language.name.
                type: str
            name:
                description:
                    - User and group name.
                required: true
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
  - name: Configure SSL VPN user bookmark.
    fortios_vpn_ssl_web_user_bookmark:
      host:  "{{ host }}"
      username: "{{ username }}"
      password: "{{ password }}"
      vdom:  "{{ vdom }}"
      https: "False"
      state: "present"
      vpn_ssl_web_user_bookmark:
        bookmarks:
         -
            additional_params: "<your_own_value>"
            apptype: "citrix"
            description: "<your_own_value>"
            folder: "<your_own_value>"
            form_data:
             -
                name: "default_name_9"
                value: "<your_own_value>"
            host: "<your_own_value>"
            listening_port: "12"
            load_balancing_info: "<your_own_value>"
            logon_password: "<your_own_value>"
            logon_user: "<your_own_value>"
            name: "default_name_16"
            port: "17"
            preconnection_blob: "<your_own_value>"
            preconnection_id: "19"
            remote_port: "20"
            security: "rdp"
            server_layout: "de-de-qwertz"
            show_status_window: "enable"
            sso: "disable"
            sso_credential: "sslvpn-login"
            sso_credential_sent_once: "enable"
            sso_password: "<your_own_value>"
            sso_username: "<your_own_value>"
            url: "myurl.com"
        custom_lang: "<your_own_value> (source system.custom-language.name)"
        name: "default_name_31"
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


def filter_vpn_ssl_web_user_bookmark_data(json):
    option_list = ['bookmarks', 'custom_lang', 'name']
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


def vpn_ssl_web_user_bookmark(data, fos):
    vdom = data['vdom']
    state = data['state']
    vpn_ssl_web_user_bookmark_data = data['vpn_ssl_web_user_bookmark']
    filtered_data = underscore_to_hyphen(filter_vpn_ssl_web_user_bookmark_data(vpn_ssl_web_user_bookmark_data))

    if state == "present":
        return fos.set('vpn.ssl.web',
                       'user-bookmark',
                       data=filtered_data,
                       vdom=vdom)

    elif state == "absent":
        return fos.delete('vpn.ssl.web',
                          'user-bookmark',
                          mkey=filtered_data['name'],
                          vdom=vdom)


def is_successful_status(status):
    return status['status'] == "success" or \
        status['http_method'] == "DELETE" and status['http_status'] == 404


def fortios_vpn_ssl_web(data, fos):

    if data['vpn_ssl_web_user_bookmark']:
        resp = vpn_ssl_web_user_bookmark(data, fos)

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
        "vpn_ssl_web_user_bookmark": {
            "required": False, "type": "dict", "default": None,
            "options": {
                "bookmarks": {"required": False, "type": "list",
                              "options": {
                                  "additional_params": {"required": False, "type": "str"},
                                  "apptype": {"required": False, "type": "str",
                                              "choices": ["citrix", "ftp", "portforward",
                                                          "rdp", "smb", "ssh",
                                                          "telnet", "vnc", "web"]},
                                  "description": {"required": False, "type": "str"},
                                  "folder": {"required": False, "type": "str"},
                                  "form_data": {"required": False, "type": "list",
                                                "options": {
                                                    "name": {"required": True, "type": "str"},
                                                    "value": {"required": False, "type": "str"}
                                                }},
                                  "host": {"required": False, "type": "str"},
                                  "listening_port": {"required": False, "type": "int"},
                                  "load_balancing_info": {"required": False, "type": "str"},
                                  "logon_password": {"required": False, "type": "str", "no_log": True},
                                  "logon_user": {"required": False, "type": "str"},
                                  "name": {"required": True, "type": "str"},
                                  "port": {"required": False, "type": "int"},
                                  "preconnection_blob": {"required": False, "type": "str"},
                                  "preconnection_id": {"required": False, "type": "int"},
                                  "remote_port": {"required": False, "type": "int"},
                                  "security": {"required": False, "type": "str",
                                               "choices": ["rdp", "nla", "tls",
                                                           "any"]},
                                  "server_layout": {"required": False, "type": "str",
                                                    "choices": ["de-de-qwertz", "en-gb-qwerty", "en-us-qwerty",
                                                                "es-es-qwerty", "fr-fr-azerty", "fr-ch-qwertz",
                                                                "it-it-qwerty", "ja-jp-qwerty", "pt-br-qwerty",
                                                                "sv-se-qwerty", "tr-tr-qwerty", "failsafe"]},
                                  "show_status_window": {"required": False, "type": "str",
                                                         "choices": ["enable", "disable"]},
                                  "sso": {"required": False, "type": "str",
                                          "choices": ["disable", "static", "auto"]},
                                  "sso_credential": {"required": False, "type": "str",
                                                     "choices": ["sslvpn-login", "alternative"]},
                                  "sso_credential_sent_once": {"required": False, "type": "str",
                                                               "choices": ["enable", "disable"]},
                                  "sso_password": {"required": False, "type": "str", "no_log": True},
                                  "sso_username": {"required": False, "type": "str"},
                                  "url": {"required": False, "type": "str"}
                              }},
                "custom_lang": {"required": False, "type": "str"},
                "name": {"required": True, "type": "str"}

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

            is_error, has_changed, result = fortios_vpn_ssl_web(module.params, fos)
        else:
            module.fail_json(**FAIL_SOCKET_MSG)
    else:
        try:
            from fortiosapi import FortiOSAPI
        except ImportError:
            module.fail_json(msg="fortiosapi module is required")

        fos = FortiOSAPI()

        login(module.params, fos)
        is_error, has_changed, result = fortios_vpn_ssl_web(module.params, fos)
        fos.logout()

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Error in repo", meta=result)


if __name__ == '__main__':
    main()
