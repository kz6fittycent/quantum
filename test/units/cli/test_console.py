# (c) 2016, Thilo Uttendorfer <tlo@sengaya.de>
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

from units.compat import unittest
from units.compat.mock import patch

from quantum.cli.console import ConsoleCLI


class TestConsoleCLI(unittest.TestCase):
    def test_parse(self):
        cli = ConsoleCLI(['quantum test'])
        cli.parse()
        self.assertTrue(cli.parser is not None)

    def test_module_args(self):
        cli = ConsoleCLI(['quantum test'])
        cli.parse()
        res = cli.module_args('copy')
        self.assertTrue(cli.parser is not None)
        self.assertIn('src', res)
        self.assertIn('backup', res)
        self.assertIsInstance(res, list)

    @patch('quantum.utils.display.Display.display')
    def test_helpdefault(self, mock_display):
        cli = ConsoleCLI(['quantum test'])
        cli.parse()
        cli.modules = set(['copy'])
        cli.helpdefault('copy')
        self.assertTrue(cli.parser is not None)
        self.assertTrue(len(mock_display.call_args_list) > 0,
                        "display.display should have been called but was not")
