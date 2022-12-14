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
module: aci_epg
short_description: Manage End Point Groups (EPG) objects (fv:AEPg)
description:
- Manage End Point Groups (EPG) on Cisco ACI fabrics.
version_added: '2.4'
options:
  tenant:
    description:
    - Name of an existing tenant.
    type: str
    aliases: [ tenant_name ]
  ap:
    description:
    - Name of an existing application network profile, that will contain the EPGs.
    type: str
    required: yes
    aliases: [ app_profile, app_profile_name ]
  epg:
    description:
    - Name of the end point group.
    type: str
    required: yes
    aliases: [ epg_name, name ]
  bd:
    description:
    - Name of the bridge domain being associated with the EPG.
    type: str
    aliases: [ bd_name, bridge_domain ]
  priority:
    description:
    - The QoS class.
    - The APIC defaults to C(unspecified) when unset during creation.
    type: str
    choices: [ level1, level2, level3, unspecified ]
  intra_epg_isolation:
    description:
    - The Intra EPG Isolation.
    - The APIC defaults to C(unenforced) when unset during creation.
    type: str
    choices: [ enforced, unenforced ]
  description:
    description:
    - Description for the EPG.
    type: str
    aliases: [ descr ]
  fwd_control:
    description:
    - The forwarding control used by the EPG.
    - The APIC defaults to C(none) when unset during creation.
    type: str
    choices: [ none, proxy-arp ]
  preferred_group:
    description:
    - Whether ot not the EPG is part of the Preferred Group and can communicate without contracts.
    - This is very convenient for migration scenarios, or when ACI is used for network automation but not for policy.
    - The APIC defaults to C(no) when unset during creation.
    type: bool
    version_added: '2.5'
  state:
    description:
    - Use C(present) or C(absent) for adding or removing.
    - Use C(query) for listing an object or multiple objects.
    type: str
    choices: [ absent, present, query ]
    default: present
extends_documentation_fragment: aci
notes:
- The C(tenant) and C(app_profile) used must exist before using this module in your coupling.
  The M(aci_tenant) and M(aci_ap) modules can be used for this.
seealso:
- module: aci_tenant
- module: aci_ap
- name: APIC Management Information Model reference
  description: More information about the internal APIC class B(fv:AEPg).
  link: https://developer.cisco.com/docs/apic-mim-ref/
author:
- Swetha Chunduri (@schunduri)
'''

EXAMPLES = r'''
- name: Add a new EPG
  aci_epg:
    host: apic
    username: admin
    password: SomeSecretPassword
    tenant: production
    ap: intranet
    epg: web_epg
    description: Web Intranet EPG
    bd: prod_bd
    preferred_group: yes
    state: present
  delegate_to: localhost

- aci_epg:
    host: apic
    username: admin
    password: SomeSecretPassword
    tenant: production
    ap: ticketing
    epg: "{{ item.epg }}"
    description: Ticketing EPG
    bd: "{{ item.bd }}"
    priority: unspecified
    intra_epg_isolation: unenforced
    state: present
  delegate_to: localhost
  with_items:
    - epg: web
      bd: web_bd
    - epg: database
      bd: database_bd

- name: Remove an EPG
  aci_epg:
    host: apic
    username: admin
    password: SomeSecretPassword
    validate_certs: no
    tenant: production
    app_profile: intranet
    epg: web_epg
    state: absent
  delegate_to: localhost

- name: Query an EPG
  aci_epg:
    host: apic
    username: admin
    password: SomeSecretPassword
    tenant: production
    ap: ticketing
    epg: web_epg
    state: query
  delegate_to: localhost
  register: query_result

- name: Query all EPGs
  aci_epg:
    host: apic
    username: admin
    password: SomeSecretPassword
    state: query
  delegate_to: localhost
  register: query_result

- name: Query all EPGs with a Specific Name
  aci_epg:
    host: apic
    username: admin
    password: SomeSecretPassword
    validate_certs: no
    epg: web_epg
    state: query
  delegate_to: localhost
  register: query_result

- name: Query all EPGs of an App Profile
  aci_epg:
    host: apic
    username: admin
    password: SomeSecretPassword
    validate_certs: no
    ap: ticketing
    state: query
  delegate_to: localhost
  register: query_result
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
        epg=dict(type='str', aliases=['epg_name', 'name']),  # Not required for querying all objects
        bd=dict(type='str', aliases=['bd_name', 'bridge_domain']),
        ap=dict(type='str', aliases=['app_profile', 'app_profile_name']),  # Not required for querying all objects
        tenant=dict(type='str', aliases=['tenant_name']),  # Not required for querying all objects
        description=dict(type='str', aliases=['descr']),
        priority=dict(type='str', choices=['level1', 'level2', 'level3', 'unspecified']),
        intra_epg_isolation=dict(choices=['enforced', 'unenforced']),
        fwd_control=dict(type='str', choices=['none', 'proxy-arp']),
        preferred_group=dict(type='bool'),
        state=dict(type='str', default='present', choices=['absent', 'present', 'query']),
    )

    module = QuantumModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[
            ['state', 'absent', ['ap', 'epg', 'tenant']],
            ['state', 'present', ['ap', 'epg', 'tenant']],
        ],
    )

    aci = ACIModule(module)

    epg = module.params['epg']
    bd = module.params['bd']
    description = module.params['description']
    priority = module.params['priority']
    intra_epg_isolation = module.params['intra_epg_isolation']
    fwd_control = module.params['fwd_control']
    preferred_group = aci.boolean(module.params['preferred_group'], 'include', 'exclude')
    state = module.params['state']
    tenant = module.params['tenant']
    ap = module.params['ap']

    aci.construct_url(
        root_class=dict(
            aci_class='fvTenant',
            aci_rn='tn-{0}'.format(tenant),
            module_object=tenant,
            target_filter={'name': tenant},
        ),
        subclass_1=dict(
            aci_class='fvAp',
            aci_rn='ap-{0}'.format(ap),
            module_object=ap,
            target_filter={'name': ap},
        ),
        subclass_2=dict(
            aci_class='fvAEPg',
            aci_rn='epg-{0}'.format(epg),
            module_object=epg,
            target_filter={'name': epg},
        ),
        child_classes=['fvRsBd'],
    )

    aci.get_existing()

    if state == 'present':
        aci.payload(
            aci_class='fvAEPg',
            class_config=dict(
                name=epg,
                descr=description,
                prio=priority,
                pcEnfPref=intra_epg_isolation,
                fwdCtrl=fwd_control,
                prefGrMemb=preferred_group,
            ),
            child_configs=[dict(
                fvRsBd=dict(
                    attributes=dict(
                        tnFvBDName=bd,
                    ),
                ),
            )],
        )

        aci.get_diff(aci_class='fvAEPg')

        aci.post_config()

    elif state == 'absent':
        aci.delete_config()

    aci.exit_json()


if __name__ == "__main__":
    main()
