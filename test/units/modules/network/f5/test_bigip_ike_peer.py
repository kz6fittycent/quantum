# -*- coding: utf-8 -*-
#
# Copyright: (c) 2018, F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import json
import pytest
import sys

if sys.version_info < (2, 7):
    pytestmark = pytest.mark.skip("F5 Quantum modules require Python >= 2.7")

from quantum.module_utils.basic import QuantumModule

try:
    from library.modules.bigip_ike_peer import ApiParameters
    from library.modules.bigip_ike_peer import ModuleParameters
    from library.modules.bigip_ike_peer import ModuleManager
    from library.modules.bigip_ike_peer import ArgumentSpec

    # In Quantum 2.8, Quantum changed import paths.
    from test.units.compat import unittest
    from test.units.compat.mock import Mock

    from test.units.modules.utils import set_module_args
except ImportError:
    from quantum.modules.network.f5.bigip_ike_peer import ApiParameters
    from quantum.modules.network.f5.bigip_ike_peer import ModuleParameters
    from quantum.modules.network.f5.bigip_ike_peer import ModuleManager
    from quantum.modules.network.f5.bigip_ike_peer import ArgumentSpec

    # Quantum 2.8 imports
    from units.compat import unittest
    from units.compat.mock import Mock

    from units.modules.utils import set_module_args


fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures')
fixture_data = {}


def load_fixture(name):
    path = os.path.join(fixture_path, name)

    if path in fixture_data:
        return fixture_data[path]

    with open(path) as f:
        data = f.read()

    try:
        data = json.loads(data)
    except Exception:
        pass

    fixture_data[path] = data
    return data


class TestParameters(unittest.TestCase):
    def test_module_parameters(self):
        args = dict(
            name='ike1',
        )
        p = ModuleParameters(params=args)
        assert p.name == 'ike1'

    def test_api_parameters(self):
        args = dict(
            name='ike1',
        )
        p = ApiParameters(params=args)
        assert p.name == 'ike1'


class TestUntypedManager(unittest.TestCase):

    def setUp(self):
        self.spec = ArgumentSpec()

    def test_create(self, *args):
        set_module_args(dict(
            name='ike1',
            version=['v1'],
            provider=dict(
                server='localhost',
                password='password',
                user='admin'
            )
        ))

        module = QuantumModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            required_if=self.spec.required_if,
            required_together=self.spec.required_together
        )

        # Override methods to force specific logic in the module to happen
        mm = ModuleManager(module=module)
        mm.create_on_device = Mock(return_value=True)
        mm.exists = Mock(return_value=False)

        results = mm.exec_module()

        assert results['changed'] is True
