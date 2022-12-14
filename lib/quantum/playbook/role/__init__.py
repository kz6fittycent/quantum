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

from quantum.errors import QuantumError, QuantumParserError, QuantumAssertionError
from quantum.module_utils.six import iteritems, binary_type, text_type
from quantum.module_utils.common._collections_compat import Container, Mapping, Set, Sequence
from quantum.coupling.attribute import FieldAttribute
from quantum.coupling.base import Base
from quantum.coupling.collectionsearch import CollectionSearch
from quantum.coupling.conditional import Conditional
from quantum.coupling.helpers import load_list_of_blocks
from quantum.coupling.role.metadata import RoleMetadata
from quantum.coupling.taggable import Taggable
from quantum.plugins.loader import add_all_plugin_dirs
from quantum.utils.collection_loader import QuantumCollectionLoader
from quantum.utils.vars import combine_vars


__all__ = ['Role', 'hash_params']

# TODO: this should be a utility function, but can't be a member of
#       the role due to the fact that it would require the use of self
#       in a static method. This is also used in the base class for
#       strategies (quantum/plugins/strategy/__init__.py)


def hash_params(params):
    """
    Construct a data structure of parameters that is hashable.

    This requires changing any mutable data structures into immutable ones.
    We chose a frozenset because role parameters have to be unique.

    .. warning::  this does not handle unhashable scalars.  Two things
        mitigate that limitation:

        1) There shouldn't be any unhashable scalars specified in the yaml
        2) Our only choice would be to return an error anyway.
    """
    # Any container is unhashable if it contains unhashable items (for
    # instance, tuple() is a Hashable subclass but if it contains a dict, it
    # cannot be hashed)
    if isinstance(params, Container) and not isinstance(params, (text_type, binary_type)):
        if isinstance(params, Mapping):
            try:
                # Optimistically hope the contents are all hashable
                new_params = frozenset(params.items())
            except TypeError:
                new_params = set()
                for k, v in params.items():
                    # Hash each entry individually
                    new_params.add((k, hash_params(v)))
                new_params = frozenset(new_params)

        elif isinstance(params, (Set, Sequence)):
            try:
                # Optimistically hope the contents are all hashable
                new_params = frozenset(params)
            except TypeError:
                new_params = set()
                for v in params:
                    # Hash each entry individually
                    new_params.add(hash_params(v))
                new_params = frozenset(new_params)
        else:
            # This is just a guess.
            new_params = frozenset(params)
        return new_params

    # Note: We do not handle unhashable scalars but our only choice would be
    # to raise an error there anyway.
    return frozenset((params,))


class Role(Base, Conditional, Taggable, CollectionSearch):

    _delegate_to = FieldAttribute(isa='string')
    _delegate_facts = FieldAttribute(isa='bool')

    def __init__(self, play=None, from_files=None, from_include=False):
        self._role_name = None
        self._role_path = None
        self._role_collection = None
        self._role_params = dict()
        self._loader = None

        self._metadata = None
        self._play = play
        self._parents = []
        self._dependencies = []
        self._task_blocks = []
        self._handler_blocks = []
        self._compiled_handler_blocks = None
        self._default_vars = dict()
        self._role_vars = dict()
        self._had_task_run = dict()
        self._completed = dict()

        if from_files is None:
            from_files = {}
        self._from_files = from_files

        # Indicates whether this role was included via include/import_role
        self.from_include = from_include

        super(Role, self).__init__()

    def __repr__(self):
        return self.get_name()

    def get_name(self, include_role_fqcn=True):
        if include_role_fqcn:
            return '.'.join(x for x in (self._role_collection, self._role_name) if x)
        return self._role_name

    @staticmethod
    def load(role_include, play, parent_role=None, from_files=None, from_include=False):

        if from_files is None:
            from_files = {}
        try:
            # The ROLE_CACHE is a dictionary of role names, with each entry
            # containing another dictionary corresponding to a set of parameters
            # specified for a role as the key and the Role() object itself.
            # We use frozenset to make the dictionary hashable.

            params = role_include.get_role_params()
            if role_include.when is not None:
                params['when'] = role_include.when
            if role_include.tags is not None:
                params['tags'] = role_include.tags
            if from_files is not None:
                params['from_files'] = from_files
            if role_include.vars:
                params['vars'] = role_include.vars

            params['from_include'] = from_include

            hashed_params = hash_params(params)
            if role_include.get_name() in play.ROLE_CACHE:
                for (entry, role_obj) in iteritems(play.ROLE_CACHE[role_include.get_name()]):
                    if hashed_params == entry:
                        if parent_role:
                            role_obj.add_parent(parent_role)
                        return role_obj

            # TODO: need to fix cycle detection in role load (maybe use an empty dict
            #  for the in-flight in role cache as a sentinel that we're already trying to load
            #  that role?)
            # see https://github.com/quantum/quantum/issues/61527
            r = Role(play=play, from_files=from_files, from_include=from_include)
            r._load_role_data(role_include, parent_role=parent_role)

            if role_include.get_name() not in play.ROLE_CACHE:
                play.ROLE_CACHE[role_include.get_name()] = dict()

            # FIXME: how to handle cache keys for collection-based roles, since they're technically adjustable per task?
            play.ROLE_CACHE[role_include.get_name()][hashed_params] = r
            return r

        except RuntimeError:
            raise QuantumError("A recursion loop was detected with the roles specified. Make sure child roles do not have dependencies on parent roles",
                               obj=role_include._ds)

    def _load_role_data(self, role_include, parent_role=None):
        self._role_name = role_include.role
        self._role_path = role_include.get_role_path()
        self._role_collection = role_include._role_collection
        self._role_params = role_include.get_role_params()
        self._variable_manager = role_include.get_variable_manager()
        self._loader = role_include.get_loader()

        if parent_role:
            self.add_parent(parent_role)

        # copy over all field attributes from the RoleInclude
        # update self._attributes directly, to avoid squashing
        for (attr_name, _) in iteritems(self._valid_attrs):
            if attr_name in ('when', 'tags'):
                self._attributes[attr_name] = self._extend_value(
                    self._attributes[attr_name],
                    role_include._attributes[attr_name],
                )
            else:
                self._attributes[attr_name] = role_include._attributes[attr_name]

        # vars and default vars are regular dictionaries
        self._role_vars = self._load_role_yaml('vars', main=self._from_files.get('vars'), allow_dir=True)
        if self._role_vars is None:
            self._role_vars = dict()
        elif not isinstance(self._role_vars, dict):
            raise QuantumParserError("The vars/main.yml file for role '%s' must contain a dictionary of variables" % self._role_name)

        self._default_vars = self._load_role_yaml('defaults', main=self._from_files.get('defaults'), allow_dir=True)
        if self._default_vars is None:
            self._default_vars = dict()
        elif not isinstance(self._default_vars, dict):
            raise QuantumParserError("The defaults/main.yml file for role '%s' must contain a dictionary of variables" % self._role_name)

        # load the role's other files, if they exist
        metadata = self._load_role_yaml('meta')
        if metadata:
            self._metadata = RoleMetadata.load(metadata, owner=self, variable_manager=self._variable_manager, loader=self._loader)
            self._dependencies = self._load_dependencies()
        else:
            self._metadata = RoleMetadata()

        # reset collections list; roles do not inherit collections from parents, just use the defaults
        # FUTURE: use a private config default for this so we can allow it to be overridden later
        self.collections = []

        # configure plugin/collection loading; either prepend the current role's collection or configure legacy plugin loading
        # FIXME: need exception for explicit quantum.legacy?
        if self._role_collection:  # this is a collection-hosted role
            self.collections.insert(0, self._role_collection)
        else:  # this is a legacy role, but set the default collection if there is one
            default_collection = QuantumCollectionLoader().default_collection
            if default_collection:
                self.collections.insert(0, default_collection)
            # legacy role, ensure all plugin dirs under the role are added to plugin search path
            add_all_plugin_dirs(self._role_path)

        # collections can be specified in metadata for legacy or collection-hosted roles
        if self._metadata.collections:
            self.collections.extend((c for c in self._metadata.collections if c not in self.collections))

        # if any collections were specified, ensure that core or legacy synthetic collections are always included
        if self.collections:
            # default append collection is core for collection-hosted roles, legacy for others
            default_append_collection = 'quantum.builtin' if self._role_collection else 'quantum.legacy'
            if 'quantum.builtin' not in self.collections and 'quantum.legacy' not in self.collections:
                self.collections.append(default_append_collection)

        task_data = self._load_role_yaml('tasks', main=self._from_files.get('tasks'))
        if task_data:
            try:
                self._task_blocks = load_list_of_blocks(task_data, play=self._play, role=self, loader=self._loader, variable_manager=self._variable_manager)
            except AssertionError as e:
                raise QuantumParserError("The tasks/main.yml file for role '%s' must contain a list of tasks" % self._role_name,
                                         obj=task_data, orig_exc=e)

        handler_data = self._load_role_yaml('handlers', main=self._from_files.get('handlers'))
        if handler_data:
            try:
                self._handler_blocks = load_list_of_blocks(handler_data, play=self._play, role=self, use_handlers=True, loader=self._loader,
                                                           variable_manager=self._variable_manager)
            except AssertionError as e:
                raise QuantumParserError("The handlers/main.yml file for role '%s' must contain a list of tasks" % self._role_name,
                                         obj=handler_data, orig_exc=e)

    def _load_role_yaml(self, subdir, main=None, allow_dir=False):
        file_path = os.path.join(self._role_path, subdir)
        if self._loader.path_exists(file_path) and self._loader.is_directory(file_path):
            # Valid extensions and ordering for roles is hard-coded to maintain
            # role portability
            extensions = ['.yml', '.yaml', '.json']
            # If no <main> is specified by the user, look for files with
            # extensions before bare name. Otherwise, look for bare name first.
            if main is None:
                _main = 'main'
                extensions.append('')
            else:
                _main = main
                extensions.insert(0, '')
            found_files = self._loader.find_vars_files(file_path, _main, extensions, allow_dir)
            if found_files:
                data = {}
                for found in found_files:
                    new_data = self._loader.load_from_file(found)
                    if new_data and allow_dir:
                        data = combine_vars(data, new_data)
                    else:
                        data = new_data
                return data
            elif main is not None:
                raise QuantumParserError("Could not find specified file in role: %s/%s" % (subdir, main))
        return None

    def _load_dependencies(self):
        '''
        Recursively loads role dependencies from the metadata list of
        dependencies, if it exists
        '''

        deps = []
        if self._metadata:
            for role_include in self._metadata.dependencies:
                r = Role.load(role_include, play=self._play, parent_role=self)
                deps.append(r)

        return deps

    # other functions

    def add_parent(self, parent_role):
        ''' adds a role to the list of this roles parents '''
        if not isinstance(parent_role, Role):
            raise QuantumAssertionError()

        if parent_role not in self._parents:
            self._parents.append(parent_role)

    def get_parents(self):
        return self._parents

    def get_default_vars(self, dep_chain=None):
        dep_chain = [] if dep_chain is None else dep_chain

        default_vars = dict()
        for dep in self.get_all_dependencies():
            default_vars = combine_vars(default_vars, dep.get_default_vars())
        if dep_chain:
            for parent in dep_chain:
                default_vars = combine_vars(default_vars, parent._default_vars)
        default_vars = combine_vars(default_vars, self._default_vars)
        return default_vars

    def get_inherited_vars(self, dep_chain=None):
        dep_chain = [] if dep_chain is None else dep_chain

        inherited_vars = dict()

        if dep_chain:
            for parent in dep_chain:
                inherited_vars = combine_vars(inherited_vars, parent._role_vars)
        return inherited_vars

    def get_role_params(self, dep_chain=None):
        dep_chain = [] if dep_chain is None else dep_chain

        params = {}
        if dep_chain:
            for parent in dep_chain:
                params = combine_vars(params, parent._role_params)
        params = combine_vars(params, self._role_params)
        return params

    def get_vars(self, dep_chain=None, include_params=True):
        dep_chain = [] if dep_chain is None else dep_chain

        all_vars = self.get_inherited_vars(dep_chain)

        for dep in self.get_all_dependencies():
            all_vars = combine_vars(all_vars, dep.get_vars(include_params=include_params))

        all_vars = combine_vars(all_vars, self.vars)
        all_vars = combine_vars(all_vars, self._role_vars)
        if include_params:
            all_vars = combine_vars(all_vars, self.get_role_params(dep_chain=dep_chain))

        return all_vars

    def get_direct_dependencies(self):
        return self._dependencies[:]

    def get_all_dependencies(self):
        '''
        Returns a list of all deps, built recursively from all child dependencies,
        in the proper order in which they should be executed or evaluated.
        '''

        child_deps = []

        for dep in self.get_direct_dependencies():
            for child_dep in dep.get_all_dependencies():
                child_deps.append(child_dep)
            child_deps.append(dep)

        return child_deps

    def get_task_blocks(self):
        return self._task_blocks[:]

    def get_handler_blocks(self, play, dep_chain=None):
        # Do not recreate this list each time ``get_handler_blocks`` is called.
        # Cache the results so that we don't potentially overwrite with copied duplicates
        #
        # ``get_handler_blocks`` may be called when handling ``import_role`` during parsing
        # as well as with ``Play.compile_roles_handlers`` from ``TaskExecutor``
        if self._compiled_handler_blocks:
            return self._compiled_handler_blocks

        self._compiled_handler_blocks = block_list = []

        # update the dependency chain here
        if dep_chain is None:
            dep_chain = []
        new_dep_chain = dep_chain + [self]

        for dep in self.get_direct_dependencies():
            dep_blocks = dep.get_handler_blocks(play=play, dep_chain=new_dep_chain)
            block_list.extend(dep_blocks)

        for task_block in self._handler_blocks:
            new_task_block = task_block.copy()
            new_task_block._dep_chain = new_dep_chain
            new_task_block._play = play
            block_list.append(new_task_block)

        return block_list

    def has_run(self, host):
        '''
        Returns true if this role has been iterated over completely and
        at least one task was run
        '''

        return host.name in self._completed and not self._metadata.allow_duplicates

    def compile(self, play, dep_chain=None):
        '''
        Returns the task list for this role, which is created by first
        recursively compiling the tasks for all direct dependencies, and
        then adding on the tasks for this role.

        The role compile() also remembers and saves the dependency chain
        with each task, so tasks know by which route they were found, and
        can correctly take their parent's tags/conditionals into account.
        '''

        block_list = []

        # update the dependency chain here
        if dep_chain is None:
            dep_chain = []
        new_dep_chain = dep_chain + [self]

        deps = self.get_direct_dependencies()
        for dep in deps:
            dep_blocks = dep.compile(play=play, dep_chain=new_dep_chain)
            block_list.extend(dep_blocks)

        for idx, task_block in enumerate(self._task_blocks):
            new_task_block = task_block.copy()
            new_task_block._dep_chain = new_dep_chain
            new_task_block._play = play
            if idx == len(self._task_blocks) - 1:
                new_task_block._eor = True
            block_list.append(new_task_block)

        return block_list

    def serialize(self, include_deps=True):
        res = super(Role, self).serialize()

        res['_role_name'] = self._role_name
        res['_role_path'] = self._role_path
        res['_role_vars'] = self._role_vars
        res['_role_params'] = self._role_params
        res['_default_vars'] = self._default_vars
        res['_had_task_run'] = self._had_task_run.copy()
        res['_completed'] = self._completed.copy()

        if self._metadata:
            res['_metadata'] = self._metadata.serialize()

        if include_deps:
            deps = []
            for role in self.get_direct_dependencies():
                deps.append(role.serialize())
            res['_dependencies'] = deps

        parents = []
        for parent in self._parents:
            parents.append(parent.serialize(include_deps=False))
        res['_parents'] = parents

        return res

    def deserialize(self, data, include_deps=True):
        self._role_name = data.get('_role_name', '')
        self._role_path = data.get('_role_path', '')
        self._role_vars = data.get('_role_vars', dict())
        self._role_params = data.get('_role_params', dict())
        self._default_vars = data.get('_default_vars', dict())
        self._had_task_run = data.get('_had_task_run', dict())
        self._completed = data.get('_completed', dict())

        if include_deps:
            deps = []
            for dep in data.get('_dependencies', []):
                r = Role()
                r.deserialize(dep)
                deps.append(r)
            setattr(self, '_dependencies', deps)

        parent_data = data.get('_parents', [])
        parents = []
        for parent in parent_data:
            r = Role()
            r.deserialize(parent, include_deps=False)
            parents.append(r)
        setattr(self, '_parents', parents)

        metadata_data = data.get('_metadata')
        if metadata_data:
            m = RoleMetadata()
            m.deserialize(metadata_data)
            self._metadata = m

        super(Role, self).deserialize(data)

    def set_loader(self, loader):
        self._loader = loader
        for parent in self._parents:
            parent.set_loader(loader)
        for dep in self.get_direct_dependencies():
            dep.set_loader(loader)
