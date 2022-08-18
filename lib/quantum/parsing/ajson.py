# Copyright: (c) 2018, Quantum Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json

# Imported for backwards compat
from quantum.module_utils.common.json import QuantumJSONEncoder

from quantum.parsing.vault import VaultLib
from quantum.parsing.yaml.objects import QuantumVaultEncryptedUnicode
from quantum.utils.unsafe_proxy import wrap_var


class QuantumJSONDecoder(json.JSONDecoder):

    _vaults = {}

    def __init__(self, *args, **kwargs):
        kwargs['object_hook'] = self.object_hook
        super(QuantumJSONDecoder, self).__init__(*args, **kwargs)

    @classmethod
    def set_secrets(cls, secrets):
        cls._vaults['default'] = VaultLib(secrets=secrets)

    def object_hook(self, pairs):
        for key in pairs:
            value = pairs[key]

            if key == '__quantum_vault':
                value = QuantumVaultEncryptedUnicode(value)
                if self._vaults:
                    value.vault = self._vaults['default']
                return value
            elif key == '__quantum_unsafe':
                return wrap_var(value)

        return pairs
