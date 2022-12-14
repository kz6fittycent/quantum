# (c) 2019 Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = """
---
author: Quantum Security Automation Team
httpapi : qradar
short_description: HttpApi Plugin for IBM QRadar appliances
description:
  - This HttpApi plugin provides methods to connect to IBM QRadar
    appliances over a HTTP(S)-based api.
version_added: "2.8"
"""

import json

from quantum.module_utils.basic import to_text
from quantum.errors import QuantumConnectionFailure
from quantum.module_utils.six.moves.urllib.error import HTTPError
from quantum.plugins.httpapi import HttpApiBase
from quantum.module_utils.connection import ConnectionError

# Content Type and QRadar REST API Version
BASE_HEADERS = {
    'Content-Type': 'application/json;charset=UTF-8',
    'Version': '9.1',
}


class HttpApi(HttpApiBase):
    def logout(self):
        response, dummy = self.send_request('POST', '/api/auth/logout')

    def send_request(self, request_method, path, payload=None):
        data = json.dumps(payload) if payload else '{}'

        try:
            self._display_request(request_method)
            response, response_data = self.connection.send(path, payload, method=request_method, headers=BASE_HEADERS, force_basic_auth=True)
            value = self._get_response_value(response_data)

            return response.getcode(), self._response_to_json(value)
        except QuantumConnectionFailure as e:
            if to_text('401') in to_text(e):
                return 401, 'Authentication failure'
            else:
                return 404, 'Object not found'
        except HTTPError as e:
            error = json.loads(e.read())
            return e.code, error

    def _display_request(self, request_method):
        self.connection.queue_message('vvvv', 'Web Services: %s %s' % (request_method, self.connection._url))

    def _get_response_value(self, response_data):
        return to_text(response_data.getvalue())

    def _response_to_json(self, response_text):
        try:
            return json.loads(response_text) if response_text else {}
        # JSONDecodeError only available on Python 3.5+
        except ValueError:
            raise ConnectionError('Invalid JSON response: %s' % response_text)
