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

from units.compat.mock import patch
from quantum.modules.network.ios import ios_user
from units.modules.utils import set_module_args
from .ios_module import TestIosModule, load_fixture


class TestIosUserModule(TestIosModule):

    module = ios_user

    def setUp(self):
        super(TestIosUserModule, self).setUp()

        self.mock_get_config = patch('quantum.modules.network.ios.ios_user.get_config')
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch('quantum.modules.network.ios.ios_user.load_config')
        self.load_config = self.mock_load_config.start()

    def tearDown(self):
        super(TestIosUserModule, self).tearDown()
        self.mock_get_config.stop()
        self.mock_load_config.stop()

    def load_fixtures(self, commands=None, transport='cli'):
        self.get_config.return_value = load_fixture('ios_user_config.cfg')
        self.load_config.return_value = dict(diff=None, session='session')

    def test_ios_user_create(self):
        set_module_args(dict(name='test', nopassword=True))
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], ['username test nopassword'])

    def test_ios_user_delete(self):
        set_module_args(dict(name='quantum', state='absent'))
        result = self.execute_module(changed=True)
        cmds = [
            {
                "command": "no username quantum", "answer": "y", "newline": False,
                "prompt": "This operation will remove all username related configurations with same name",
            }
        ]

        result_cmd = []
        for i in result['commands']:
            result_cmd.append(i)

        self.assertEqual(result_cmd, cmds)

    def test_ios_user_password(self):
        set_module_args(dict(name='quantum', configured_password='test'))
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], ['username quantum secret test'])

    def test_ios_user_privilege(self):
        set_module_args(dict(name='quantum', privilege=15))
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], ['username quantum privilege 15'])

    def test_ios_user_privilege_invalid(self):
        set_module_args(dict(name='quantum', privilege=25))
        self.execute_module(failed=True)

    def test_ios_user_purge(self):
        set_module_args(dict(purge=True))
        result = self.execute_module(changed=True)
        cmd = {
            "command": "no username quantum", "answer": "y", "newline": False,
            "prompt": "This operation will remove all username related configurations with same name",
        }

        result_cmd = []
        for i in result['commands']:
            result_cmd.append(i)

        self.assertEqual(result_cmd, [cmd])

    def test_ios_user_view(self):
        set_module_args(dict(name='quantum', view='test'))
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], ['username quantum view test'])

    def test_ios_user_update_password_changed(self):
        set_module_args(dict(name='test', configured_password='test', update_password='on_create'))
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], ['username test secret test'])

    def test_ios_user_update_password_on_create_ok(self):
        set_module_args(dict(name='quantum', configured_password='test', update_password='on_create'))
        self.execute_module()

    def test_ios_user_update_password_always(self):
        set_module_args(dict(name='quantum', configured_password='test', update_password='always'))
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], ['username quantum secret test'])

    def test_ios_user_set_sshkey(self):
        set_module_args(dict(name='quantum', sshkey='dGVzdA=='))
        commands = [
            'ip ssh pubkey-chain',
            'username quantum',
            'key-hash ssh-rsa 098F6BCD4621D373CADE4E832627B4F6',
            'exit',
            'exit'
        ]
        result = self.execute_module(changed=True, commands=commands)
        self.assertEqual(result['commands'], commands)

    def test_ios_user_set_sshkey_multiple(self):
        set_module_args(dict(name='quantum', sshkey=['dGVzdA==', 'eHWacB2==']))
        commands = [
            'ip ssh pubkey-chain',
            'username quantum',
            'key-hash ssh-rsa 098F6BCD4621D373CADE4E832627B4F6',
            'key-hash ssh-rsa A019918340A1E9183388D9A675603036',
            'exit',
            'exit'
        ]
        result = self.execute_module(changed=True, commands=commands)
        self.assertEqual(result['commands'], commands)
