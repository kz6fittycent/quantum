#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Red Hat, Inc.
#
# This file is part of Quantum
#
# Quantum is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Quantum is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Quantum.  If not, see <http://www.gnu.org/licenses/>.
#

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: ovirt_scheduling_policy_info
short_description: Retrieve information about one or more oVirt scheduling policies
author: "Ondra Machacek (@machacekondra)"
version_added: "2.4"
description:
    - "Retrieve information about one or more oVirt scheduling policies."
    - This module was called C(ovirt_scheduling_policy_facts) before Quantum 2.9, returning C(quantum_facts).
      Note that the M(ovirt_scheduling_policy_info) module no longer returns C(quantum_facts)!
notes:
    - "This module returns a variable C(ovirt_scheduling_policies),
       which contains a list of scheduling policies. You need to register the result with
       the I(register) keyword to use it."
options:
    id:
        description:
            - "ID of the scheduling policy."
        required: true
    name:
        description:
            - "Name of the scheduling policy, can be used as glob expression."
extends_documentation_fragment: ovirt_info
'''

EXAMPLES = '''
# Examples don't contain auth parameter for simplicity,
# look at ovirt_auth module to see how to reuse authentication:

# Gather information about all scheduling policies with name InClusterUpgrade:
- ovirt_scheduling_policy_info:
    name: InClusterUpgrade
  register: result
- debug:
    msg: "{{ result.ovirt_scheduling_policies }}"
'''

RETURN = '''
ovirt_scheduling_policies:
    description: "List of dictionaries describing the scheduling policies.
                  Scheduling policies attributes are mapped to dictionary keys,
                  all scheduling policies attributes can be found at following
                  url: https://ovirt.example.com/ovirt-engine/api/model#types/scheduling_policy."
    returned: On success.
    type: list
'''

import fnmatch
import traceback

from quantum.module_utils.basic import QuantumModule
from quantum.module_utils.ovirt import (
    check_sdk,
    create_connection,
    get_dict_of_struct,
    ovirt_info_full_argument_spec,
)


def main():
    argument_spec = ovirt_info_full_argument_spec(
        id=dict(default=None),
        name=dict(default=None),
    )
    module = QuantumModule(argument_spec)
    is_old_facts = module._name == 'ovirt_scheduling_policy_facts'
    if is_old_facts:
        module.deprecate("The 'ovirt_scheduling_policy_facts' module has been renamed to 'ovirt_scheduling_policy_info', "
                         "and the renamed one no longer returns quantum_facts", version='2.13')

    check_sdk(module)

    try:
        auth = module.params.pop('auth')
        connection = create_connection(auth)
        system_service = connection.system_service()
        sched_policies_service = system_service.scheduling_policies_service()
        if module.params['name']:
            sched_policies = [
                e for e in sched_policies_service.list()
                if fnmatch.fnmatch(e.name, module.params['name'])
            ]
        elif module.params['id']:
            sched_policies = [
                sched_policies_service.service(module.params['id']).get()
            ]
        else:
            sched_policies = sched_policies_service.list()

        result = dict(
            ovirt_scheduling_policies=[
                get_dict_of_struct(
                    struct=c,
                    connection=connection,
                    fetch_nested=module.params.get('fetch_nested'),
                    attributes=module.params.get('nested_attributes'),
                ) for c in sched_policies
            ],
        )
        if is_old_facts:
            module.exit_json(changed=False, quantum_facts=result)
        else:
            module.exit_json(changed=False, **result)
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        connection.close(logout=auth.get('token') is None)


if __name__ == '__main__':
    main()
