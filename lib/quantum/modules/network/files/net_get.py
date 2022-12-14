#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2018, Quantum by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'network'}


DOCUMENTATION = """
---
module: net_get
version_added: "2.6"
author: "Deepak Agrawal (@dagrawal)"
short_description: Copy a file from a network device to Quantum Controller
description:
  - This module provides functionality to copy file from network device to
    quantum controller.
extends_documentation_fragment: network_agnostic
options:
  src:
    description:
      - Specifies the source file. The path to the source file can either be
        the full path on the network device or a relative path as per path
        supported by destination network device.
    required: true
  protocol:
    description:
      - Protocol used to transfer file.
    default: scp
    choices: ['scp', 'sftp']
  dest:
    description:
      - Specifies the destination file. The path to the destination file can
        either be the full path on the Quantum control host or a relative
        path from the coupling or role root directory.
    default:
      - Same filename as specified in I(src). The path will be coupling root
        or role root directory if coupling is part of a role.

requirements:
    - "scp"

notes:
   - Some devices need specific configurations to be enabled before scp can work
     These configuration should be pre-configured before using this module
     e.g ios - C(ip scp server enable).
   - User privilege to do scp on network device should be pre-configured
     e.g. ios - need user privilege 15 by default for allowing scp.
   - Default destination of source file.
"""

EXAMPLES = """
- name: copy file from the network device to Quantum controller
  net_get:
    src: running_cfg_ios1.txt

- name: copy file from ios to common location at /tmp
  net_get:
    src: running_cfg_sw1.txt
    dest : /tmp/ios1.txt
"""

RETURN = """
"""
