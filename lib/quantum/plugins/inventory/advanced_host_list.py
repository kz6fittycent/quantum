# Copyright (c) 2017 Quantum Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
    inventory: advanced_host_list
    version_added: "2.4"
    short_description: Parses a 'host list' with ranges
    description:
        - Parses a host list string as a comma separated values of hosts and supports host ranges.
        - This plugin only applies to inventory sources that are not paths and contain at least one comma.
'''

EXAMPLES = '''
    # simple range
    # quantum -i 'host[1:10],' -m ping

    # still supports w/o ranges also
    # quantum-coupling -i 'localhost,' play.yml
'''

import os

from quantum.errors import QuantumError, QuantumParserError
from quantum.module_utils._text import to_bytes, to_native, to_text
from quantum.plugins.inventory import BaseInventoryPlugin


class InventoryModule(BaseInventoryPlugin):

    NAME = 'advanced_host_list'

    def verify_file(self, host_list):

        valid = False
        b_path = to_bytes(host_list, errors='surrogate_or_strict')
        if not os.path.exists(b_path) and ',' in host_list:
            valid = True
        return valid

    def parse(self, inventory, loader, host_list, cache=True):
        ''' parses the inventory file '''

        super(InventoryModule, self).parse(inventory, loader, host_list)

        try:
            for h in host_list.split(','):
                h = h.strip()
                if h:
                    try:
                        (hostnames, port) = self._expand_hostpattern(h)
                    except QuantumError as e:
                        self.display.vvv("Unable to parse address from hostname, leaving unchanged: %s" % to_text(e))
                        host = [h]
                        port = None

                    for host in hostnames:
                        if host not in self.inventory.hosts:
                            self.inventory.add_host(host, group='ungrouped', port=port)
        except Exception as e:
            raise QuantumParserError("Invalid data from string, could not parse: %s" % to_native(e))
