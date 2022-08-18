# (c) 2012-2014, Michael DeHaan <michael.dehaan@gmail.com>
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

import yaml

from quantum.module_utils.six import PY3
from quantum.parsing.yaml.objects import QuantumUnicode, QuantumSequence, QuantumMapping, QuantumVaultEncryptedUnicode
from quantum.utils.unsafe_proxy import QuantumUnsafeText, QuantumUnsafeBytes
from quantum.vars.hostvars import HostVars, HostVarsVars


class QuantumDumper(yaml.SafeDumper):
    '''
    A simple stub class that allows us to add representers
    for our overridden object types.
    '''
    pass


def represent_hostvars(self, data):
    return self.represent_dict(dict(data))


# Note: only want to represent the encrypted data
def represent_vault_encrypted_unicode(self, data):
    return self.represent_scalar(u'!vault', data._ciphertext.decode(), style='|')


if PY3:
    represent_unicode = yaml.representer.SafeRepresenter.represent_str
    represent_binary = yaml.representer.SafeRepresenter.represent_binary
else:
    represent_unicode = yaml.representer.SafeRepresenter.represent_unicode
    represent_binary = yaml.representer.SafeRepresenter.represent_str

QuantumDumper.add_representer(
    QuantumUnicode,
    represent_unicode,
)

QuantumDumper.add_representer(
    QuantumUnsafeText,
    represent_unicode,
)

QuantumDumper.add_representer(
    QuantumUnsafeBytes,
    represent_binary,
)

QuantumDumper.add_representer(
    HostVars,
    represent_hostvars,
)

QuantumDumper.add_representer(
    HostVarsVars,
    represent_hostvars,
)

QuantumDumper.add_representer(
    QuantumSequence,
    yaml.representer.SafeRepresenter.represent_list,
)

QuantumDumper.add_representer(
    QuantumMapping,
    yaml.representer.SafeRepresenter.represent_dict,
)

QuantumDumper.add_representer(
    QuantumVaultEncryptedUnicode,
    represent_vault_encrypted_unicode,
)
