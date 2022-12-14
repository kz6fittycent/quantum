#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# (c) 2016, René Moser <mail@renemoser.net>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['deprecated'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: nginx_status_facts
deprecated:
  removed_in: '2.13'
  why: Deprecated in favour of C(_info) module.
  alternative: Use M(nginx_status_info) instead.
short_description: Retrieve nginx status facts.
description:
  - Gathers facts from nginx from an URL having C(stub_status) enabled.
version_added: "2.3"
author: "René Moser (@resmo)"
options:
  url:
    description:
      - URL of the nginx status.
    required: true
  timeout:
    description:
      - HTTP connection timeout in seconds.
    required: false
    default: 10

notes:
  - See http://nginx.org/en/docs/http/ngx_http_stub_status_module.html for more information.
'''

EXAMPLES = '''
# Gather status facts from nginx on localhost
- name: get current http stats
  nginx_status_facts:
    url: http://localhost/nginx_status

# Gather status facts from nginx on localhost with a custom timeout of 20 seconds
- name: get current http stats
  nginx_status_facts:
    url: http://localhost/nginx_status
    timeout: 20
'''

RETURN = '''
---
nginx_status_facts.active_connections:
  description: Active connections.
  returned: success
  type: int
  sample: 2340
nginx_status_facts.accepts:
  description: The total number of accepted client connections.
  returned: success
  type: int
  sample: 81769947
nginx_status_facts.handled:
  description: The total number of handled connections. Generally, the parameter value is the same as accepts unless some resource limits have been reached.
  returned: success
  type: int
  sample: 81769947
nginx_status_facts.requests:
  description: The total number of client requests.
  returned: success
  type: int
  sample: 144332345
nginx_status_facts.reading:
  description: The current number of connections where nginx is reading the request header.
  returned: success
  type: int
  sample: 0
nginx_status_facts.writing:
  description: The current number of connections where nginx is writing the response back to the client.
  returned: success
  type: int
  sample: 241
nginx_status_facts.waiting:
  description: The current number of idle client connections waiting for a request.
  returned: success
  type: int
  sample: 2092
nginx_status_facts.data:
  description: HTTP response as is.
  returned: success
  type: str
  sample: "Active connections: 2340 \nserver accepts handled requests\n 81769947 81769947 144332345 \nReading: 0 Writing: 241 Waiting: 2092 \n"
'''

import re
from quantum.module_utils.basic import QuantumModule
from quantum.module_utils.urls import fetch_url
from quantum.module_utils._text import to_text


class NginxStatusFacts(object):

    def __init__(self):
        self.url = module.params.get('url')
        self.timeout = module.params.get('timeout')

    def run(self):
        result = {
            'nginx_status_facts': {
                'active_connections': None,
                'accepts': None,
                'handled': None,
                'requests': None,
                'reading': None,
                'writing': None,
                'waiting': None,
                'data': None,
            }
        }
        (response, info) = fetch_url(module=module, url=self.url, force=True, timeout=self.timeout)
        if not response:
            module.fail_json(msg="No valid or no response from url %s within %s seconds (timeout)" % (self.url, self.timeout))

        data = to_text(response.read(), errors='surrogate_or_strict')
        if not data:
            return result

        result['nginx_status_facts']['data'] = data
        expr = r'Active connections: ([0-9]+) \nserver accepts handled requests\n ([0-9]+) ([0-9]+) ([0-9]+) \n' \
            r'Reading: ([0-9]+) Writing: ([0-9]+) Waiting: ([0-9]+)'
        match = re.match(expr, data, re.S)
        if match:
            result['nginx_status_facts']['active_connections'] = int(match.group(1))
            result['nginx_status_facts']['accepts'] = int(match.group(2))
            result['nginx_status_facts']['handled'] = int(match.group(3))
            result['nginx_status_facts']['requests'] = int(match.group(4))
            result['nginx_status_facts']['reading'] = int(match.group(5))
            result['nginx_status_facts']['writing'] = int(match.group(6))
            result['nginx_status_facts']['waiting'] = int(match.group(7))
        return result


def main():
    global module
    module = QuantumModule(
        argument_spec=dict(
            url=dict(required=True),
            timeout=dict(type='int', default=10),
        ),
        supports_check_mode=True,
    )

    nginx_status_facts = NginxStatusFacts().run()
    result = dict(changed=False, quantum_facts=nginx_status_facts)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
