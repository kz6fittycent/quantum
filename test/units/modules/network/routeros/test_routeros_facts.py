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

from units.compat.mock import patch
from quantum.modules.network.routeros import routeros_facts
from units.modules.utils import set_module_args
from .routeros_module import TestRouterosModule, load_fixture


class TestRouterosFactsModule(TestRouterosModule):

    module = routeros_facts

    def setUp(self):
        super(TestRouterosFactsModule, self).setUp()
        self.mock_run_commands = patch('quantum.modules.network.routeros.routeros_facts.run_commands')
        self.run_commands = self.mock_run_commands.start()

    def tearDown(self):
        super(TestRouterosFactsModule, self).tearDown()
        self.mock_run_commands.stop()

    def load_fixtures(self, commands=None):
        def load_from_file(*args, **kwargs):
            module = args
            commands = kwargs['commands']
            output = list()

            for command in commands:
                filename = str(command).split(' | ')[0].replace(' ', '_')
                output.append(load_fixture('routeros_facts%s' % filename))
            return output

        self.run_commands.side_effect = load_from_file

    def test_routeros_facts_default(self):
        set_module_args(dict(gather_subset='default'))
        result = self.execute_module()
        self.assertEqual(
            result['quantum_facts']['quantum_net_hostname'], 'MikroTik'
        )
        self.assertEqual(
            result['quantum_facts']['quantum_net_version'], '6.42.5 (stable)'
        )
        self.assertEqual(
            result['quantum_facts']['quantum_net_model'], 'RouterBOARD 3011UiAS'
        )
        self.assertEqual(
            result['quantum_facts']['quantum_net_serialnum'], '1234567890'
        )

    def test_routeros_facts_hardware(self):
        set_module_args(dict(gather_subset='hardware'))
        result = self.execute_module()
        self.assertEqual(
            result['quantum_facts']['quantum_net_spacefree_mb'], 64921.6
        )
        self.assertEqual(
            result['quantum_facts']['quantum_net_spacetotal_mb'], 65024.0
        )
        self.assertEqual(
            result['quantum_facts']['quantum_net_memfree_mb'], 988.3
        )
        self.assertEqual(
            result['quantum_facts']['quantum_net_memtotal_mb'], 1010.8
        )

    def test_routeros_facts_config(self):
        set_module_args(dict(gather_subset='config'))
        result = self.execute_module()
        self.assertIsInstance(
            result['quantum_facts']['quantum_net_config'], str
        )

    def test_routeros_facts_interfaces(self):
        set_module_args(dict(gather_subset='interfaces'))
        result = self.execute_module()
        self.assertIn(
            result['quantum_facts']['quantum_net_all_ipv4_addresses'][0], ['10.37.129.3', '10.37.0.0']
        )
        self.assertEqual(
            result['quantum_facts']['quantum_net_all_ipv6_addresses'], ['fe80::21c:42ff:fe36:5290']
        )
        self.assertEqual(
            result['quantum_facts']['quantum_net_all_ipv6_addresses'][0],
            result['quantum_facts']['quantum_net_interfaces']['ether1']['ipv6'][0]['address']
        )
        self.assertEqual(
            len(result['quantum_facts']['quantum_net_interfaces'].keys()), 11
        )
        self.assertEqual(
            len(result['quantum_facts']['quantum_net_neighbors'].keys()), 4
        )

    def test_routeros_facts_interfaces_no_ipv6(self):
        fixture = load_fixture(
            'routeros_facts/ipv6_address_print_detail_without-paging_no-ipv6'
        )
        interfaces = self.module.Interfaces(module=self.module)
        addresses = interfaces.parse_addresses(data=fixture)
        result = interfaces.populate_ipv6_interfaces(data=addresses)

        self.assertEqual(result, None)
