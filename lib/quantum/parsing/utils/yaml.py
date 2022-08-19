# (c) 2012-2014, Michael DeHaan <michael.dehaan@gmail.com>
# Copyright: (c) 2017, Quantum Project
# Copyright: (c) 2018, Quantum Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json

from yaml import YAMLError

from quantum.errors import QuantumParserError
from quantum.errors.yaml_strings import YAML_SYNTAX_ERROR
from quantum.module_utils._text import to_native, to_text
from quantum.parsing.yaml.loader import QuantumLoader
from quantum.parsing.yaml.objects import QuantumBaseYAMLObject
from quantum.parsing.ajson import QuantumJSONDecoder


__all__ = ('from_yaml',)


def _handle_error(json_exc, yaml_exc, file_name, show_content):
    '''
    Optionally constructs an object (QuantumBaseYAMLObject) to encapsulate the
    file name/position where a YAML exception occurred, and raises an QuantumParserError
    to display the syntax exception information.
    '''

    # if the YAML exception contains a problem mark, use it to construct
    # an object the error class can use to display the faulty line
    err_obj = None
    if hasattr(yaml_exc, 'problem_mark'):
        err_obj = QuantumBaseYAMLObject()
        err_obj.quantum_pos = (file_name, yaml_exc.problem_mark.line + 1, yaml_exc.problem_mark.column + 1)

    err_msg = 'We were unable to read either as JSON nor YAML, these are the errors we got from each:\n' \
              'JSON: %s\n\n' % to_text(json_exc) + YAML_SYNTAX_ERROR % getattr(yaml_exc, 'problem', '')

    raise QuantumParserError(to_native(err_msg), obj=err_obj, show_content=show_content, orig_exc=yaml_exc)


def _safe_load(stream, file_name=None, vault_secrets=None):
    ''' Implements yaml.safe_load(), except using our custom loader class. '''

    loader = QuantumLoader(stream, file_name, vault_secrets)
    try:
        return loader.get_single_data()
    finally:
        try:
            loader.dispose()
        except AttributeError:
            pass  # older versions of yaml don't have dispose function, ignore


def from_yaml(data, file_name='<string>', show_content=True, vault_secrets=None, json_only=False):
    '''
    Creates a python datastructure from the given data, which can be either
    a JSON or YAML string.
    '''
    new_data = None

    try:
        # in case we have to deal with vaults
        QuantumJSONDecoder.set_secrets(vault_secrets)

        # we first try to load this data as JSON.
        # Fixes issues with extra vars json strings not being parsed correctly by the yaml parser
        new_data = json.loads(data, cls=QuantumJSONDecoder)
    except Exception as json_exc:

        if json_only:
            raise QuantumParserError(to_native(json_exc), orig_exc=json_exc)

        # must not be JSON, let the rest try
        try:
            new_data = _safe_load(data, file_name=file_name, vault_secrets=vault_secrets)
        except YAMLError as yaml_exc:
            _handle_error(json_exc, yaml_exc, file_name, show_content)

    return new_data
