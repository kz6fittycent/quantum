#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'certified'}

DOCUMENTATION = r'''
---
module: aci_interface_policy_fc
short_description: Manage Fibre Channel interface policies (fc:IfPol)
description:
- Manage ACI Fiber Channel interface policies on Cisco ACI fabrics.
version_added: '2.4'
options:
  fc_policy:
    description:
    - The name of the Fiber Channel interface policy.
    type: str
    required: yes
    aliases: [ name ]
  description:
    description:
    - The description of the Fiber Channel interface policy.
    type: str
    aliases: [ descr ]
  port_mode:
    description:
    - The Port Mode to use.
    - The APIC defaults to C(f) when unset during creation.
    type: str
    choices: [ f, np ]
  state:
    description:
    - Use C(present) or C(absent) for adding or removing.
    - Use C(query) for listing an object or multiple objects.
    type: str
    choices: [ absent, present, query ]
    default: present
extends_documentation_fragment: aci
seealso:
- name: APIC Management Information Model reference
  description: More information about the internal APIC class B(fc:IfPol).
  link: https://developer.cisco.com/docs/apic-mim-ref/
author:
- Dag Wieers (@dagwieers)
'''

EXAMPLES = r'''
- aci_interface_policy_fc:
    host: '{{ hostname }}'
    username: '{{ username }}'
    password: '{{ password }}'
    fc_policy: '{{ fc_policy }}'
    port_mode: '{{ port_mode }}'
    description: '{{ description }}'
    state: present
  delegate_to: localhost
'''

RETURN = r'''
current:
  description: The existing configuration from the APIC after the module has finished
  returned: success
  type: list
  sample:
    [
        {
            "fvTenant": {
                "attributes": {
                    "descr": "Production environment",
                    "dn": "uni/tn-production",
                    "name": "production",
                    "nameAlias": "",
                    "ownerKey": "",
                    "ownerTag": ""
                }
            }
        }
    ]
error:
  description: The error information as returned from the APIC
  returned: failure
  type: dict
  sample:
    {
        "code": "122",
        "text": "unknown managed object class foo"
    }
raw:
  description: The raw output returned by the APIC REST API (xml or json)
  returned: parse error
  type: str
  sample: '<?xml version="1.0" encoding="UTF-8"?><imdata totalCount="1"><error code="122" text="unknown managed object class foo"/></imdata>'
sent:
  description: The actual/minimal configuration pushed to the APIC
  returned: info
  type: list
  sample:
    {
        "fvTenant": {
            "attributes": {
                "descr": "Production environment"
            }
        }
    }
previous:
  description: The original configuration from the APIC before the module has started
  returned: info
  type: list
  sample:
    [
        {
            "fvTenant": {
                "attributes": {
                    "descr": "Production",
                    "dn": "uni/tn-production",
                    "name": "production",
                    "nameAlias": "",
                    "ownerKey": "",
                    "ownerTag": ""
                }
            }
        }
    ]
proposed:
  description: The assembled configuration from the user-provided parameters
  returned: info
  type: dict
  sample:
    {
        "fvTenant": {
            "attributes": {
                "descr": "Production environment",
                "name": "production"
            }
        }
    }
filter_string:
  description: The filter string used for the request
  returned: failure or debug
  type: str
  sample: ?rsp-prop-include=config-only
method:
  description: The HTTP method used for the request to the APIC
  returned: failure or debug
  type: str
  sample: POST
response:
  description: The HTTP response from the APIC
  returned: failure or debug
  type: str
  sample: OK (30 bytes)
status:
  description: The HTTP status from the APIC
  returned: failure or debug
  type: int
  sample: 200
url:
  description: The HTTP url used for the request to the APIC
  returned: failure or debug
  type: str
  sample: https://10.11.12.13/api/mo/uni/tn-production.json
'''

from quantum.module_utils.basic import QuantumModule
from quantum.module_utils.network.aci.aci import ACIModule, aci_argument_spec


def main():
    argument_spec = aci_argument_spec()
    argument_spec.update(
        fc_policy=dict(type='str', aliases=['name']),  # Not required for querying all objects
        description=dict(type='str', aliases=['descr']),
        port_mode=dict(type='str', choices=['f', 'np']),  # No default provided on purpose
        state=dict(type='str', default='present', choices=['absent', 'present', 'query']),
    )

    module = QuantumModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[
            ['state', 'absent', ['fc_policy']],
            ['state', 'present', ['fc_policy']],
        ],
    )

    fc_policy = module.params['fc_policy']
    port_mode = module.params['port_mode']
    description = module.params['description']
    state = module.params['state']

    aci = ACIModule(module)
    aci.construct_url(
        root_class=dict(
            aci_class='fcIfPol',
            aci_rn='infra/fcIfPol-{0}'.format(fc_policy),
            module_object=fc_policy,
            target_filter={'name': fc_policy},
        ),
    )

    aci.get_existing()

    if state == 'present':
        aci.payload(
            aci_class='fcIfPol',
            class_config=dict(
                name=fc_policy,
                descr=description,
                portMode=port_mode,
            ),
        )

        aci.get_diff(aci_class='fcIfPol')

        aci.post_config()

    elif state == 'absent':
        aci.delete_config()

    aci.exit_json()


if __name__ == "__main__":
    main()
