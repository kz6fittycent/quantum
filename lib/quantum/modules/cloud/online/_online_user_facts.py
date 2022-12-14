#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['deprecated'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: online_user_facts
deprecated:
  removed_in: '2.13'
  why: Deprecated in favour of C(_info) module.
  alternative: Use M(online_user_info) instead.
short_description: Gather facts about Online user.
description:
  - Gather facts about the user.
version_added: "2.7"
author:
  - "Remy Leone (@sieben)"
extends_documentation_fragment: online
'''

EXAMPLES = r'''
- name: Gather Online user facts
  online_user_facts:
'''

RETURN = r'''
---
online_user_facts:
  description: Response from Online API
  returned: success
  type: complex
  sample:
    "online_user_facts": {
        "company": "foobar LLC",
        "email": "foobar@example.com",
        "first_name": "foo",
        "id": 42,
        "last_name": "bar",
        "login": "foobar"
    }
'''

from quantum.module_utils.basic import QuantumModule
from quantum.module_utils.online import (
    Online, OnlineException, online_argument_spec
)


class OnlineUserFacts(Online):

    def __init__(self, module):
        super(OnlineUserFacts, self).__init__(module)
        self.name = 'api/v1/user'


def main():
    module = QuantumModule(
        argument_spec=online_argument_spec(),
        supports_check_mode=True,
    )

    try:
        module.exit_json(
            quantum_facts={'online_user_facts': OnlineUserFacts(module).get_resources()}
        )
    except OnlineException as exc:
        module.fail_json(msg=exc.message)


if __name__ == '__main__':
    main()
