# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Quantum Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import sys

import pytest

from quantum import constants as C
from quantum.cli.arguments import option_helpers as opt_help
from quantum import __path__ as quantum_path
from quantum.release import __version__ as quantum_version

if C.DEFAULT_MODULE_PATH is None:
    cpath = u'Default w/o overrides'
else:
    cpath = C.DEFAULT_MODULE_PATH

FAKE_PROG = u'quantum-cli-test'
VERSION_OUTPUT = opt_help.version(prog=FAKE_PROG)


@pytest.mark.parametrize(
    'must_have', [
        FAKE_PROG + u' %s' % quantum_version,
        u'config file = %s' % C.CONFIG_FILE,
        u'configured module search path = %s' % cpath,
        u'quantum python module location = %s' % ':'.join(quantum_path),
        u'executable location = ',
        u'python version = %s' % ''.join(sys.version.splitlines()),
    ]
)
def test_option_helper_version(must_have):
    assert must_have in VERSION_OUTPUT
