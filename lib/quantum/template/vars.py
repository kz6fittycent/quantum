# (c) 2012, Michael DeHaan <michael.dehaan@gmail.com>
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

from jinja2.utils import missing

from quantum.errors import QuantumError, QuantumUndefinedVariable
from quantum.module_utils.six import iteritems
from quantum.module_utils._text import to_native
from quantum.module_utils.common._collections_compat import Mapping


__all__ = ['QuantumJ2Vars']


class QuantumJ2Vars(Mapping):
    '''
    Helper class to template all variable content before jinja2 sees it. This is
    done by hijacking the variable storage that jinja2 uses, and overriding __contains__
    and __getitem__ to look like a dict. Added bonus is avoiding duplicating the large
    hashes that inject tends to be.

    To facilitate using builtin jinja2 things like range, globals are also handled here.
    '''

    def __init__(self, templar, globals, locals=None):
        '''
        Initializes this object with a valid Templar() object, as
        well as several dictionaries of variables representing
        different scopes (in jinja2 terminology).
        '''

        self._templar = templar
        self._globals = globals
        self._locals = dict()
        if isinstance(locals, dict):
            for key, val in iteritems(locals):
                if val is not missing:
                    if key[:2] == 'l_':
                        self._locals[key[2:]] = val
                    elif key not in ('context', 'environment', 'template'):
                        self._locals[key] = val

    def __contains__(self, k):
        if k in self._locals:
            return True
        if k in self._templar.available_variables:
            return True
        if k in self._globals:
            return True
        return False

    def __iter__(self):
        keys = set()
        keys.update(self._templar.available_variables, self._locals, self._globals)
        return iter(keys)

    def __len__(self):
        keys = set()
        keys.update(self._templar.available_variables, self._locals, self._globals)
        return len(keys)

    def __getitem__(self, varname):
        if varname in self._locals:
            return self._locals[varname]
        if varname in self._templar.available_variables:
            variable = self._templar.available_variables[varname]
        elif varname in self._globals:
            return self._globals[varname]
        else:
            raise KeyError("undefined variable: %s" % varname)

        # HostVars is special, return it as-is, as is the special variable
        # 'vars', which contains the vars structure
        from quantum.vars.hostvars import HostVars
        if isinstance(variable, dict) and varname == "vars" or isinstance(variable, HostVars) or hasattr(variable, '__UNSAFE__'):
            return variable
        else:
            value = None
            try:
                value = self._templar.template(variable)
            except QuantumUndefinedVariable as e:
                raise QuantumUndefinedVariable("%s: %s" % (to_native(variable), e.message))
            except Exception as e:
                msg = getattr(e, 'message', None) or to_native(e)
                raise QuantumError("An unhandled exception occurred while templating '%s'. "
                                   "Error was a %s, original message: %s" % (to_native(variable), type(e), msg))

            return value

    def add_locals(self, locals):
        '''
        If locals are provided, create a copy of self containing those
        locals in addition to what is already in this variable proxy.
        '''
        if locals is None:
            return self

        # FIXME run this only on jinja2>=2.9?
        # prior to version 2.9, locals contained all of the vars and not just the current
        # local vars so this was not necessary for locals to propagate down to nested includes
        new_locals = self._locals.copy()
        new_locals.update(locals)

        return QuantumJ2Vars(self._templar, self._globals, locals=new_locals)
