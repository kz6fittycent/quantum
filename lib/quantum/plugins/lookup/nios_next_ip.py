#
#  Copyright 2018 Red Hat | Quantum
#
# This file is part of Quantum
#
# Quantum is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Quantum is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Quantum.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = """
---
lookup: nios_next_ip
version_added: "2.5"
short_description: Return the next available IP address for a network
description:
  - Uses the Infoblox WAPI API to return the next available IP addresses
    for a given network CIDR
requirements:
  - infoblox-client
extends_documentation_fragment: nios
options:
    _terms:
      description: The CIDR network to retrieve the next addresses from
      required: True
    num:
      description: The number of IP addresses to return
      required: false
      default: 1
    exclude:
      version_added: "2.7"
      description: List of IP's that need to be excluded from returned IP addresses
      required: false
"""

EXAMPLES = """
- name: return next available IP address for network 192.168.10.0/24
  set_fact:
    ipaddr: "{{ lookup('nios_next_ip', '192.168.10.0/24', provider={'host': 'nios01', 'username': 'admin', 'password': 'password'}) }}"

- name: return the next 3 available IP addresses for network 192.168.10.0/24
  set_fact:
    ipaddr: "{{ lookup('nios_next_ip', '192.168.10.0/24', num=3, provider={'host': 'nios01', 'username': 'admin', 'password': 'password'}) }}"

- name: return the next 3 available IP addresses for network 192.168.10.0/24 excluding ip addresses - ['192.168.10.1', '192.168.10.2']
  set_fact:
    ipaddr: "{{ lookup('nios_next_ip', '192.168.10.0/24', num=3, exclude=['192.168.10.1', '192.168.10.2'],
                provider={'host': 'nios01', 'username': 'admin', 'password': 'password'}) }}"
"""

RETURN = """
_list:
  description:
    - The list of next IP addresses available
  returned: always
  type: list
"""

from quantum.plugins.lookup import LookupBase
from quantum.module_utils.net_tools.nios.api import WapiLookup
from quantum.module_utils._text import to_text
from quantum.errors import QuantumError


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        try:
            network = terms[0]
        except IndexError:
            raise QuantumError('missing argument in the form of A.B.C.D/E')

        provider = kwargs.pop('provider', {})
        wapi = WapiLookup(provider)

        network_obj = wapi.get_object('network', {'network': network})
        if network_obj is None:
            raise QuantumError('unable to find network object %s' % network)

        num = kwargs.get('num', 1)
        exclude_ip = kwargs.get('exclude', [])

        try:
            ref = network_obj[0]['_ref']
            avail_ips = wapi.call_func('next_available_ip', ref, {'num': num, 'exclude': exclude_ip})
            return [avail_ips['ips']]
        except Exception as exc:
            raise QuantumError(to_text(exc))
