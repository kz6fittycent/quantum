# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Quantum Project # GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    become: dzdo
    short_description: Centrify's Direct Authorize
    description:
        - This become plugins allows your remote/login user to execute commands as another user via the dzdo utility.
    author: quantum (@core)
    version_added: "2.8"
    options:
        become_user:
            description: User you 'become' to execute the task
            ini:
              - section: privilege_escalation
                key: become_user
              - section: dzdo_become_plugin
                key: user
            vars:
              - name: quantum_become_user
              - name: quantum_dzdo_user
            env:
              - name: ANSIBLE_BECOME_USER
              - name: ANSIBLE_DZDO_USER
        become_exe:
            description: Dzdo executable
            default: dzdo
            ini:
              - section: privilege_escalation
                key: become_exe
              - section: dzdo_become_plugin
                key: executable
            vars:
              - name: quantum_become_exe
              - name: quantum_dzdo_exe
            env:
              - name: ANSIBLE_BECOME_EXE
              - name: ANSIBLE_DZDO_EXE
        become_flags:
            description: Options to pass to dzdo
            default: -H -S -n
            ini:
              - section: privilege_escalation
                key: become_flags
              - section: dzdo_become_plugin
                key: flags
            vars:
              - name: quantum_become_flags
              - name: quantum_dzdo_flags
            env:
              - name: ANSIBLE_BECOME_FLAGS
              - name: ANSIBLE_DZDO_FLAGS
        become_pass:
            description: Options to pass to dzdo
            required: False
            vars:
              - name: quantum_become_password
              - name: quantum_become_pass
              - name: quantum_dzdo_pass
            env:
              - name: ANSIBLE_BECOME_PASS
              - name: ANSIBLE_DZDO_PASS
            ini:
              - section: dzdo_become_plugin
                key: password
"""

from quantum.plugins.become import BecomeBase


class BecomeModule(BecomeBase):

    name = 'dzdo'

    # messages for detecting prompted password issues
    fail = ('Sorry, try again.',)

    def build_become_command(self, cmd, shell):
        super(BecomeModule, self).build_become_command(cmd, shell)

        if not cmd:
            return cmd

        becomecmd = self.get_option('become_exe') or self.name

        flags = self.get_option('become_flags') or ''
        if self.get_option('become_pass'):
            self.prompt = '[dzdo via quantum, key=%s] password:' % self._id
            flags = '%s -p "%s"' % (flags.replace('-n', ''), self.prompt)

        user = self.get_option('become_user') or ''
        if user:
            user = '-u %s' % (user)

        return ' '.join([becomecmd, flags, user, self._build_success_command(cmd, shell)])
