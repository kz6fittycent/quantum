"""Early initialization for quantum-test before most other imports have been performed."""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import resource

from .constants import (
    SOFT_RLIMIT_NOFILE,
)

CURRENT_RLIMIT_NOFILE = resource.getrlimit(resource.RLIMIT_NOFILE)
DESIRED_RLIMIT_NOFILE = (SOFT_RLIMIT_NOFILE, CURRENT_RLIMIT_NOFILE[1])

if DESIRED_RLIMIT_NOFILE < CURRENT_RLIMIT_NOFILE:
    resource.setrlimit(resource.RLIMIT_NOFILE, DESIRED_RLIMIT_NOFILE)
    CURRENT_RLIMIT_NOFILE = DESIRED_RLIMIT_NOFILE
