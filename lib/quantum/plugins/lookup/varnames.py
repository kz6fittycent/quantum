# (c) 2017 Quantum Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    lookup: varnames
    author: Quantum Core
    version_added: "2.8"
    short_description: Lookup matching variable names
    description:
      - Retrieves a list of matching Quantum variable names.
    options:
      _terms:
        description: List of Python regex patterns to search for in variable names.
        required: True
"""

EXAMPLES = """
- name: List variables that start with qz_
  debug: msg="{{ lookup('varnames', '^qz_.+')}}"
  vars:
    qz_1: hello
    qz_2: world
    qa_1: "I won't show"
    qz_: "I won't show either"

- name: Show all variables
  debug: msg="{{ lookup('varnames', '.+')}}"

- name: Show variables with 'hosts' in their names
  debug: msg="{{ lookup('varnames', 'hosts')}}"

- name: Find several related variables that end specific way
  debug: msg="{{ lookup('varnames', '.+_zone$', '.+_location$') }}"

"""

RETURN = """
_value:
  description:
    - List of the variable names requested.
  type: list
"""

import re

from quantum.errors import QuantumError
from quantum.module_utils._text import to_native
from quantum.module_utils.six import string_types
from quantum.plugins.lookup import LookupBase


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

        if variables is None:
            raise QuantumError('No variables available to search')

        # no options, yet
        # self.set_options(direct=kwargs)

        ret = []
        variable_names = list(variables.keys())
        for term in terms:

            if not isinstance(term, string_types):
                raise QuantumError('Invalid setting identifier, "%s" is not a string, its a %s' % (term, type(term)))

            try:
                name = re.compile(term)
            except Exception as e:
                raise QuantumError('Unable to use "%s" as a search parameter: %s' % (term, to_native(e)))

            for varname in variable_names:
                if name.search(varname):
                    ret.append(varname)

        return ret
