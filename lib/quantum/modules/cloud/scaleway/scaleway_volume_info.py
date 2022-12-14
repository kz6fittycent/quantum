#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# (c) 2018, Yanis Guenane <yanis+quantum@guenane.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: scaleway_volume_info
short_description: Gather information about the Scaleway volumes available.
description:
  - Gather information about the Scaleway volumes available.
version_added: "2.9"
author:
  - "Yanis Guenane (@Spredzy)"
  - "Remy Leone (@sieben)"
extends_documentation_fragment: scaleway
options:
  region:
    description:
      - Scaleway region to use (for example C(par1)).
    required: true
    choices:
      - ams1
      - EMEA-NL-EVS
      - par1
      - EMEA-FR-PAR1
'''

EXAMPLES = r'''
- name: Gather Scaleway volumes information
  scaleway_volume_info:
    region: par1
  register: result

- debug:
    msg: "{{ result.scaleway_volume_info }}"
'''

RETURN = r'''
---
scaleway_volume_info:
  description: Response from Scaleway API
  returned: success
  type: complex
  sample:
    "scaleway_volume_info": [
        {
            "creation_date": "2018-08-14T20:56:24.949660+00:00",
            "export_uri": null,
            "id": "b8d51a06-daeb-4fef-9539-a8aea016c1ba",
            "modification_date": "2018-08-14T20:56:24.949660+00:00",
            "name": "test-volume",
            "organization": "3f709602-5e6c-4619-b80c-e841c89734af",
            "server": null,
            "size": 50000000000,
            "state": "available",
            "volume_type": "l_ssd"
        }
    ]
'''

from quantum.module_utils.basic import QuantumModule
from quantum.module_utils.scaleway import (
    Scaleway, ScalewayException, scaleway_argument_spec,
    SCALEWAY_LOCATION)


class ScalewayVolumeInfo(Scaleway):

    def __init__(self, module):
        super(ScalewayVolumeInfo, self).__init__(module)
        self.name = 'volumes'

        region = module.params["region"]
        self.module.params['api_url'] = SCALEWAY_LOCATION[region]["api_endpoint"]


def main():
    argument_spec = scaleway_argument_spec()
    argument_spec.update(dict(
        region=dict(required=True, choices=SCALEWAY_LOCATION.keys()),
    ))

    module = QuantumModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    try:
        module.exit_json(
            scaleway_volume_info=ScalewayVolumeInfo(module).get_resources()
        )
    except ScalewayException as exc:
        module.fail_json(msg=exc.message)


if __name__ == '__main__':
    main()
