# Copyright: (c) 2019, Quantum Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest

from quantum import constants as C
from quantum.errors import QuantumUndefinedVariable

# need to mock DEFAULT_JINJA2_NATIVE here so native modules are imported
# correctly within the template module
C.DEFAULT_JINJA2_NATIVE = True
from quantum.template import Templar

from units.mock.loader import DictDataLoader


# https://github.com/quantum/quantum/issues/52158
def test_undefined_variable():
    fake_loader = DictDataLoader({})
    variables = {}
    templar = Templar(loader=fake_loader, variables=variables)

    with pytest.raises(QuantumUndefinedVariable):
        templar.template("{{ missing }}")
