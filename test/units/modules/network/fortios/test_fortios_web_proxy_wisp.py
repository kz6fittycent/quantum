# Copyright 2019 Fortinet, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Quantum.  If not, see <https://www.gnu.org/licenses/>.

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import json
import pytest
from mock import ANY
from quantum.module_utils.network.fortios.fortios import FortiOSHandler

try:
    from quantum.modules.network.fortios import fortios_web_proxy_wisp
except ImportError:
    pytest.skip("Could not load required modules for testing", allow_module_level=True)


@pytest.fixture(autouse=True)
def connection_mock(mocker):
    connection_class_mock = mocker.patch('quantum.modules.network.fortios.fortios_web_proxy_wisp.Connection')
    return connection_class_mock


fos_instance = FortiOSHandler(connection_mock)


def test_web_proxy_wisp_creation(mocker):
    schema_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.schema')

    set_method_result = {'status': 'success', 'http_method': 'POST', 'http_status': 200}
    set_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.set', return_value=set_method_result)

    input_data = {
        'username': 'admin',
        'state': 'present',
        'web_proxy_wisp': {
            'comment': 'Comment.',
            'max_connections': '4',
            'name': 'default_name_5',
            'outgoing_ip': 'test_value_6',
            'server_ip': 'test_value_7',
            'server_port': '8',
            'timeout': '9'
        },
        'vdom': 'root'}

    is_error, changed, response = fortios_web_proxy_wisp.fortios_web_proxy(input_data, fos_instance)

    expected_data = {
        'comment': 'Comment.',
        'max-connections': '4',
        'name': 'default_name_5',
                'outgoing-ip': 'test_value_6',
                'server-ip': 'test_value_7',
                'server-port': '8',
                'timeout': '9'
    }

    set_method_mock.assert_called_with('web-proxy', 'wisp', data=expected_data, vdom='root')
    schema_method_mock.assert_not_called()
    assert not is_error
    assert changed
    assert response['status'] == 'success'
    assert response['http_status'] == 200


def test_web_proxy_wisp_creation_fails(mocker):
    schema_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.schema')

    set_method_result = {'status': 'error', 'http_method': 'POST', 'http_status': 500}
    set_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.set', return_value=set_method_result)

    input_data = {
        'username': 'admin',
        'state': 'present',
        'web_proxy_wisp': {
            'comment': 'Comment.',
            'max_connections': '4',
            'name': 'default_name_5',
            'outgoing_ip': 'test_value_6',
            'server_ip': 'test_value_7',
            'server_port': '8',
            'timeout': '9'
        },
        'vdom': 'root'}

    is_error, changed, response = fortios_web_proxy_wisp.fortios_web_proxy(input_data, fos_instance)

    expected_data = {
        'comment': 'Comment.',
        'max-connections': '4',
        'name': 'default_name_5',
                'outgoing-ip': 'test_value_6',
                'server-ip': 'test_value_7',
                'server-port': '8',
                'timeout': '9'
    }

    set_method_mock.assert_called_with('web-proxy', 'wisp', data=expected_data, vdom='root')
    schema_method_mock.assert_not_called()
    assert is_error
    assert not changed
    assert response['status'] == 'error'
    assert response['http_status'] == 500


def test_web_proxy_wisp_removal(mocker):
    schema_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.schema')

    delete_method_result = {'status': 'success', 'http_method': 'POST', 'http_status': 200}
    delete_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.delete', return_value=delete_method_result)

    input_data = {
        'username': 'admin',
        'state': 'absent',
        'web_proxy_wisp': {
            'comment': 'Comment.',
            'max_connections': '4',
            'name': 'default_name_5',
            'outgoing_ip': 'test_value_6',
            'server_ip': 'test_value_7',
            'server_port': '8',
            'timeout': '9'
        },
        'vdom': 'root'}

    is_error, changed, response = fortios_web_proxy_wisp.fortios_web_proxy(input_data, fos_instance)

    delete_method_mock.assert_called_with('web-proxy', 'wisp', mkey=ANY, vdom='root')
    schema_method_mock.assert_not_called()
    assert not is_error
    assert changed
    assert response['status'] == 'success'
    assert response['http_status'] == 200


def test_web_proxy_wisp_deletion_fails(mocker):
    schema_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.schema')

    delete_method_result = {'status': 'error', 'http_method': 'POST', 'http_status': 500}
    delete_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.delete', return_value=delete_method_result)

    input_data = {
        'username': 'admin',
        'state': 'absent',
        'web_proxy_wisp': {
            'comment': 'Comment.',
            'max_connections': '4',
            'name': 'default_name_5',
            'outgoing_ip': 'test_value_6',
            'server_ip': 'test_value_7',
            'server_port': '8',
            'timeout': '9'
        },
        'vdom': 'root'}

    is_error, changed, response = fortios_web_proxy_wisp.fortios_web_proxy(input_data, fos_instance)

    delete_method_mock.assert_called_with('web-proxy', 'wisp', mkey=ANY, vdom='root')
    schema_method_mock.assert_not_called()
    assert is_error
    assert not changed
    assert response['status'] == 'error'
    assert response['http_status'] == 500


def test_web_proxy_wisp_idempotent(mocker):
    schema_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.schema')

    set_method_result = {'status': 'error', 'http_method': 'DELETE', 'http_status': 404}
    set_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.set', return_value=set_method_result)

    input_data = {
        'username': 'admin',
        'state': 'present',
        'web_proxy_wisp': {
            'comment': 'Comment.',
            'max_connections': '4',
            'name': 'default_name_5',
            'outgoing_ip': 'test_value_6',
            'server_ip': 'test_value_7',
            'server_port': '8',
            'timeout': '9'
        },
        'vdom': 'root'}

    is_error, changed, response = fortios_web_proxy_wisp.fortios_web_proxy(input_data, fos_instance)

    expected_data = {
        'comment': 'Comment.',
        'max-connections': '4',
        'name': 'default_name_5',
                'outgoing-ip': 'test_value_6',
                'server-ip': 'test_value_7',
                'server-port': '8',
                'timeout': '9'
    }

    set_method_mock.assert_called_with('web-proxy', 'wisp', data=expected_data, vdom='root')
    schema_method_mock.assert_not_called()
    assert not is_error
    assert not changed
    assert response['status'] == 'error'
    assert response['http_status'] == 404


def test_web_proxy_wisp_filter_foreign_attributes(mocker):
    schema_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.schema')

    set_method_result = {'status': 'success', 'http_method': 'POST', 'http_status': 200}
    set_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.set', return_value=set_method_result)

    input_data = {
        'username': 'admin',
        'state': 'present',
        'web_proxy_wisp': {
            'random_attribute_not_valid': 'tag',
            'comment': 'Comment.',
            'max_connections': '4',
            'name': 'default_name_5',
            'outgoing_ip': 'test_value_6',
            'server_ip': 'test_value_7',
            'server_port': '8',
            'timeout': '9'
        },
        'vdom': 'root'}

    is_error, changed, response = fortios_web_proxy_wisp.fortios_web_proxy(input_data, fos_instance)

    expected_data = {
        'comment': 'Comment.',
        'max-connections': '4',
        'name': 'default_name_5',
                'outgoing-ip': 'test_value_6',
                'server-ip': 'test_value_7',
                'server-port': '8',
                'timeout': '9'
    }

    set_method_mock.assert_called_with('web-proxy', 'wisp', data=expected_data, vdom='root')
    schema_method_mock.assert_not_called()
    assert not is_error
    assert changed
    assert response['status'] == 'success'
    assert response['http_status'] == 200
