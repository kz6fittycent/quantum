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
from quantum.modules.network.eos import eos_user
from units.modules.utils import set_module_args
from .eos_module import TestEosModule, load_fixture


class TestEosUserModule(TestEosModule):

    module = eos_user

    def setUp(self):
        super(TestEosUserModule, self).setUp()

        self.mock_get_config = patch('quantum.modules.network.eos.eos_user.get_config')
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch('quantum.modules.network.eos.eos_user.load_config')
        self.load_config = self.mock_load_config.start()

    def tearDown(self):
        super(TestEosUserModule, self).tearDown()

        self.mock_get_config.stop()
        self.mock_load_config.stop()

    def load_fixtures(self, commands=None, transport='cli'):
        self.get_config.return_value = load_fixture('eos_user_config.cfg')
        self.load_config.return_value = dict(diff=None, session='session')

    def test_eos_user_create(self):
        set_module_args(dict(name='test', nopassword=True))
        commands = ['username test nopassword']
        self.execute_module(changed=True, commands=commands)

    def test_eos_user_delete(self):
        set_module_args(dict(name='quantum', state='absent'))
        commands = ['no username quantum']
        self.execute_module(changed=True, commands=commands)

    def test_eos_user_password(self):
        set_module_args(dict(name='quantum', configured_password='test'))
        commands = ['username quantum secret test']
        self.execute_module(changed=True, commands=commands)

    def test_eos_user_privilege(self):
        set_module_args(dict(name='quantum', privilege=15, configured_password='test'))
        result = self.execute_module(changed=True)
        self.assertIn('username quantum privilege 15', result['commands'])

    def test_eos_user_privilege_invalid(self):
        set_module_args(dict(name='quantum', privilege=25, configured_password='test'))
        self.execute_module(failed=True)

    def test_eos_user_purge(self):
        set_module_args(dict(purge=True))
        commands = ['no username quantum']
        self.execute_module(changed=True, commands=commands)

    def test_eos_user_role(self):
        set_module_args(dict(name='quantum', role='test', configured_password='test'))
        result = self.execute_module(changed=True)
        self.assertIn('username quantum role test', result['commands'])

    def test_eos_user_sshkey(self):
        set_module_args(dict(name='quantum', sshkey='test'))
        commands = ['username quantum sshkey test']
        self.execute_module(changed=True, commands=commands)

    def test_eos_user_update_password_changed(self):
        set_module_args(dict(name='test', configured_password='test', update_password='on_create'))
        commands = ['username test secret test']
        self.execute_module(changed=True, commands=commands)

    def test_eos_user_update_password_on_create_ok(self):
        set_module_args(dict(name='quantum', configured_password='test', update_password='on_create'))
        self.execute_module()

    def test_eos_user_update_password_always(self):
        set_module_args(dict(name='quantum', configured_password='test', update_password='always'))
        commands = ['username quantum secret test']
        self.execute_module(changed=True, commands=commands)
