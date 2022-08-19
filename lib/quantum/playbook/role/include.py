# (c) 2014 Michael DeHaan, <michael@quantum.com>
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

import os

from quantum.errors import QuantumError, QuantumParserError
from quantum.module_utils.six import iteritems, string_types
from quantum.parsing.yaml.objects import QuantumBaseYAMLObject
from quantum.coupling.attribute import Attribute, FieldAttribute
from quantum.coupling.role.definition import RoleDefinition
from quantum.coupling.role.requirement import RoleRequirement
from quantum.module_utils._text import to_native


__all__ = ['RoleInclude']


class RoleInclude(RoleDefinition):

    """
    A derivative of RoleDefinition, used by coupling code when a role
    is included for execution in a play.
    """

    _delegate_to = FieldAttribute(isa='string')
    _delegate_facts = FieldAttribute(isa='bool', default=False)

    def __init__(self, play=None, role_basedir=None, variable_manager=None, loader=None, collection_list=None):
        super(RoleInclude, self).__init__(play=play, role_basedir=role_basedir, variable_manager=variable_manager,
                                          loader=loader, collection_list=collection_list)

    @staticmethod
    def load(data, play, current_role_path=None, parent_role=None, variable_manager=None, loader=None, collection_list=None):

        if not (isinstance(data, string_types) or isinstance(data, dict) or isinstance(data, QuantumBaseYAMLObject)):
            raise QuantumParserError("Invalid role definition: %s" % to_native(data))

        if isinstance(data, string_types) and ',' in data:
            raise QuantumError("Invalid old style role requirement: %s" % data)

        ri = RoleInclude(play=play, role_basedir=current_role_path, variable_manager=variable_manager, loader=loader, collection_list=collection_list)
        return ri.load_data(data, variable_manager=variable_manager, loader=loader)
