# (c) 2016 Red Hat Inc.
#
# (c) 2017 Dell EMC.
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
from quantum.modules.network.dellos9 import dellos9_command
from units.modules.utils import set_module_args
from .dellos9_module import TestDellos9Module, load_fixture


class TestDellos9CommandModule(TestDellos9Module):

    module = dellos9_command

    def setUp(self):
        super(TestDellos9CommandModule, self).setUp()

        self.mock_run_commands = patch('quantum.modules.network.dellos9.dellos9_command.run_commands')
        self.run_commands = self.mock_run_commands.start()

    def tearDown(self):
        super(TestDellos9CommandModule, self).tearDown()
        self.mock_run_commands.stop()

    def load_fixtures(self, commands=None):

        def load_from_file(*args, **kwargs):
            module, commands = args
            output = list()

            for item in commands:
                try:
                    obj = json.loads(item['command'])
                    command = obj['command']
                except ValueError:
                    command = item['command']
                filename = str(command).replace(' ', '_')
                output.append(load_fixture(filename))
            return output

        self.run_commands.side_effect = load_from_file

    def test_dellos9_command_simple(self):
        set_module_args(dict(commands=['show version']))
        result = self.execute_module()
        self.assertEqual(len(result['stdout']), 1)
        self.assertTrue(result['stdout'][0].startswith('Dell Real Time'))

    def test_dellos9_command_multiple(self):
        set_module_args(dict(commands=['show version', 'show version']))
        result = self.execute_module()
        self.assertEqual(len(result['stdout']), 2)
        self.assertTrue(result['stdout'][0].startswith('Dell Real Time'))

    def test_dellos9_command_wait_for(self):
        wait_for = 'result[0] contains "Dell Real"'
        set_module_args(dict(commands=['show version'], wait_for=wait_for))
        self.execute_module()

    def test_dellos9_command_wait_for_fails(self):
        wait_for = 'result[0] contains "test string"'
        set_module_args(dict(commands=['show version'], wait_for=wait_for))
        self.execute_module(failed=True)
        self.assertEqual(self.run_commands.call_count, 10)

    def test_dellos9_command_retries(self):
        wait_for = 'result[0] contains "test string"'
        set_module_args(dict(commands=['show version'], wait_for=wait_for, retries=2))
        self.execute_module(failed=True)
        self.assertEqual(self.run_commands.call_count, 2)

    def test_dellos9_command_match_any(self):
        wait_for = ['result[0] contains "Dell Real"',
                    'result[0] contains "test string"']
        set_module_args(dict(commands=['show version'], wait_for=wait_for, match='any'))
        self.execute_module()

    def test_dellos9_command_match_all(self):
        wait_for = ['result[0] contains "Dell Real"',
                    'result[0] contains "Operating System"']
        set_module_args(dict(commands=['show version'], wait_for=wait_for, match='all'))
        self.execute_module()

    def test_dellos9_command_match_all_failure(self):
        wait_for = ['result[0] contains "Dell Real"',
                    'result[0] contains "test string"']
        commands = ['show version', 'show version']
        set_module_args(dict(commands=commands, wait_for=wait_for, match='all'))
        self.execute_module(failed=True)
