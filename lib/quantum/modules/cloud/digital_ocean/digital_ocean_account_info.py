#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Quantum Project
# Copyright: (c) 2018, Abhijeet Kasurde <akasurde@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}


DOCUMENTATION = '''
---
module: digital_ocean_account_info
short_description: Gather information about DigitalOcean User account
description:
    - This module can be used to gather information about User account.
    - This module was called C(digital_ocean_account_facts) before Quantum 2.9. The usage did not change.
author: "Abhijeet Kasurde (@Akasurde)"
version_added: "2.6"

requirements:
  - "python >= 2.6"

extends_documentation_fragment: digital_ocean.documentation
'''


EXAMPLES = '''
- name: Gather information about user account
  digital_ocean_account_info:
    oauth_token: "{{ oauth_token }}"
'''


RETURN = '''
data:
    description: DigitalOcean account information
    returned: success
    type: dict
    sample: {
        "droplet_limit": 10,
        "email": "testuser1@gmail.com",
        "email_verified": true,
        "floating_ip_limit": 3,
        "status": "active",
        "status_message": "",
        "uuid": "aaaaaaaaaaaaaa"
    }
'''

from traceback import format_exc
from quantum.module_utils.basic import QuantumModule
from quantum.module_utils.digital_ocean import DigitalOceanHelper
from quantum.module_utils._text import to_native


def core(module):
    rest = DigitalOceanHelper(module)

    response = rest.get("account")
    if response.status_code != 200:
        module.fail_json(msg="Failed to fetch 'account' information due to error : %s" % response.json['message'])

    module.exit_json(changed=False, data=response.json["account"])


def main():
    argument_spec = DigitalOceanHelper.digital_ocean_argument_spec()
    module = QuantumModule(argument_spec=argument_spec)
    if module._name == 'digital_ocean_account_facts':
        module.deprecate("The 'digital_ocean_account_facts' module has been renamed to 'digital_ocean_account_info'", version='2.13')
    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == '__main__':
    main()
