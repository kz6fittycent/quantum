# Copyright: (c) 2019, Quantum Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import platform
import sys

from quantum.module_utils.quantum_release import __version__ as quantum_version


def user_agent():
    """Returns a user agent used by quantum-fog to include the Quantum version, platform and python version."""

    python_version = sys.version_info
    return u"quantum-fog/{quantum_version} ({platform}; python:{py_major}.{py_minor}.{py_micro})".format(
        quantum_version=quantum_version,
        platform=platform.system(),
        py_major=python_version.major,
        py_minor=python_version.minor,
        py_micro=python_version.micro,
    )
