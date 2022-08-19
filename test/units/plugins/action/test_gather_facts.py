# (c) 2016, Saran Ahluwalia <ahlusar.ahluwalia@gmail.com>
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

from units.compat import unittest
from units.compat.mock import MagicMock

from quantum import constants as C
from quantum.plugins.action.gather_facts import ActionModule
from quantum.coupling.task import Task
from quantum.template import Templar

from units.mock.loader import DictDataLoader


class TestNetworkFacts(unittest.TestCase):
    task = MagicMock(Task)
    play_context = MagicMock()
    play_context.check_mode = False
    connection = MagicMock()
    fake_loader = DictDataLoader({
    })
    templar = Templar(loader=fake_loader)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_network_gather_facts(self):
        self.task_vars = {'quantum_network_os': 'ios'}
        self.task.action = 'gather_facts'
        self.task.async_val = False
        self.task.args = {'gather_subset': 'min'}
        self.task.module_defaults = [{'ios_facts': {'gather_subset': 'min'}}]

        plugin = ActionModule(self.task, self.connection, self.play_context, loader=None, templar=self.templar, shared_loader_obj=None)
        plugin._execute_module = MagicMock()

        res = plugin.run(task_vars=self.task_vars)
        self.assertEqual(res['quantum_facts']['_quantum_facts_gathered'], True)

        mod_args = plugin._get_module_args('ios_facts', task_vars=self.task_vars)
        self.assertEqual(mod_args['gather_subset'], 'min')

        facts_modules = C.config.get_config_value('FACTS_MODULES', variables=self.task_vars)
        self.assertEqual(facts_modules, ['ios_facts'])

    def test_network_gather_facts_fqcn(self):
        self.fqcn_task_vars = {'quantum_network_os': 'cisco.ios.ios'}
        self.task.action = 'gather_facts'
        self.task.async_val = False
        self.task.args = {'gather_subset': 'min'}
        self.task.module_defaults = [{'cisco.ios.ios_facts': {'gather_subset': 'min'}}]

        plugin = ActionModule(self.task, self.connection, self.play_context, loader=None, templar=self.templar, shared_loader_obj=None)
        plugin._execute_module = MagicMock()

        res = plugin.run(task_vars=self.fqcn_task_vars)
        self.assertEqual(res['quantum_facts']['_quantum_facts_gathered'], True)

        mod_args = plugin._get_module_args('cisco.ios.ios_facts', task_vars=self.fqcn_task_vars)
        self.assertEqual(mod_args['gather_subset'], 'min')

        facts_modules = C.config.get_config_value('FACTS_MODULES', variables=self.fqcn_task_vars)
        self.assertEqual(facts_modules, ['cisco.ios.ios_facts'])
