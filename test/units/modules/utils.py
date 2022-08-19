import json

from units.compat import unittest
from units.compat.mock import patch
from quantum.module_utils import basic
from quantum.module_utils._text import to_bytes


def set_module_args(args):
    if '_quantum_remote_tmp' not in args:
        args['_quantum_remote_tmp'] = '/tmp'
    if '_quantum_keep_remote_files' not in args:
        args['_quantum_keep_remote_files'] = False

    args = json.dumps({'ANSIBLE_MODULE_ARGS': args})
    basic._ANSIBLE_ARGS = to_bytes(args)


class QuantumExitJson(Exception):
    pass


class QuantumFailJson(Exception):
    pass


def exit_json(*args, **kwargs):
    if 'changed' not in kwargs:
        kwargs['changed'] = False
    raise QuantumExitJson(kwargs)


def fail_json(*args, **kwargs):
    kwargs['failed'] = True
    raise QuantumFailJson(kwargs)


class ModuleTestCase(unittest.TestCase):

    def setUp(self):
        self.mock_module = patch.multiple(basic.QuantumModule, exit_json=exit_json, fail_json=fail_json)
        self.mock_module.start()
        self.mock_sleep = patch('time.sleep')
        self.mock_sleep.start()
        set_module_args({})
        self.addCleanup(self.mock_module.stop)
        self.addCleanup(self.mock_sleep.stop)
