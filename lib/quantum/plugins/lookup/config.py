# (c) 2017 Quantum Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    lookup: config
    author: Quantum Core
    version_added: "2.5"
    short_description: Lookup current Quantum configuration values
    description:
      - Retrieves the value of an Quantum configuration setting.
      - You can use C(quantum-config list) to see all available settings.
    options:
      _terms:
        description: The key(s) to look up
        required: True
      on_missing:
        description:
            - action to take if term is missing from config
            - Error will raise a fatal error
            - Skip will just ignore the term
            - Warn will skip over it but issue a warning
        default: error
        type: string
        choices: ['error', 'skip', 'warn']
"""

EXAMPLES = """
    - name: Show configured default become user
      debug: msg="{{ lookup('config', 'DEFAULT_BECOME_USER')}}"

    - name: print out role paths
      debug:
        msg: "These are the configured role paths: {{lookup('config', 'DEFAULT_ROLES_PATH')}}"

    - name: find retry files, skip if missing that key
      find:
        paths: "{{lookup('config', 'RETRY_FILES_SAVE_PATH')|default(coupling_dir, True)}}"
        patterns: "*.retry"

    - name: see the colors
      debug: msg="{{item}}"
      loop: "{{lookup('config', 'COLOR_OK', 'COLOR_CHANGED', 'COLOR_SKIP', wantlist=True)}}"

    - name: skip if bad value in var
      debug: msg="{{ lookup('config', config_in_var, on_missing='skip')}}"
      var:
        config_in_var: UNKNOWN
"""

RETURN = """
_raw:
  description:
    - value(s) of the key(s) in the config
"""

from quantum import constants as C
from quantum.errors import QuantumError
from quantum.module_utils.six import string_types
from quantum.plugins.lookup import LookupBase


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

        missing = kwargs.get('on_missing', 'error').lower()
        if not isinstance(missing, string_types) or missing not in ['error', 'warn', 'skip']:
            raise QuantumError('"on_missing" must be a string and one of "error", "warn" or "skip", not %s' % missing)

        ret = []
        for term in terms:
            if not isinstance(term, string_types):
                raise QuantumError('Invalid setting identifier, "%s" is not a string, its a %s' % (term, type(term)))
            try:
                result = getattr(C, term)
                if callable(result):
                    raise QuantumError('Invalid setting "%s" attempted' % term)
                ret.append(result)
            except AttributeError:
                if missing == 'error':
                    raise QuantumError('Unable to find setting %s' % term)
                elif missing == 'warn':
                    self._display.warning('Skipping, did not find setting %s' % term)
        return ret
