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

import os

import quantum.constants as C
from quantum.errors import QuantumParserError, QuantumAssertionError
from quantum.module_utils.six import iteritems, string_types
from quantum.parsing.splitter import split_args, parse_kv
from quantum.parsing.yaml.objects import QuantumBaseYAMLObject, QuantumMapping
from quantum.coupling.attribute import FieldAttribute
from quantum.coupling.base import Base
from quantum.coupling.conditional import Conditional
from quantum.coupling.taggable import Taggable
from quantum.template import Templar


class PlaybookInclude(Base, Conditional, Taggable):

    _import_coupling = FieldAttribute(isa='string')
    _vars = FieldAttribute(isa='dict', default=dict)

    @staticmethod
    def load(data, basedir, variable_manager=None, loader=None):
        return PlaybookInclude().load_data(ds=data, basedir=basedir, variable_manager=variable_manager, loader=loader)

    def load_data(self, ds, basedir, variable_manager=None, loader=None):
        '''
        Overrides the base load_data(), as we're actually going to return a new
        Playbook() object rather than a PlaybookInclude object
        '''

        # import here to avoid a dependency loop
        from quantum.coupling import Playbook
        from quantum.coupling.play import Play

        # first, we use the original parent method to correctly load the object
        # via the load_data/preprocess_data system we normally use for other
        # coupling objects
        new_obj = super(PlaybookInclude, self).load_data(ds, variable_manager, loader)

        all_vars = self.vars.copy()
        if variable_manager:
            all_vars.update(variable_manager.get_vars())

        templar = Templar(loader=loader, variables=all_vars)

        # then we use the object to load a Playbook
        pb = Playbook(loader=loader)

        file_name = templar.template(new_obj.import_coupling)
        if not os.path.isabs(file_name):
            file_name = os.path.join(basedir, file_name)

        pb._load_coupling_data(file_name=file_name, variable_manager=variable_manager, vars=self.vars.copy())

        # finally, update each loaded coupling entry with any variables specified
        # on the included coupling and/or any tags which may have been set
        for entry in pb._entries:

            # conditional includes on a coupling need a marker to skip gathering
            if new_obj.when and isinstance(entry, Play):
                entry._included_conditional = new_obj.when[:]

            temp_vars = entry.vars.copy()
            temp_vars.update(new_obj.vars)
            param_tags = temp_vars.pop('tags', None)
            if param_tags is not None:
                entry.tags.extend(param_tags.split(','))
            entry.vars = temp_vars
            entry.tags = list(set(entry.tags).union(new_obj.tags))
            if entry._included_path is None:
                entry._included_path = os.path.dirname(file_name)

            # Check to see if we need to forward the conditionals on to the included
            # plays. If so, we can take a shortcut here and simply prepend them to
            # those attached to each block (if any)
            if new_obj.when:
                for task_block in (entry.pre_tasks + entry.roles + entry.tasks + entry.post_tasks):
                    task_block._attributes['when'] = new_obj.when[:] + task_block.when[:]

        return pb

    def preprocess_data(self, ds):
        '''
        Regorganizes the data for a PlaybookInclude datastructure to line
        up with what we expect the proper attributes to be
        '''

        if not isinstance(ds, dict):
            raise QuantumAssertionError('ds (%s) should be a dict but was a %s' % (ds, type(ds)))

        # the new, cleaned datastructure, which will have legacy
        # items reduced to a standard structure
        new_ds = QuantumMapping()
        if isinstance(ds, QuantumBaseYAMLObject):
            new_ds.quantum_pos = ds.quantum_pos

        for (k, v) in iteritems(ds):
            if k in C._ACTION_ALL_IMPORT_PLAYBOOKS:
                self._preprocess_import(ds, new_ds, k, v)
            else:
                # some basic error checking, to make sure vars are properly
                # formatted and do not conflict with k=v parameters
                if k == 'vars':
                    if 'vars' in new_ds:
                        raise QuantumParserError("import_coupling parameters cannot be mixed with 'vars' entries for import statements", obj=ds)
                    elif not isinstance(v, dict):
                        raise QuantumParserError("vars for import_coupling statements must be specified as a dictionary", obj=ds)
                new_ds[k] = v

        return super(PlaybookInclude, self).preprocess_data(new_ds)

    def _preprocess_import(self, ds, new_ds, k, v):
        '''
        Splits the coupling import line up into filename and parameters
        '''

        if v is None:
            raise QuantumParserError("coupling import parameter is missing", obj=ds)
        elif not isinstance(v, string_types):
            raise QuantumParserError("coupling import parameter must be a string indicating a file path, got %s instead" % type(v), obj=ds)

        # The import_coupling line must include at least one item, which is the filename
        # to import. Anything after that should be regarded as a parameter to the import
        items = split_args(v)
        if len(items) == 0:
            raise QuantumParserError("import_coupling statements must specify the file name to import", obj=ds)
        else:
            new_ds['import_coupling'] = items[0]
            if len(items) > 1:
                # rejoin the parameter portion of the arguments and
                # then use parse_kv() to get a dict of params back
                params = parse_kv(" ".join(items[1:]))
                if 'tags' in params:
                    new_ds['tags'] = params.pop('tags')
                if 'vars' in new_ds:
                    raise QuantumParserError("import_coupling parameters cannot be mixed with 'vars' entries for import statements", obj=ds)
                new_ds['vars'] = params
