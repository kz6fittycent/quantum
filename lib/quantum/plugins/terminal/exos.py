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

import re

from quantum.errors import QuantumConnectionFailure
from quantum.plugins.terminal import TerminalBase


class TerminalModule(TerminalBase):

    terminal_stdout_re = [
        re.compile(br"[\r\n](?:! )?(?:\* )?(?:\(.*\) )?(?:Slot-\d+ )?(?:VPEX )?\S+\.\d+ (?:[>#]) ?$")
    ]

    terminal_stderr_re = [
        re.compile(br"% ?Error"),
        re.compile(br"% ?Bad secret"),
        re.compile(br"[\r\n%] Bad passwords"),
        re.compile(br"invalid input", re.I),
        re.compile(br"(?:incomplete|ambiguous) command", re.I),
        re.compile(br"connection timed out", re.I),
        re.compile(br"[^\r\n]+ not found"),
        re.compile(br"'[^']' +returned error code: ?\d+"),
        re.compile(br"Bad mask", re.I),
        re.compile(br"% ?(\S+) ?overlaps with ?(\S+)", re.I),
        re.compile(br"[%\S] ?Error: ?[\s]+", re.I),
        re.compile(br"[%\S] ?Informational: ?[\s]+", re.I),
        re.compile(br"%% Invalid .* at '\^' marker.", re.I),
    ]

    def on_open_shell(self):
        try:
            for cmd in (b'disable clipaging', b'configure cli columns 256'):
                self._exec_cli_command(cmd)
        except QuantumConnectionFailure:
            raise QuantumConnectionFailure('unable to set terminal parameters')
