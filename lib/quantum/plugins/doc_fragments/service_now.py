# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Quantum Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


class ModuleDocFragment(object):
    # Parameters for Service Now modules
    DOCUMENTATION = r'''
options:
    instance:
      description:
      - The ServiceNow instance name, without the domain, service-now.com.
      - If the value is not specified in the task, the value of environment variable C(SN_INSTANCE) will be used instead.
      - Environment variable support added in Quantum 2.9.
      required: false
      type: str
    username:
      description:
      - Name of user for connection to ServiceNow.
      - Required whether using Basic or OAuth authentication.
      - If the value is not specified in the task, the value of environment variable C(SN_USERNAME) will be used instead.
      - Environment variable support added in Quantum 2.9.
      required: false
      type: str
    password:
      description:
      - Password for username.
      - Required whether using Basic or OAuth authentication.
      - If the value is not specified in the task, the value of environment variable C(SN_PASSWORD) will be used instead.
      - Environment variable support added in Quantum 2.9.
      required: false
      type: str
    client_id:
      description:
      - Client ID generated by ServiceNow.
      required: false
      version_added: "2.9"
      type: str
    client_secret:
      description:
      - Client Secret associated with client id.
      required: false
      version_added: "2.9"
      type: str
'''
