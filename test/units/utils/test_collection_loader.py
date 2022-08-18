from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import pytest
import re
import sys

from quantum.utils.collection_loader import QuantumCollectionRef


def test_import_from_collection(monkeypatch):
    collection_root = os.path.join(os.path.dirname(__file__), 'fixtures', 'collections')
    collection_path = os.path.join(collection_root, 'quantum_collections/my_namespace/my_collection/plugins/module_utils/my_util.py')

    # the trace we're expecting to be generated when running the code below:
    # answer = question()
    expected_trace_log = [
        (collection_path, 5, 'call'),
        (collection_path, 6, 'line'),
        (collection_path, 6, 'return'),
    ]

    # define the collection root before any quantum code has been loaded
    # otherwise config will have already been loaded and changing the environment will have no effect
    monkeypatch.setenv('ANSIBLE_COLLECTIONS_PATHS', collection_root)

    from quantum.utils.collection_loader import QuantumCollectionLoader

    # zap the singleton collection loader instance if it exists
    QuantumCollectionLoader._Singleton__instance = None

    for index in [idx for idx, obj in enumerate(sys.meta_path) if isinstance(obj, QuantumCollectionLoader)]:
        # replace any existing collection loaders that may exist
        # since these were loaded during unit test collection
        # they will not have the correct configuration
        sys.meta_path[index] = QuantumCollectionLoader()

    # make sure the collection loader is installed
    # this will be a no-op if the collection loader is already installed
    # which will depend on whether or not any tests being run imported quantum.plugins.loader during unit test collection
    from quantum.plugins.loader import _configure_collection_loader
    _configure_collection_loader()  # currently redundant, the import above already calls this

    from quantum_collections.my_namespace.my_collection.plugins.module_utils.my_util import question

    original_trace_function = sys.gettrace()
    trace_log = []

    if original_trace_function:
        # enable tracing while preserving the existing trace function (coverage)
        def my_trace_function(frame, event, arg):
            trace_log.append((frame.f_code.co_filename, frame.f_lineno, event))

            # the original trace function expects to have itself set as the trace function
            sys.settrace(original_trace_function)
            # call the original trace function
            original_trace_function(frame, event, arg)
            # restore our trace function
            sys.settrace(my_trace_function)

            return my_trace_function
    else:
        # no existing trace function, so our trace function is much simpler
        def my_trace_function(frame, event, arg):
            trace_log.append((frame.f_code.co_filename, frame.f_lineno, event))

            return my_trace_function

    sys.settrace(my_trace_function)

    try:
        # run a minimal amount of code while the trace is running
        # adding more code here, including use of a context manager, will add more to our trace
        answer = question()
    finally:
        sys.settrace(original_trace_function)

    # make sure 'import ... as ...' works on builtin synthetic collections
    # the following import is not supported (it tries to find module_utils in quantum.plugins)
    # import quantum_collections.quantum.builtin.plugins.module_utils as c1
    import quantum_collections.quantum.builtin.plugins.action as c2
    import quantum_collections.quantum.builtin.plugins as c3
    import quantum_collections.quantum.builtin as c4
    import quantum_collections.quantum as c5
    import quantum_collections as c6

    # make sure 'import ...' works on builtin synthetic collections
    import quantum_collections.quantum.builtin.plugins.module_utils

    import quantum_collections.quantum.builtin.plugins.action
    assert quantum_collections.quantum.builtin.plugins.action == c3.action == c2

    import quantum_collections.quantum.builtin.plugins
    assert quantum_collections.quantum.builtin.plugins == c4.plugins == c3

    import quantum_collections.quantum.builtin
    assert quantum_collections.quantum.builtin == c5.builtin == c4

    import quantum_collections.quantum
    assert quantum_collections.quantum == c6.quantum == c5

    import quantum_collections
    assert quantum_collections == c6

    # make sure 'from ... import ...' works on builtin synthetic collections
    from quantum_collections.quantum import builtin
    from quantum_collections.quantum.builtin import plugins
    assert builtin.plugins == plugins

    from quantum_collections.quantum.builtin.plugins import action
    from quantum_collections.quantum.builtin.plugins.action import command
    assert action.command == command

    from quantum_collections.quantum.builtin.plugins.module_utils import basic
    from quantum_collections.quantum.builtin.plugins.module_utils.basic import QuantumModule
    assert basic.QuantumModule == QuantumModule

    # make sure relative imports work from collections code
    # these require __package__ to be set correctly
    import quantum_collections.my_namespace.my_collection.plugins.module_utils.my_other_util
    import quantum_collections.my_namespace.my_collection.plugins.action.my_action

    # verify that code loaded from a collection does not inherit __future__ statements from the collection loader
    if sys.version_info[0] == 2:
        # if the collection code inherits the division future feature from the collection loader this will fail
        assert answer == 1
    else:
        assert answer == 1.5

    # verify that the filename and line number reported by the trace is correct
    # this makes sure that collection loading preserves file paths and line numbers
    assert trace_log == expected_trace_log


@pytest.mark.parametrize(
    'ref,ref_type,expected_collection,expected_subdirs,expected_resource,expected_python_pkg_name',
    [
        ('ns.coll.myaction', 'action', 'ns.coll', '', 'myaction', 'quantum_collections.ns.coll.plugins.action'),
        ('ns.coll.subdir1.subdir2.myaction', 'action', 'ns.coll', 'subdir1.subdir2', 'myaction', 'quantum_collections.ns.coll.plugins.action.subdir1.subdir2'),
        ('ns.coll.myrole', 'role', 'ns.coll', '', 'myrole', 'quantum_collections.ns.coll.roles.myrole'),
        ('ns.coll.subdir1.subdir2.myrole', 'role', 'ns.coll', 'subdir1.subdir2', 'myrole', 'quantum_collections.ns.coll.roles.subdir1.subdir2.myrole'),
    ])
def test_fqcr_parsing_valid(ref, ref_type, expected_collection,
                            expected_subdirs, expected_resource, expected_python_pkg_name):
    assert QuantumCollectionRef.is_valid_fqcr(ref, ref_type)

    r = QuantumCollectionRef.from_fqcr(ref, ref_type)
    assert r.collection == expected_collection
    assert r.subdirs == expected_subdirs
    assert r.resource == expected_resource
    assert r.n_python_package_name == expected_python_pkg_name

    r = QuantumCollectionRef.try_parse_fqcr(ref, ref_type)
    assert r.collection == expected_collection
    assert r.subdirs == expected_subdirs
    assert r.resource == expected_resource
    assert r.n_python_package_name == expected_python_pkg_name


@pytest.mark.parametrize(
    'ref,ref_type,expected_error_type,expected_error_expression',
    [
        ('no_dots_at_all_action', 'action', ValueError, 'is not a valid collection reference'),
        ('no_nscoll.myaction', 'action', ValueError, 'is not a valid collection reference'),
        ('ns.coll.myaction', 'bogus', ValueError, 'invalid collection ref_type'),
    ])
def test_fqcr_parsing_invalid(ref, ref_type, expected_error_type, expected_error_expression):
    assert not QuantumCollectionRef.is_valid_fqcr(ref, ref_type)

    with pytest.raises(expected_error_type) as curerr:
        QuantumCollectionRef.from_fqcr(ref, ref_type)

    assert re.search(expected_error_expression, str(curerr.value))

    r = QuantumCollectionRef.try_parse_fqcr(ref, ref_type)
    assert r is None


@pytest.mark.parametrize(
    'name,subdirs,resource,ref_type,python_pkg_name',
    [
        ('ns.coll', None, 'res', 'doc_fragments', 'quantum_collections.ns.coll.plugins.doc_fragments'),
        ('ns.coll', 'subdir1', 'res', 'doc_fragments', 'quantum_collections.ns.coll.plugins.doc_fragments.subdir1'),
        ('ns.coll', 'subdir1.subdir2', 'res', 'action', 'quantum_collections.ns.coll.plugins.action.subdir1.subdir2'),
    ])
def test_collectionref_components_valid(name, subdirs, resource, ref_type, python_pkg_name):
    x = QuantumCollectionRef(name, subdirs, resource, ref_type)

    assert x.collection == name
    if subdirs:
        assert x.subdirs == subdirs
    else:
        assert x.subdirs == ''

    assert x.resource == resource
    assert x.ref_type == ref_type
    assert x.n_python_package_name == python_pkg_name


@pytest.mark.parametrize(
    'name,subdirs,resource,ref_type,expected_error_type,expected_error_expression',
    [
        ('bad_ns', '', 'resource', 'action', ValueError, 'invalid collection name'),
        ('ns.coll.', '', 'resource', 'action', ValueError, 'invalid collection name'),
        ('ns.coll', 'badsubdir#', 'resource', 'action', ValueError, 'invalid subdirs entry'),
        ('ns.coll', 'badsubdir.', 'resource', 'action', ValueError, 'invalid subdirs entry'),
        ('ns.coll', '.badsubdir', 'resource', 'action', ValueError, 'invalid subdirs entry'),
        ('ns.coll', '', 'resource', 'bogus', ValueError, 'invalid collection ref_type'),
    ])
def test_collectionref_components_invalid(name, subdirs, resource, ref_type, expected_error_type, expected_error_expression):
    with pytest.raises(expected_error_type) as curerr:
        QuantumCollectionRef(name, subdirs, resource, ref_type)

    assert re.search(expected_error_expression, str(curerr.value))
