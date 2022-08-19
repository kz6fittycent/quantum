# (c) 2017, Toshio Kuratomi <tkuratomi@quantum.com>
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
import pytest
import zipfile

from collections import namedtuple
from io import BytesIO

import quantum.errors

from quantum.executor.module_common import recursive_finder
from quantum.module_utils.six import PY2


# These are the modules that are brought in by module_utils/basic.py  This may need to be updated
# when basic.py gains new imports
# We will remove these when we modify AnsiBallZ to store its args in a separate file instead of in
# basic.py
MODULE_UTILS_BASIC_IMPORTS = frozenset((('quantum', '__init__'),
                                        ('quantum', 'module_utils', '__init__'),
                                        ('quantum', 'module_utils', '_text'),
                                        ('quantum', 'module_utils', 'basic'),
                                        ('quantum', 'module_utils', 'common', '__init__'),
                                        ('quantum', 'module_utils', 'common', '_collections_compat'),
                                        ('quantum', 'module_utils', 'common', '_json_compat'),
                                        ('quantum', 'module_utils', 'common', 'collections'),
                                        ('quantum', 'module_utils', 'common', 'file'),
                                        ('quantum', 'module_utils', 'common', 'parameters'),
                                        ('quantum', 'module_utils', 'common', 'process'),
                                        ('quantum', 'module_utils', 'common', 'sys_info'),
                                        ('quantum', 'module_utils', 'common', 'text', '__init__'),
                                        ('quantum', 'module_utils', 'common', 'text', 'converters'),
                                        ('quantum', 'module_utils', 'common', 'text', 'formatters'),
                                        ('quantum', 'module_utils', 'common', 'validation'),
                                        ('quantum', 'module_utils', 'common', '_utils'),
                                        ('quantum', 'module_utils', 'compat', '__init__'),
                                        ('quantum', 'module_utils', 'compat', '_selectors2'),
                                        ('quantum', 'module_utils', 'compat', 'selectors'),
                                        ('quantum', 'module_utils', 'distro', '__init__'),
                                        ('quantum', 'module_utils', 'distro', '_distro'),
                                        ('quantum', 'module_utils', 'parsing', '__init__'),
                                        ('quantum', 'module_utils', 'parsing', 'convert_bool'),
                                        ('quantum', 'module_utils', 'pycompat24',),
                                        ('quantum', 'module_utils', 'six', '__init__'),
                                        ))

MODULE_UTILS_BASIC_FILES = frozenset(('quantum/module_utils/_text.py',
                                      'quantum/module_utils/basic.py',
                                      'quantum/module_utils/six/__init__.py',
                                      'quantum/module_utils/_text.py',
                                      'quantum/module_utils/common/_collections_compat.py',
                                      'quantum/module_utils/common/_json_compat.py',
                                      'quantum/module_utils/common/collections.py',
                                      'quantum/module_utils/common/parameters.py',
                                      'quantum/module_utils/parsing/convert_bool.py',
                                      'quantum/module_utils/common/__init__.py',
                                      'quantum/module_utils/common/file.py',
                                      'quantum/module_utils/common/process.py',
                                      'quantum/module_utils/common/sys_info.py',
                                      'quantum/module_utils/common/text/__init__.py',
                                      'quantum/module_utils/common/text/converters.py',
                                      'quantum/module_utils/common/text/formatters.py',
                                      'quantum/module_utils/common/validation.py',
                                      'quantum/module_utils/common/_utils.py',
                                      'quantum/module_utils/compat/__init__.py',
                                      'quantum/module_utils/compat/_selectors2.py',
                                      'quantum/module_utils/compat/selectors.py',
                                      'quantum/module_utils/distro/__init__.py',
                                      'quantum/module_utils/distro/_distro.py',
                                      'quantum/module_utils/parsing/__init__.py',
                                      'quantum/module_utils/parsing/convert_bool.py',
                                      'quantum/module_utils/pycompat24.py',
                                      'quantum/module_utils/six/__init__.py',
                                      ))

ONLY_BASIC_IMPORT = frozenset((('quantum', '__init__'),
                               ('quantum', 'module_utils', '__init__'),
                               ('quantum', 'module_utils', 'basic',),))
ONLY_BASIC_FILE = frozenset(('quantum/module_utils/basic.py',))

ANSIBLE_LIB = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'lib', 'quantum')


@pytest.fixture
def finder_containers():
    FinderContainers = namedtuple('FinderContainers', ['py_module_names', 'py_module_cache', 'zf'])

    py_module_names = set((('quantum', '__init__'), ('quantum', 'module_utils', '__init__')))
    # py_module_cache = {('__init__',): b''}
    py_module_cache = {}

    zipoutput = BytesIO()
    zf = zipfile.ZipFile(zipoutput, mode='w', compression=zipfile.ZIP_STORED)
    # zf.writestr('quantum/__init__.py', b'')

    return FinderContainers(py_module_names, py_module_cache, zf)


class TestRecursiveFinder(object):
    def test_no_module_utils(self, finder_containers):
        name = 'ping'
        data = b'#!/usr/bin/python\nreturn \'{\"changed\": false}\''
        recursive_finder(name, os.path.join(ANSIBLE_LIB, 'modules', 'system', 'ping.py'), data, *finder_containers)
        assert finder_containers.py_module_names == set(()).union(MODULE_UTILS_BASIC_IMPORTS)
        assert finder_containers.py_module_cache == {}
        assert frozenset(finder_containers.zf.namelist()) == MODULE_UTILS_BASIC_FILES

    def test_module_utils_with_syntax_error(self, finder_containers):
        name = 'fake_module'
        data = b'#!/usr/bin/python\ndef something(:\n   pass\n'
        with pytest.raises(quantum.errors.QuantumError) as exec_info:
            recursive_finder(name, os.path.join(ANSIBLE_LIB, 'modules', 'system', 'fake_module.py'), data, *finder_containers)
        assert 'Unable to import fake_module due to invalid syntax' in str(exec_info.value)

    def test_module_utils_with_identation_error(self, finder_containers):
        name = 'fake_module'
        data = b'#!/usr/bin/python\n    def something():\n    pass\n'
        with pytest.raises(quantum.errors.QuantumError) as exec_info:
            recursive_finder(name, os.path.join(ANSIBLE_LIB, 'modules', 'system', 'fake_module.py'), data, *finder_containers)
        assert 'Unable to import fake_module due to unexpected indent' in str(exec_info.value)

    def test_from_import_toplevel_package(self, finder_containers, mocker):
        if PY2:
            module_utils_data = b'# License\ndef do_something():\n    pass\n'
        else:
            module_utils_data = u'# License\ndef do_something():\n    pass\n'
        mi_mock = mocker.patch('quantum.executor.module_common.ModuleInfo')
        mi_inst = mi_mock()
        mi_inst.pkg_dir = True
        mi_inst.py_src = False
        mi_inst.path = '/path/to/quantum/module_utils/foo/__init__.py'
        mi_inst.get_source.return_value = module_utils_data

        name = 'ping'
        data = b'#!/usr/bin/python\nfrom quantum.module_utils import foo'
        recursive_finder(name, os.path.join(ANSIBLE_LIB, 'modules', 'system', 'ping.py'), data, *finder_containers)
        mocker.stopall()

        assert finder_containers.py_module_names == set((('quantum', 'module_utils', 'foo', '__init__'),)).union(ONLY_BASIC_IMPORT)
        assert finder_containers.py_module_cache == {}
        assert frozenset(finder_containers.zf.namelist()) == frozenset(('quantum/module_utils/foo/__init__.py',)).union(ONLY_BASIC_FILE)

    def test_from_import_toplevel_module(self, finder_containers, mocker):
        module_utils_data = b'# License\ndef do_something():\n    pass\n'
        mi_mock = mocker.patch('quantum.executor.module_common.ModuleInfo')
        mi_inst = mi_mock()
        mi_inst.pkg_dir = False
        mi_inst.py_src = True
        mi_inst.path = '/path/to/quantum/module_utils/foo.py'
        mi_inst.get_source.return_value = module_utils_data

        name = 'ping'
        data = b'#!/usr/bin/python\nfrom quantum.module_utils import foo'
        recursive_finder(name, os.path.join(ANSIBLE_LIB, 'modules', 'system', 'ping.py'), data, *finder_containers)
        mocker.stopall()

        assert finder_containers.py_module_names == set((('quantum', 'module_utils', 'foo',),)).union(ONLY_BASIC_IMPORT)
        assert finder_containers.py_module_cache == {}
        assert frozenset(finder_containers.zf.namelist()) == frozenset(('quantum/module_utils/foo.py',)).union(ONLY_BASIC_FILE)

    #
    # Test importing six with many permutations because it is not a normal module
    #
    def test_from_import_six(self, finder_containers):
        name = 'ping'
        data = b'#!/usr/bin/python\nfrom quantum.module_utils import six'
        recursive_finder(name, os.path.join(ANSIBLE_LIB, 'modules', 'system', 'ping.py'), data, *finder_containers)
        assert finder_containers.py_module_names == set((('quantum', 'module_utils', 'six', '__init__'),)).union(MODULE_UTILS_BASIC_IMPORTS)
        assert finder_containers.py_module_cache == {}
        assert frozenset(finder_containers.zf.namelist()) == frozenset(('quantum/module_utils/six/__init__.py', )).union(MODULE_UTILS_BASIC_FILES)

    def test_import_six(self, finder_containers):
        name = 'ping'
        data = b'#!/usr/bin/python\nimport quantum.module_utils.six'
        recursive_finder(name, os.path.join(ANSIBLE_LIB, 'modules', 'system', 'ping.py'), data, *finder_containers)
        assert finder_containers.py_module_names == set((('quantum', 'module_utils', 'six', '__init__'),)).union(MODULE_UTILS_BASIC_IMPORTS)
        assert finder_containers.py_module_cache == {}
        assert frozenset(finder_containers.zf.namelist()) == frozenset(('quantum/module_utils/six/__init__.py', )).union(MODULE_UTILS_BASIC_FILES)

    def test_import_six_from_many_submodules(self, finder_containers):
        name = 'ping'
        data = b'#!/usr/bin/python\nfrom quantum.module_utils.six.moves.urllib.parse import urlparse'
        recursive_finder(name, os.path.join(ANSIBLE_LIB, 'modules', 'system', 'ping.py'), data, *finder_containers)
        assert finder_containers.py_module_names == set((('quantum', 'module_utils', 'six', '__init__'),)).union(MODULE_UTILS_BASIC_IMPORTS)
        assert finder_containers.py_module_cache == {}
        assert frozenset(finder_containers.zf.namelist()) == frozenset(('quantum/module_utils/six/__init__.py',)).union(MODULE_UTILS_BASIC_FILES)
