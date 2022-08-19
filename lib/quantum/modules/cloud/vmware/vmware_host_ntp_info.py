#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2018, Abhijeet Kasurde <akasurde@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: vmware_host_ntp_info
short_description: Gathers info about NTP configuration on an ESXi host
description:
- This module can be used to gather information about NTP configurations on an ESXi host.
version_added: '2.9'
author:
- Abhijeet Kasurde (@Akasurde)
notes:
- Tested on vSphere 6.5
requirements:
- python >= 2.6
- PyVmomi
options:
  cluster_name:
    description:
    - Name of the cluster.
    - NTP config information about each ESXi server will be returned for the given cluster.
    - If C(esxi_hostname) is not given, this parameter is required.
    type: str
  esxi_hostname:
    description:
    - ESXi hostname.
    - NTP config information about this ESXi server will be returned.
    - If C(cluster_name) is not given, this parameter is required.
    type: str
extends_documentation_fragment: vmware.documentation
'''

EXAMPLES = r'''
- name: Gather NTP info about all ESXi Host in the given Cluster
  vmware_host_ntp_info:
    hostname: '{{ vcenter_hostname }}'
    username: '{{ vcenter_username }}'
    password: '{{ vcenter_password }}'
    cluster_name: cluster_name
  delegate_to: localhost
  register: cluster_host_ntp

- name: Gather NTP info about ESXi Host
  vmware_host_ntp_info:
    hostname: '{{ vcenter_hostname }}'
    username: '{{ vcenter_username }}'
    password: '{{ vcenter_password }}'
    esxi_hostname: '{{ esxi_hostname }}'
  delegate_to: localhost
  register: host_ntp
'''

RETURN = r'''
hosts_ntp_info:
    description:
    - dict with hostname as key and dict with NTP infos as value
    returned: hosts_ntp_info
    type: dict
    sample: {
        "10.76.33.226": [
            {
                "ntp_servers": [],
                "time_zone_description": "UTC",
                "time_zone_gmt_offset": 0,
                "time_zone_identifier": "UTC",
                "time_zone_name": "UTC"
            }
        ]
    }
'''

from quantum.module_utils.basic import QuantumModule
from quantum.module_utils.vmware import vmware_argument_spec, PyVmomi


class VmwareNtpInfoManager(PyVmomi):
    def __init__(self, module):
        super(VmwareNtpInfoManager, self).__init__(module)
        cluster_name = self.params.get('cluster_name', None)
        esxi_host_name = self.params.get('esxi_hostname', None)
        self.hosts = self.get_all_host_objs(cluster_name=cluster_name, esxi_host_name=esxi_host_name)

    def gather_ntp_info(self):
        hosts_info = {}
        for host in self.hosts:
            host_ntp_info = []
            host_date_time_manager = host.configManager.dateTimeSystem
            if host_date_time_manager:
                host_ntp_info.append(
                    dict(
                        time_zone_identifier=host_date_time_manager.dateTimeInfo.timeZone.key,
                        time_zone_name=host_date_time_manager.dateTimeInfo.timeZone.name,
                        time_zone_description=host_date_time_manager.dateTimeInfo.timeZone.description,
                        time_zone_gmt_offset=host_date_time_manager.dateTimeInfo.timeZone.gmtOffset,
                        ntp_servers=[ntp_server for ntp_server in host_date_time_manager.dateTimeInfo.ntpConfig.server]
                    )
                )
            hosts_info[host.name] = host_ntp_info
        return hosts_info


def main():
    argument_spec = vmware_argument_spec()
    argument_spec.update(
        cluster_name=dict(type='str', required=False),
        esxi_hostname=dict(type='str', required=False),
    )

    module = QuantumModule(
        argument_spec=argument_spec,
        required_one_of=[
            ['cluster_name', 'esxi_hostname'],
        ],
        supports_check_mode=True,
    )

    vmware_host_ntp_config = VmwareNtpInfoManager(module)
    module.exit_json(changed=False, hosts_ntp_info=vmware_host_ntp_config.gather_ntp_info())


if __name__ == "__main__":
    main()
