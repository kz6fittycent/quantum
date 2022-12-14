# -*- coding: utf-8 -*-

# This code is part of Quantum, but is an independent component

# This particular file snippet, and this file snippet only, is BSD licensed.
# Modules you write using this snippet, which is embedded dynamically by Quantum
# still belong to the author of the module, and may assign their own license
# to the complete work.

# Copyright: (c) 2018, Kevin Breit <kevin.breit@kevinbreit.net>
# All rights reserved.

# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import time
import os
import re
from quantum.module_utils.basic import QuantumModule, json, env_fallback
from quantum.module_utils.common.dict_transformations import camel_dict_to_snake_dict
from quantum.module_utils.urls import fetch_url
from quantum.module_utils.six.moves.urllib.parse import urlencode
from quantum.module_utils._text import to_native, to_bytes, to_text


RATE_LIMIT_RETRY_MULTIPLIER = 3
INTERNAL_ERROR_RETRY_MULTIPLIER = 3


def meraki_argument_spec():
    return dict(auth_key=dict(type='str', no_log=True, fallback=(env_fallback, ['MERAKI_KEY']), required=True),
                host=dict(type='str', default='api.meraki.com'),
                use_proxy=dict(type='bool', default=False),
                use_https=dict(type='bool', default=True),
                validate_certs=dict(type='bool', default=True),
                output_format=dict(type='str', choices=['camelcase', 'snakecase'], default='snakecase', fallback=(env_fallback, ['ANSIBLE_MERAKI_FORMAT'])),
                output_level=dict(type='str', default='normal', choices=['normal', 'debug']),
                timeout=dict(type='int', default=30),
                org_name=dict(type='str', aliases=['organization']),
                org_id=dict(type='str'),
                rate_limit_retry_time=dict(type='int', default=165),
                internal_error_retry_time=dict(type='int', default=60)
                )


class RateLimitException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class InternalErrorException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class HTTPError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


def _error_report(function):
    def inner(self, *args, **kwargs):
        while True:
            try:
                response = function(self, *args, **kwargs)
                if self.status == 429:
                    raise RateLimitException(
                        "Rate limiter hit, retry {0}".format(self.retry))
                elif self.status == 500:
                    raise InternalErrorException(
                        "Internal server error 500, retry {0}".format(self.retry))
                elif self.status == 502:
                    raise InternalErrorException(
                        "Internal server error 502, retry {0}".format(self.retry))
                elif self.status >= 400:
                    raise HTTPError("HTTP error {0} - {1}".format(self.status, response))
                self.retry = 0  # Needs to reset in case of future retries
                return response
            except RateLimitException as e:
                self.retry += 1
                if self.retry <= 10:
                    self.retry_time += self.retry * RATE_LIMIT_RETRY_MULTIPLIER
                    time.sleep(self.retry * RATE_LIMIT_RETRY_MULTIPLIER)
                else:
                    self.retry_time += 30
                    time.sleep(30)
                if self.retry_time > self.params['rate_limit_retry_time']:
                    raise RateLimitException(e)
            except InternalErrorException as e:
                self.retry += 1
                if self.retry <= 10:
                    self.retry_time += self.retry * INTERNAL_ERROR_RETRY_MULTIPLIER
                    time.sleep(self.retry * INTERNAL_ERROR_RETRY_MULTIPLIER)
                else:
                    self.retry_time += 9
                    time.sleep(9)
                if self.retry_time > self.params['internal_error_retry_time']:
                    raise InternalErrorException(e)
            except HTTPError as e:
                raise HTTPError(e)
    return inner


class MerakiModule(object):

    def __init__(self, module, function=None):
        self.module = module
        self.params = module.params
        self.result = dict(changed=False)
        self.headers = dict()
        self.function = function
        self.orgs = None
        self.nets = None
        self.org_id = None
        self.net_id = None
        self.check_mode = module.check_mode
        self.key_map = {}
        self.request_attempts = 0

        # normal output
        self.existing = None

        # info output
        self.config = dict()
        self.original = None
        self.proposed = dict()
        self.merged = None
        self.ignored_keys = ['id', 'organizationId']

        # debug output
        self.filter_string = ''
        self.method = None
        self.path = None
        self.response = None
        self.status = None
        self.url = None

        # rate limiting statistics
        self.retry = 0
        self.retry_time = 0

        # If URLs need to be modified or added for specific purposes, use .update() on the url_catalog dictionary
        self.get_urls = {'organizations': '/organizations',
                         'network': '/organizations/{org_id}/networks',
                         'admins': '/organizations/{org_id}/admins',
                         'configTemplates': '/organizations/{org_id}/configTemplates',
                         'samlymbols': '/organizations/{org_id}/samlRoles',
                         'ssids': '/networks/{net_id}/ssids',
                         'groupPolicies': '/networks/{net_id}/groupPolicies',
                         'staticRoutes': '/networks/{net_id}/staticRoutes',
                         'vlans': '/networks/{net_id}/vlans',
                         'devices': '/networks/{net_id}/devices',
                         }

        # Used to retrieve only one item
        self.get_one_urls = {'organizations': '/organizations/{org_id}',
                             'network': '/networks/{net_id}',
                             }

        # Module should add URLs which are required by the module
        self.url_catalog = {'get_all': self.get_urls,
                            'get_one': self.get_one_urls,
                            'create': None,
                            'update': None,
                            'delete': None,
                            'misc': None,
                            }

        if self.module._debug or self.params['output_level'] == 'debug':
            self.module.warn('Enable debug output because ANSIBLE_DEBUG was set or output_level is set to debug.')

        # TODO: This should be removed as org_name isn't always required
        self.module.required_if = [('state', 'present', ['org_name']),
                                   ('state', 'absent', ['org_name']),
                                   ]
        # self.module.mutually_exclusive = [('org_id', 'org_name'),
        #                                   ]
        self.modifiable_methods = ['POST', 'PUT', 'DELETE']

        self.headers = {'Content-Type': 'application/json',
                        'X-Cisco-Meraki-API-Key': module.params['auth_key'],
                        }

    def define_protocol(self):
        """Set protocol based on use_https parameters."""
        if self.params['use_https'] is True:
            self.params['protocol'] = 'https'
        else:
            self.params['protocol'] = 'http'

    def sanitize_keys(self, data):
        if isinstance(data, dict):
            items = {}
            for k, v in data.items():
                try:
                    new = {self.key_map[k]: data[k]}
                    items[self.key_map[k]] = self.sanitize_keys(data[k])
                except KeyError:
                    snake_k = re.sub('([a-z0-9])([A-Z])', r'\1_\2', k).lower()
                    new = {snake_k: data[k]}
                    items[snake_k] = self.sanitize_keys(data[k])
            return items
        elif isinstance(data, list):
            items = []
            for i in data:
                items.append(self.sanitize_keys(i))
            return items
        elif isinstance(data, int) or isinstance(data, str) or isinstance(data, float):
            return data

    def is_update_required(self, original, proposed, optional_ignore=None):
        ''' Compare two data-structures '''
        self.ignored_keys.append('net_id')
        if optional_ignore is not None:
            self.ignored_keys = self.ignored_keys + optional_ignore

        if type(original) != type(proposed):
            # self.fail_json(msg="Types don't match")
            return True
        if isinstance(original, list):
            if len(original) != len(proposed):
                # self.fail_json(msg="Length of lists don't match")
                return True
            for a, b in zip(original, proposed):
                if self.is_update_required(a, b):
                    # self.fail_json(msg="List doesn't match", a=a, b=b)
                    return True
        elif isinstance(original, dict):
            for k, v in proposed.items():
                if k not in self.ignored_keys:
                    if k in original:
                        if self.is_update_required(original[k], proposed[k]):
                            return True
                    else:
                        # self.fail_json(msg="Key not in original", k=k)
                        return True
        else:
            if original != proposed:
                # self.fail_json(msg="Fallback", original=original, proposed=proposed)
                return True
        return False

    def get_orgs(self):
        """Downloads all organizations for a user."""
        response = self.request('/organizations', method='GET')
        if self.status != 200:
            self.fail_json(msg='Organization lookup failed')
        self.orgs = response
        return self.orgs

    def is_org_valid(self, data, org_name=None, org_id=None):
        """Checks whether a specific org exists and is duplicated.

        If 0, doesn't exist. 1, exists and not duplicated. >1 duplicated.
        """
        org_count = 0
        if org_name is not None:
            for o in data:
                if o['name'] == org_name:
                    org_count += 1
        if org_id is not None:
            for o in data:
                if o['id'] == org_id:
                    org_count += 1
        return org_count

    def get_org_id(self, org_name):
        """Returns an organization id based on organization name, only if unique.

        If org_id is specified as parameter, return that instead of a lookup.
        """
        orgs = self.get_orgs()
        # self.fail_json(msg='ogs', orgs=orgs)
        if self.params['org_id'] is not None:
            if self.is_org_valid(orgs, org_id=self.params['org_id']) is True:
                return self.params['org_id']
        org_count = self.is_org_valid(orgs, org_name=org_name)
        if org_count == 0:
            self.fail_json(msg='There are no organizations with the name {org_name}'.format(org_name=org_name))
        if org_count > 1:
            self.fail_json(msg='There are multiple organizations with the name {org_name}'.format(org_name=org_name))
        elif org_count == 1:
            for i in orgs:
                if org_name == i['name']:
                    # self.fail_json(msg=i['id'])
                    return str(i['id'])

    def get_nets(self, org_name=None, org_id=None):
        """Downloads all networks in an organization."""
        if org_name:
            org_id = self.get_org_id(org_name)
        path = self.construct_path('get_all', org_id=org_id, function='network')
        r = self.request(path, method='GET')
        if self.status != 200:
            self.fail_json(msg='Network lookup failed')
        self.nets = r
        templates = self.get_config_templates(org_id)
        for t in templates:
            self.nets.append(t)
        return self.nets

    def get_net(self, org_name, net_name=None, org_id=None, data=None, net_id=None):
        ''' Return network information '''
        if not data:
            if not org_id:
                org_id = self.get_org_id(org_name)
            data = self.get_nets(org_id=org_id)
        for n in data:
            if net_id:
                if n['id'] == net_id:
                    return n
            elif net_name:
                if n['name'] == net_name:
                    return n
        return False

    def get_net_id(self, org_name=None, net_name=None, data=None):
        """Return network id from lookup or existing data."""
        if data is None:
            self.fail_json(msg='Must implement lookup')
        for n in data:
            if n['name'] == net_name:
                return n['id']
        self.fail_json(msg='No network found with the name {0}'.format(net_name))

    def get_config_templates(self, org_id):
        path = self.construct_path('get_all', function='configTemplates', org_id=org_id)
        response = self.request(path, 'GET')
        if self.status != 200:
            self.fail_json(msg='Unable to get configuration templates')
        return response

    def get_template_id(self, name, data):
        for template in data:
            if name == template['name']:
                return template['id']
        self.fail_json(msg='No configuration template named {0} found'.format(name))

    def convert_camel_to_snake(self, data):
        """
        Converts a dictionary or list to snake case from camel case
        :type data: dict or list
        :return: Converted data structure, if list or dict
        """

        if isinstance(data, dict):
            return camel_dict_to_snake_dict(data, ignore_list=('tags', 'tag'))
        elif isinstance(data, list):
            return [camel_dict_to_snake_dict(item, ignore_list=('tags', 'tag')) for item in data]
        else:
            return data

    def construct_params_list(self, keys, aliases=None):
        qs = {}
        for key in keys:
            if key in aliases:
                qs[aliases[key]] = self.module.params[key]
            else:
                qs[key] = self.module.params[key]
        return qs

    def encode_url_params(self, params):
        """Encodes key value pairs for URL"""
        return "?{0}".format(urlencode(params))

    def construct_path(self,
                       action,
                       function=None,
                       org_id=None,
                       net_id=None,
                       org_name=None,
                       custom=None,
                       params=None):
        """Build a path from the URL catalog.
        Uses function property from class for catalog lookup.
        """
        built_path = None
        if function is None:
            built_path = self.url_catalog[action][self.function]
        else:
            built_path = self.url_catalog[action][function]
        if org_name:
            org_id = self.get_org_id(org_name)
        if custom:
            built_path = built_path.format(org_id=org_id, net_id=net_id, **custom)
        else:
            built_path = built_path.format(org_id=org_id, net_id=net_id)
        if params:
            built_path += self.encode_url_params(params)
        return built_path

    @_error_report
    def request(self, path, method=None, payload=None):
        """Generic HTTP method for Meraki requests."""
        self.path = path
        self.define_protocol()

        if method is not None:
            self.method = method
        self.url = '{protocol}://{host}/api/v0/{path}'.format(path=self.path.lstrip('/'), **self.params)
        resp, info = fetch_url(self.module, self.url,
                               headers=self.headers,
                               data=payload,
                               method=self.method,
                               timeout=self.params['timeout'],
                               use_proxy=self.params['use_proxy'],
                               )
        self.response = info['msg']
        self.status = info['status']

        try:
            return json.loads(to_native(resp.read()))
        except Exception:
            pass

    def exit_json(self, **kwargs):
        """Custom written method to exit from module."""
        self.result['response'] = self.response
        self.result['status'] = self.status
        if self.retry > 0:
            self.module.warn("Rate limiter triggered - retry count {0}".format(self.retry))
        # Return the gory details when we need it
        if self.params['output_level'] == 'debug':
            self.result['method'] = self.method
            self.result['url'] = self.url
        self.result.update(**kwargs)
        if self.params['output_format'] == 'camelcase':
            self.module.deprecate("Update your couplings to support snake_case format instead of camelCase format.", version=2.13)
        else:
            if 'data' in self.result:
                try:
                    self.result['data'] = self.convert_camel_to_snake(self.result['data'])
                except (KeyError, AttributeError):
                    pass
        self.module.exit_json(**self.result)

    def fail_json(self, msg, **kwargs):
        """Custom written method to return info on failure."""
        self.result['response'] = self.response
        self.result['status'] = self.status

        if self.params['output_level'] == 'debug':
            if self.url is not None:
                self.result['method'] = self.method
                self.result['url'] = self.url

        self.result.update(**kwargs)
        self.module.fail_json(msg=msg, **self.result)
