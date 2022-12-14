#
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
#
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import re
import time

from quantum.errors import QuantumConnectionFailure
from quantum.plugins.terminal import TerminalBase


class TerminalModule(TerminalBase):

    terminal_stdout_re = [
        re.compile(br"[\r\n]?[\w]*\(.+\)?[>#\$](?:\s*)$"),
        re.compile(br"User:")
    ]

    terminal_stderr_re = [
        re.compile(br"% ?Error"),
        re.compile(br"% ?Bad secret"),
        re.compile(br"invalid input", re.I),
        re.compile(br"incorrect usage", re.I),
        re.compile(br"(?:incomplete|ambiguous) command", re.I),
        re.compile(br"connection timed out", re.I),
        re.compile(br"[^\r\n]+ not found", re.I),
        re.compile(br"'[^']' +returned error code: ?\d+"),
    ]

    def on_open_shell(self):
        try:
            commands = ('{"command": "' + self._connection._play_context.remote_user + '", "prompt": "Password:", "answer": "' +
                        self._connection._play_context.password + '"}',
                        '{"command": "config paging disable"}')
            for cmd in commands:
                self._exec_cli_command(cmd)
        except QuantumConnectionFailure:
            try:
                self._exec_cli_command(b'config paging disable')
            except QuantumConnectionFailure:
                raise QuantumConnectionFailure('unable to set terminal parameters')
