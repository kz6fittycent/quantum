# (c) 2016 Red Hat Inc.
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

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json

from units.compat.mock import patch
from units.modules.utils import set_module_args
from .iosxr_module import TestIosxrModule, load_fixture
from quantum.modules.network.iosxr import iosxr_facts


class TestIosxrFacts(TestIosxrModule):

    module = iosxr_facts

    def setUp(self):
        super(TestIosxrFacts, self).setUp()

        self.mock_run_commands = patch(
            'quantum.module_utils.network.iosxr.facts.legacy.base.run_commands')
        self.run_commands = self.mock_run_commands.start()

        self.mock_get_resource_connection = patch('quantum.module_utils.network.common.facts.facts.get_resource_connection')
        self.get_resource_connection = self.mock_get_resource_connection.start()

        self.mock_get_capabilities = patch('quantum.module_utils.network.iosxr.facts.legacy.base.get_capabilities')
        self.get_capabilities = self.mock_get_capabilities.start()
        self.get_capabilities.return_value = {
            'device_info': {
                'network_os': 'iosxr',
                'network_os_hostname': 'iosxr01',
                'network_os_image': 'bootflash:disk0/xrvr-os-mbi-6.1.3/mbixrvr-rp.vm',
                'network_os_version': '6.1.3[Default]'
            },
            'network_api': 'cliconf'
        }

    def tearDown(self):
        super(TestIosxrFacts, self).tearDown()

        self.mock_run_commands.stop()
        self.mock_get_capabilities.stop()
        self.mock_get_resource_connection.stop()

    def load_fixtures(self, commands=None):

        def load_from_file(*args, **kwargs):
            module, commands = args
            output = list()

            for item in commands:
                try:
                    obj = json.loads(item)
                    command = obj['command']
                except ValueError:
                    command = item
                filename = str(command).replace(' ', '_')
                filename = filename.replace('/', '7')
                filename = filename.replace('|', '_')
                output.append(load_fixture(filename))
            return output

        self.run_commands.side_effect = load_from_file

    def test_iosxr_facts_gather_subset_default(self):
        set_module_args(dict())
        result = self.execute_module()
        quantum_facts = result['quantum_facts']
        self.assertIn('hardware', quantum_facts['quantum_net_gather_subset'])
        self.assertIn('default', quantum_facts['quantum_net_gather_subset'])
        self.assertIn('interfaces', quantum_facts['quantum_net_gather_subset'])
        self.assertEquals('iosxr01', quantum_facts['quantum_net_hostname'])
        self.assertEquals(['disk0:', 'flash0:'], quantum_facts['quantum_net_filesystems'])
        self.assertIn('GigabitEthernet0/0/0/0', quantum_facts['quantum_net_interfaces'].keys())
        self.assertEquals('3095', quantum_facts['quantum_net_memtotal_mb'])
        self.assertEquals('1499', quantum_facts['quantum_net_memfree_mb'])

    def test_iosxr_facts_gather_subset_config(self):
        set_module_args({'gather_subset': 'config'})
        result = self.execute_module()
        quantum_facts = result['quantum_facts']
        self.assertIn('default', quantum_facts['quantum_net_gather_subset'])
        self.assertIn('config', quantum_facts['quantum_net_gather_subset'])
        self.assertEquals('iosxr01', quantum_facts['quantum_net_hostname'])
        self.assertIn('quantum_net_config', quantum_facts)
