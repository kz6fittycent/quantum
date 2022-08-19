from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from quantum_collections.testns.testcoll.plugins.module_utils import secondary
import quantum_collections.testns.testcoll.plugins.module_utils.secondary


def thingtocall():
    if secondary != quantum_collections.testns.testcoll.plugins.module_utils.secondary:
        raise Exception()

    return "thingtocall in base called " + quantum_collections.testns.testcoll.plugins.module_utils.secondary.thingtocall()
