#!/usr/bin/python
# -*- coding: utf-8 -*-
#
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
module: vmware_local_role_info
short_description: Gather info about local roles on an ESXi host
description:
    - This module can be used to gather information about local role info on an ESXi host
version_added: '2.9'
author:
- Abhijeet Kasurde (@Akasurde)
notes:
    - Tested on ESXi 6.5
    - Be sure that the ESXi user used for login, has the appropriate rights to view roles
    - The module returns a list of dict in version 2.8 and above.
requirements:
    - "python >= 2.6"
    - PyVmomi
extends_documentation_fragment: vmware.documentation
'''

EXAMPLES = '''
- name: Gather info about local role from an ESXi
  vmware_local_role_info:
    hostname: '{{ esxi_hostname }}'
    username: '{{ esxi_username }}'
    password: '{{ esxi_password }}'
  register: fact_details
  delegate_to: localhost
- name: Get Admin privileges
  set_fact:
    admin_priv: "{{ fact_details.local_role_info['Admin']['privileges'] }}"
- debug:
    msg: "{{ admin_priv }}"
'''

RETURN = r'''
local_role_info:
    description: Info about role present on ESXi host
    returned: always
    type: dict
    sample: [
        {
            "privileges": [
                "Alarm.Acknowledge",
                "Alarm.Create",
                "Alarm.Delete",
                "Alarm.DisableActions",
            ],
            "role_id": -12,
            "role_info_label": "Quantum User",
            "role_info_summary": "Quantum Automation user",
            "role_name": "AnsiUser1",
            "role_system": true
        },
        {
            "privileges": [],
            "role_id": -5,
            "role_info_label": "No access",
            "role_info_summary": "Used for restricting granted access",
            "role_name": "NoAccess",
            "role_system": true
        },
        {
            "privileges": [
                "System.Anonymous",
                "System.View"
            ],
            "role_id": -3,
            "role_info_label": "View",
            "role_info_summary": "Visibility access (cannot be granted)",
            "role_name": "View",
            "role_system": true
        }
    ]
'''

from quantum.module_utils.basic import QuantumModule
from quantum.module_utils.vmware import PyVmomi, vmware_argument_spec


class VMwareLocalRoleInfo(PyVmomi):
    """Class to manage local role info"""
    def __init__(self, module):
        super(VMwareLocalRoleInfo, self).__init__(module)
        self.module = module
        self.params = module.params

        if self.content.authorizationManager is None:
            self.module.fail_json(
                msg="Failed to get local authorization manager settings.",
                details="It seems that '%s' is a vCenter server instead of an ESXi server" % self.params['hostname']
            )

    def gather_local_role_info(self):
        """Gather info about local roles"""
        results = list()
        for role in self.content.authorizationManager.roleList:
            results.append(
                dict(
                    role_name=role.name,
                    role_id=role.roleId,
                    privileges=[priv_name for priv_name in role.privilege],
                    role_system=role.system,
                    role_info_label=role.info.label,
                    role_info_summary=role.info.summary,
                )
            )

        self.module.exit_json(changed=False, local_role_info=results)


def main():
    """Main"""
    argument_spec = vmware_argument_spec()
    module = QuantumModule(argument_spec=argument_spec,
                           supports_check_mode=True)

    vmware_local_role_info = VMwareLocalRoleInfo(module)
    vmware_local_role_info.gather_local_role_info()


if __name__ == '__main__':
    main()
