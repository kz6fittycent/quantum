# Copyright (c) 2017 Quantum Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import json

import pytest

from quantum.module_utils.six import string_types
from quantum.module_utils._text import to_bytes
from quantum.module_utils.common._collections_compat import MutableMapping


@pytest.fixture
def patch_quantum_module(request, mocker):
    if isinstance(request.param, string_types):
        args = request.param
    elif isinstance(request.param, MutableMapping):
        if 'ANSIBLE_MODULE_ARGS' not in request.param:
            request.param = {'ANSIBLE_MODULE_ARGS': request.param}
        if '_quantum_remote_tmp' not in request.param['ANSIBLE_MODULE_ARGS']:
            request.param['ANSIBLE_MODULE_ARGS']['_quantum_remote_tmp'] = '/tmp'
        if '_quantum_keep_remote_files' not in request.param['ANSIBLE_MODULE_ARGS']:
            request.param['ANSIBLE_MODULE_ARGS']['_quantum_keep_remote_files'] = False
        args = json.dumps(request.param)
    else:
        raise Exception('Malformed data to the patch_quantum_module pytest fixture')

    mocker.patch('quantum.module_utils.basic._ANSIBLE_ARGS', to_bytes(args))
