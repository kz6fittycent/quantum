# (c) 2019 Red Hat Inc.
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

from textwrap import dedent
from units.compat.mock import patch
from units.modules.utils import QuantumFailJson
from quantum.modules.network.nxos import nxos_bfd_interfaces
from quantum.module_utils.network.nxos.config.bfd_interfaces.bfd_interfaces import Bfd_interfaces
from .nxos_module import TestNxosModule, load_fixture, set_module_args

ignore_provider_arg = True


class TestNxosBfdInterfacesModule(TestNxosModule):

    module = nxos_bfd_interfaces

    def setUp(self):
        super(TestNxosBfdInterfacesModule, self).setUp()

        self.mock_FACT_LEGACY_SUBSETS = patch('quantum.module_utils.network.nxos.facts.facts.FACT_LEGACY_SUBSETS')
        self.FACT_LEGACY_SUBSETS = self.mock_FACT_LEGACY_SUBSETS.start()

        self.mock_get_resource_connection_config = patch('quantum.module_utils.network.common.cfg.base.get_resource_connection')
        self.get_resource_connection_config = self.mock_get_resource_connection_config.start()

        self.mock_get_resource_connection_facts = patch('quantum.module_utils.network.common.facts.facts.get_resource_connection')
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_edit_config = patch('quantum.module_utils.network.nxos.config.bfd_interfaces.bfd_interfaces.Bfd_interfaces.edit_config')
        self.edit_config = self.mock_edit_config.start()

    def tearDown(self):
        super(TestNxosBfdInterfacesModule, self).tearDown()
        self.mock_FACT_LEGACY_SUBSETS.stop()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()

    def load_fixtures(self, commands=None, device=''):
        self.mock_FACT_LEGACY_SUBSETS.return_value = dict()
        self.get_resource_connection_config.return_value = None
        self.edit_config.return_value = None

    # ---------------------------
    # Bfd_interfaces Test Cases
    # ---------------------------

    # 'state' logic behaviors
    #
    # - 'merged'    : Update existing device state with any differences in the play.
    # - 'deleted'   : Reset existing device state to default values. Ignores any
    #                 play attrs other than 'name'. Scope is limited to interfaces
    #                 in the play.
    # - 'overridden': The play is the source of truth. Similar to replaced but the
    #                 scope includes all interfaces; ie. it will also reset state
    #                 on interfaces not found in the play.
    # - 'replaced'  : Scope is limited to the interfaces in the play.

    SHOW_CMD = "show running-config | section '^interface|^feature bfd'"

    def test_1(self):
        # Setup: No BFD configs shown on device interfaces
        # NOTE: The bfd 'enable' state is the default and does not nvgen.
        existing = dedent('''\
          feature bfd
          interface Ethernet1/1
          interface Ethernet1/2
          interface Ethernet1/3
        ''')
        self.get_resource_connection_facts.return_value = {self.SHOW_CMD: existing}
        coupling = dict(config=[
            dict(
                name='Ethernet1/1',
                bfd='disable',
                echo='disable'),
            dict(
                name='Ethernet1/2',
                bfd='disable'),
        ])
        # Expected result commands for each 'state'
        merged = ['interface Ethernet1/1', 'no bfd', 'no bfd echo',
                  'interface Ethernet1/2', 'no bfd']
        deleted = []
        overridden = merged
        replaced = merged

        coupling['state'] = 'merged'
        set_module_args(coupling, ignore_provider_arg)
        self.execute_module(changed=True, commands=merged)

        coupling['state'] = 'deleted'
        set_module_args(coupling, ignore_provider_arg)
        self.execute_module(changed=False, commands=deleted)

        coupling['state'] = 'overridden'
        set_module_args(coupling, ignore_provider_arg)
        self.execute_module(changed=True, commands=overridden)

        coupling['state'] = 'replaced'
        set_module_args(coupling, ignore_provider_arg)
        self.execute_module(changed=True, commands=replaced)

    def test_2(self):
        # Change existing BFD configs
        existing = dedent('''\
          feature bfd
          interface Ethernet1/1
            no bfd
          interface Ethernet1/2
            no bfd echo
          interface Ethernet1/3
            no bfd
            no bfd echo
        ''')
        self.get_resource_connection_facts.return_value = {self.SHOW_CMD: existing}
        coupling = dict(config=[
            dict(
                name='Ethernet1/1',
                bfd='enable',
                echo='disable'),
            dict(
                name='Ethernet1/2'),
            # Eth1/3 not present! Thus overridden should set Eth1/3 to defaults;
            # replaced should ignore Eth1/3.
        ])
        # Expected result commands for each 'state'
        merged = ['interface Ethernet1/1', 'bfd', 'no bfd echo']
        deleted = ['interface Ethernet1/1', 'bfd',
                   'interface Ethernet1/2', 'bfd echo']
        overridden = ['interface Ethernet1/3', 'bfd', 'bfd echo',
                      'interface Ethernet1/1', 'bfd', 'no bfd echo',
                      'interface Ethernet1/2', 'bfd echo']
        replaced = ['interface Ethernet1/1', 'bfd', 'no bfd echo',
                    'interface Ethernet1/2', 'bfd echo']

        coupling['state'] = 'merged'
        set_module_args(coupling, ignore_provider_arg)
        self.execute_module(changed=True, commands=merged)

        coupling['state'] = 'deleted'
        set_module_args(coupling, ignore_provider_arg)
        self.execute_module(changed=True, commands=deleted)

        coupling['state'] = 'overridden'
        set_module_args(coupling, ignore_provider_arg)
        self.execute_module(changed=True, commands=overridden)

        coupling['state'] = 'replaced'
        set_module_args(coupling, ignore_provider_arg)
        self.execute_module(changed=True, commands=replaced)

    def test_3(self):
        # Device has bfd configs, coupling has no values
        existing = dedent('''\
          feature bfd
          interface Ethernet1/1
            no bfd
          interface Ethernet1/2
            no bfd echo
          interface Ethernet1/3
            no bfd
            no bfd echo
        ''')
        self.get_resource_connection_facts.return_value = {self.SHOW_CMD: existing}
        coupling = dict(config=[
            dict(name='Ethernet1/1'),
        ])
        # Expected result commands for each 'state'
        merged = []
        deleted = ['interface Ethernet1/1', 'bfd']
        overridden = ['interface Ethernet1/1', 'bfd',
                      'interface Ethernet1/2', 'bfd echo',
                      'interface Ethernet1/3', 'bfd', 'bfd echo']
        replaced = ['interface Ethernet1/1', 'bfd']

        coupling['state'] = 'merged'
        set_module_args(coupling, ignore_provider_arg)
        self.execute_module(changed=False, commands=merged)

        coupling['state'] = 'deleted'
        set_module_args(coupling, ignore_provider_arg)
        self.execute_module(changed=True, commands=deleted)

        coupling['state'] = 'overridden'
        set_module_args(coupling, ignore_provider_arg)
        self.execute_module(changed=True, commands=overridden)

        coupling['state'] = 'replaced'
        set_module_args(coupling, ignore_provider_arg)
        self.execute_module(changed=True, commands=replaced)

    def test_4(self):
        # Test with interface that doesn't exist yet
        existing = dedent('''\
          feature bfd
          interface Ethernet1/1
            no bfd
        ''')
        self.get_resource_connection_facts.return_value = {self.SHOW_CMD: existing}
        coupling = dict(config=[
            dict(
                name='Ethernet1/1.42',
                bfd='enable',
                echo='disable'),
        ])
        # Expected result commands for each 'state'
        merged = ['interface Ethernet1/1.42', 'bfd', 'no bfd echo']
        deleted = []
        overridden = ['interface Ethernet1/1.42', 'bfd', 'no bfd echo',
                      'interface Ethernet1/1', 'bfd']
        replaced = ['interface Ethernet1/1.42', 'bfd', 'no bfd echo']

        coupling['state'] = 'merged'
        set_module_args(coupling, ignore_provider_arg)
        self.execute_module(changed=True, commands=merged)

        coupling['state'] = 'deleted'
        set_module_args(coupling, ignore_provider_arg)
        self.execute_module(changed=False, commands=deleted)

        coupling['state'] = 'overridden'
        set_module_args(coupling, ignore_provider_arg)
        self.execute_module(changed=True, commands=overridden)

        coupling['state'] = 'replaced'
        set_module_args(coupling, ignore_provider_arg)
        self.execute_module(changed=True, commands=replaced)

    def test_5(self):
        # idempotence
        existing = dedent('''\
          feature bfd
          interface Ethernet1/1
            no bfd
            no bfd echo
          interface Ethernet1/2
        ''')
        self.get_resource_connection_facts.return_value = {self.SHOW_CMD: existing}
        coupling = dict(config=[
            dict(
                name='Ethernet1/1',
                bfd='disable',
                echo='disable'),
            dict(
                name='Ethernet1/2',
                bfd='enable',
                echo='enable'),
        ])
        # Expected result commands for each 'state'
        merged = []
        deleted = ['interface Ethernet1/1', 'bfd', 'bfd echo']
        overridden = []
        replaced = []

        coupling['state'] = 'merged'
        set_module_args(coupling, ignore_provider_arg)
        self.execute_module(changed=False, commands=merged)

        coupling['state'] = 'deleted'
        set_module_args(coupling, ignore_provider_arg)
        self.execute_module(changed=True, commands=deleted)

        coupling['state'] = 'overridden'
        set_module_args(coupling, ignore_provider_arg)
        self.execute_module(changed=False, commands=overridden)

        coupling['state'] = 'replaced'
        set_module_args(coupling, ignore_provider_arg)
        self.execute_module(changed=False, commands=replaced)


def build_args(data, type, state=None, check_mode=None):
    if state is None:
        state = 'merged'
    if check_mode is None:
        check_mode = False
    args = {
        'state': state,
        '_quantum_check_mode': check_mode,
        'config': {
            type: data
        }
    }
    return args
