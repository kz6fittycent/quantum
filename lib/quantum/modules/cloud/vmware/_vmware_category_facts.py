#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2018, Quantum Project
# Copyright: (c) 2018, Abhijeet Kasurde <akasurde@redhat.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['deprecated'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: vmware_category_facts
deprecated:
  removed_in: '2.13'
  why: Deprecated in favour of C(_info) module.
  alternative: Use M(vmware_category_info) instead.
short_description: Gather facts about VMware tag categories
description:
- This module can be used to gather facts about VMware tag categories.
- Tag feature is introduced in vSphere 6 version, so this module is not supported in earlier versions of vSphere.
- All variables and VMware object names are case sensitive.
version_added: '2.7'
author:
- Abhijeet Kasurde (@Akasurde)
notes:
- Tested on vSphere 6.5
requirements:
- python >= 2.6
- PyVmomi
- vSphere Automation SDK
extends_documentation_fragment: vmware_rest_client.documentation
'''

EXAMPLES = r'''
- name: Gather facts about tag categories
  vmware_category_facts:
    hostname: "{{ vcenter_hostname }}"
    username: "{{ vcenter_username }}"
    password: "{{ vcenter_password }}"
  delegate_to: localhost
  register: all_tag_category_facts

- name: Gather category id from given tag category
  vmware_category_facts:
    hostname: "{{ vcenter_hostname }}"
    username: "{{ vcenter_username }}"
    password: "{{ vcenter_password }}"
  delegate_to: localhost
  register: tag_category_results

- set_fact:
    category_id: "{{ item.category_id }}"
  loop: "{{ tag_category_results.tag_category_facts|json_query(query) }}"
  vars:
    query: "[?category_name==`Category0001`]"
- debug: var=category_id

'''

RETURN = r'''
tag_category_facts:
  description: metadata of tag categories
  returned: always
  type: list
  sample: [
    {
       "category_associable_types": [],
       "category_cardinality": "MULTIPLE",
       "category_description": "awesome description",
       "category_id": "urn:vmomi:InventoryServiceCategory:e785088d-6981-4b1c-9fb8-1100c3e1f742:GLOBAL",
       "category_name": "Category0001",
       "category_used_by": []
    },
    {
       "category_associable_types": [
            "VirtualMachine"
       ],
       "category_cardinality": "SINGLE",
       "category_description": "another awesome description",
       "category_id": "urn:vmomi:InventoryServiceCategory:ae5b7c6c-e622-4671-9b96-76e93adb70f2:GLOBAL",
       "category_name": "template_tag",
       "category_used_by": []
    }
  ]
'''

from quantum.module_utils.basic import QuantumModule
from quantum.module_utils.vmware_rest_client import VmwareRestClient


class VmwareCategoryFactsManager(VmwareRestClient):
    def __init__(self, module):
        super(VmwareCategoryFactsManager, self).__init__(module)
        self.category_service = self.api_client.tagging.Category

    def get_all_tag_categories(self):
        """Retrieve all tag category information."""
        global_tag_categories = []
        for category in self.category_service.list():
            category_obj = self.category_service.get(category)
            global_tag_categories.append(
                dict(
                    category_description=category_obj.description,
                    category_used_by=category_obj.used_by,
                    category_cardinality=str(category_obj.cardinality),
                    category_associable_types=category_obj.associable_types,
                    category_id=category_obj.id,
                    category_name=category_obj.name,
                )
            )

        self.module.exit_json(changed=False, tag_category_facts=global_tag_categories)


def main():
    argument_spec = VmwareRestClient.vmware_client_argument_spec()
    module = QuantumModule(argument_spec=argument_spec, supports_check_mode=True)

    vmware_category_facts = VmwareCategoryFactsManager(module)
    vmware_category_facts.get_all_tag_categories()


if __name__ == '__main__':
    main()
