#!/usr/bin/python
# Copyright (c) 2016-2017 Hewlett Packard Enterprise Development LP
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_fc_network_info
short_description: Retrieve the information about one or more of the OneView Fibre Channel Networks
description:
    - Retrieve the information about one or more of the Fibre Channel Networks from OneView.
    - This module was called C(oneview_fc_network_facts) before Quantum 2.9, returning C(quantum_facts).
      Note that the M(oneview_fc_network_info) module no longer returns C(quantum_facts)!
version_added: "2.4"
requirements:
    - hpOneView >= 2.0.1
author:
    - Felipe Bulsoni (@fgbulsoni)
    - Thiago Miotto (@tmiotto)
    - Adriane Cardozo (@adriane-cardozo)
options:
    name:
      description:
        - Fibre Channel Network name.

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather information about all Fibre Channel Networks
  oneview_fc_network_info:
    config: /etc/oneview/oneview_config.json
  delegate_to: localhost
  register: result

- debug:
    msg: "{{ result.fc_networks }}"

- name: Gather paginated, filtered and sorted information about Fibre Channel Networks
  oneview_fc_network_info:
    config: /etc/oneview/oneview_config.json
    params:
      start: 1
      count: 3
      sort: 'name:descending'
      filter: 'fabricType=FabricAttach'
  delegate_to: localhost
  register: result
- debug:
    msg: "{{ result.fc_networks }}"

- name: Gather information about a Fibre Channel Network by name
  oneview_fc_network_info:
    config: /etc/oneview/oneview_config.json
    name: network name
  delegate_to: localhost
  register: result

- debug:
    msg: "{{ result.fc_networks }}"
'''

RETURN = '''
fc_networks:
    description: Has all the OneView information about the Fibre Channel Networks.
    returned: Always, but can be null.
    type: dict
'''

from quantum.module_utils.oneview import OneViewModuleBase


class FcNetworkInfoModule(OneViewModuleBase):
    def __init__(self):

        argument_spec = dict(
            name=dict(required=False, type='str'),
            params=dict(required=False, type='dict')
        )

        super(FcNetworkInfoModule, self).__init__(additional_arg_spec=argument_spec)
        self.is_old_facts = self.module._name == 'oneview_fc_network_facts'
        if self.is_old_facts:
            self.module.deprecate("The 'oneview_fc_network_facts' module has been renamed to 'oneview_fc_network_info', "
                                  "and the renamed one no longer returns quantum_facts", version='2.13')

    def execute_module(self):

        if self.module.params['name']:
            fc_networks = self.oneview_client.fc_networks.get_by('name', self.module.params['name'])
        else:
            fc_networks = self.oneview_client.fc_networks.get_all(**self.facts_params)

        if self.is_old_facts:
            return dict(changed=False, quantum_facts=dict(fc_networks=fc_networks))
        else:
            return dict(changed=False, fc_networks=fc_networks)


def main():
    FcNetworkInfoModule().run()


if __name__ == '__main__':
    main()
