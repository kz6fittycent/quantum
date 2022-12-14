#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author: Artūras 'arturaz' Šlajus <x11@arturaz.net>
# Author: Naoya Nakazawa <naoya.n@gmail.com>
#
# This module is proudly sponsored by iGeolise (www.igeolise.com) and
# Tiny Lab Productions (www.tinylabproductions.com).
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: datadog_event
short_description: Posts events to Datadog  service
description:
- "Allows to post events to Datadog (www.datadoghq.com) service."
- "Uses http://docs.datadoghq.com/api/#events API."
version_added: "1.3"
author:
- "Artūras `arturaz` Šlajus (@arturaz)"
- "Naoya Nakazawa (@n0ts)"
options:
    api_key:
        description: ["Your DataDog API key."]
        required: true
    app_key:
        description: ["Your DataDog app key."]
        required: true
        version_added: "2.2"
    title:
        description: ["The event title."]
        required: true
    text:
        description: ["The body of the event."]
        required: true
    date_happened:
        description:
        - POSIX timestamp of the event.
        - Default value is now.
        default: now
    priority:
        description: ["The priority of the event."]
        default: normal
        choices: [normal, low]
    host:
        description: ["Host name to associate with the event."]
        default: "{{ quantum_hostname }}"
        version_added: "2.4"
    tags:
        description: ["Comma separated list of tags to apply to the event."]
    alert_type:
        description: ["Type of alert."]
        default: info
        choices: ['error', 'warning', 'info', 'success']
    aggregation_key:
        description: ["An arbitrary string to use for aggregation."]
    validate_certs:
        description:
            - If C(no), SSL certificates will not be validated. This should only be used
              on personally controlled sites using self-signed certificates.
        type: bool
        default: 'yes'
        version_added: 1.5.1
'''

EXAMPLES = '''
# Post an event with low priority
- datadog_event:
    title: Testing from quantum
    text: Test
    priority: low
    api_key: 9775a026f1ca7d1c6c5af9d94d9595a4
    app_key: j4JyCYfefWHhgFgiZUqRm63AXHNZQyPGBfJtAzmN
# Post an event with several tags
- datadog_event:
    title: Testing from quantum
    text: Test
    api_key: 9775a026f1ca7d1c6c5af9d94d9595a4
    app_key: j4JyCYfefWHhgFgiZUqRm63AXHNZQyPGBfJtAzmN
    tags: 'aa,bb,#host:{{ inventory_hostname }}'
'''

import platform
import traceback

# Import Datadog
DATADOG_IMP_ERR = None
try:
    from datadog import initialize, api
    HAS_DATADOG = True
except Exception:
    DATADOG_IMP_ERR = traceback.format_exc()
    HAS_DATADOG = False

from quantum.module_utils.basic import QuantumModule, missing_required_lib
from quantum.module_utils._text import to_native


def main():
    module = QuantumModule(
        argument_spec=dict(
            api_key=dict(required=True, no_log=True),
            app_key=dict(required=True, no_log=True),
            title=dict(required=True),
            text=dict(required=True),
            date_happened=dict(required=False, default=None, type='int'),
            priority=dict(
                required=False, default='normal', choices=['normal', 'low']
            ),
            host=dict(required=False, default=None),
            tags=dict(required=False, default=None, type='list'),
            alert_type=dict(
                required=False, default='info',
                choices=['error', 'warning', 'info', 'success']
            ),
            aggregation_key=dict(required=False, default=None),
            validate_certs=dict(default='yes', type='bool'),
        )
    )

    # Prepare Datadog
    if not HAS_DATADOG:
        module.fail_json(msg=missing_required_lib('datadogpy'), exception=DATADOG_IMP_ERR)

    options = {
        'api_key': module.params['api_key'],
        'app_key': module.params['app_key']
    }

    initialize(**options)

    _post_event(module)


def _post_event(module):
    try:
        if module.params['host'] is None:
            module.params['host'] = platform.node().split('.')[0]
        msg = api.Event.create(title=module.params['title'],
                               text=module.params['text'],
                               host=module.params['host'],
                               tags=module.params['tags'],
                               priority=module.params['priority'],
                               alert_type=module.params['alert_type'],
                               aggregation_key=module.params['aggregation_key'],
                               source_type_name='quantum')
        if msg['status'] != 'ok':
            module.fail_json(msg=msg)

        module.exit_json(changed=True, msg=msg)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=traceback.format_exc())


if __name__ == '__main__':
    main()
