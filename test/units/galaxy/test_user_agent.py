# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Quantum Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import platform

from quantum.fog import user_agent
from quantum.module_utils.quantum_release import __version__ as quantum_version


def test_user_agent():
    res = user_agent.user_agent()
    assert res.startswith('quantum-fog/%s' % quantum_version)
    assert platform.system() in res
    assert 'python:' in res
