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
    from quantum.modules.network.fortios import fortios_icap_profile
except ImportError:
    pytest.skip("Could not load required modules for testing", allow_module_level=True)


@pytest.fixture(autouse=True)
def connection_mock(mocker):
    connection_class_mock = mocker.patch('quantum.modules.network.fortios.fortios_icap_profile.Connection')
    return connection_class_mock


fos_instance = FortiOSHandler(connection_mock)


def test_icap_profile_creation(mocker):
    schema_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.schema')

    set_method_result = {'status': 'success', 'http_method': 'POST', 'http_status': 200}
    set_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.set', return_value=set_method_result)

    input_data = {
        'username': 'admin',
        'state': 'present',
        'icap_profile': {
            'methods': 'delete',
            'name': 'default_name_4',
            'replacemsg_group': 'test_value_5',
            'request': 'disable',
            'request_failure': 'error',
            'request_path': 'test_value_8',
            'request_server': 'test_value_9',
            'response': 'disable',
            'response_failure': 'error',
            'response_path': 'test_value_12',
            'response_server': 'test_value_13',
            'streaming_content_bypass': 'disable'
        },
        'vdom': 'root'}

    is_error, changed, response = fortios_icap_profile.fortios_icap(input_data, fos_instance)

    expected_data = {
        'methods': 'delete',
        'name': 'default_name_4',
                'replacemsg-group': 'test_value_5',
                'request': 'disable',
                'request-failure': 'error',
                'request-path': 'test_value_8',
                'request-server': 'test_value_9',
                'response': 'disable',
                'response-failure': 'error',
                'response-path': 'test_value_12',
                'response-server': 'test_value_13',
                'streaming-content-bypass': 'disable'
    }

    set_method_mock.assert_called_with('icap', 'profile', data=expected_data, vdom='root')
    schema_method_mock.assert_not_called()
    assert not is_error
    assert changed
    assert response['status'] == 'success'
    assert response['http_status'] == 200


def test_icap_profile_creation_fails(mocker):
    schema_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.schema')

    set_method_result = {'status': 'error', 'http_method': 'POST', 'http_status': 500}
    set_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.set', return_value=set_method_result)

    input_data = {
        'username': 'admin',
        'state': 'present',
        'icap_profile': {
            'methods': 'delete',
            'name': 'default_name_4',
            'replacemsg_group': 'test_value_5',
            'request': 'disable',
            'request_failure': 'error',
            'request_path': 'test_value_8',
            'request_server': 'test_value_9',
            'response': 'disable',
            'response_failure': 'error',
            'response_path': 'test_value_12',
            'response_server': 'test_value_13',
            'streaming_content_bypass': 'disable'
        },
        'vdom': 'root'}

    is_error, changed, response = fortios_icap_profile.fortios_icap(input_data, fos_instance)

    expected_data = {
        'methods': 'delete',
        'name': 'default_name_4',
                'replacemsg-group': 'test_value_5',
                'request': 'disable',
                'request-failure': 'error',
                'request-path': 'test_value_8',
                'request-server': 'test_value_9',
                'response': 'disable',
                'response-failure': 'error',
                'response-path': 'test_value_12',
                'response-server': 'test_value_13',
                'streaming-content-bypass': 'disable'
    }

    set_method_mock.assert_called_with('icap', 'profile', data=expected_data, vdom='root')
    schema_method_mock.assert_not_called()
    assert is_error
    assert not changed
    assert response['status'] == 'error'
    assert response['http_status'] == 500


def test_icap_profile_removal(mocker):
    schema_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.schema')

    delete_method_result = {'status': 'success', 'http_method': 'POST', 'http_status': 200}
    delete_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.delete', return_value=delete_method_result)

    input_data = {
        'username': 'admin',
        'state': 'absent',
        'icap_profile': {
            'methods': 'delete',
            'name': 'default_name_4',
            'replacemsg_group': 'test_value_5',
            'request': 'disable',
            'request_failure': 'error',
            'request_path': 'test_value_8',
            'request_server': 'test_value_9',
            'response': 'disable',
            'response_failure': 'error',
            'response_path': 'test_value_12',
            'response_server': 'test_value_13',
            'streaming_content_bypass': 'disable'
        },
        'vdom': 'root'}

    is_error, changed, response = fortios_icap_profile.fortios_icap(input_data, fos_instance)

    delete_method_mock.assert_called_with('icap', 'profile', mkey=ANY, vdom='root')
    schema_method_mock.assert_not_called()
    assert not is_error
    assert changed
    assert response['status'] == 'success'
    assert response['http_status'] == 200


def test_icap_profile_deletion_fails(mocker):
    schema_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.schema')

    delete_method_result = {'status': 'error', 'http_method': 'POST', 'http_status': 500}
    delete_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.delete', return_value=delete_method_result)

    input_data = {
        'username': 'admin',
        'state': 'absent',
        'icap_profile': {
            'methods': 'delete',
            'name': 'default_name_4',
            'replacemsg_group': 'test_value_5',
            'request': 'disable',
            'request_failure': 'error',
            'request_path': 'test_value_8',
            'request_server': 'test_value_9',
            'response': 'disable',
            'response_failure': 'error',
            'response_path': 'test_value_12',
            'response_server': 'test_value_13',
            'streaming_content_bypass': 'disable'
        },
        'vdom': 'root'}

    is_error, changed, response = fortios_icap_profile.fortios_icap(input_data, fos_instance)

    delete_method_mock.assert_called_with('icap', 'profile', mkey=ANY, vdom='root')
    schema_method_mock.assert_not_called()
    assert is_error
    assert not changed
    assert response['status'] == 'error'
    assert response['http_status'] == 500


def test_icap_profile_idempotent(mocker):
    schema_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.schema')

    set_method_result = {'status': 'error', 'http_method': 'DELETE', 'http_status': 404}
    set_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.set', return_value=set_method_result)

    input_data = {
        'username': 'admin',
        'state': 'present',
        'icap_profile': {
            'methods': 'delete',
            'name': 'default_name_4',
            'replacemsg_group': 'test_value_5',
            'request': 'disable',
            'request_failure': 'error',
            'request_path': 'test_value_8',
            'request_server': 'test_value_9',
            'response': 'disable',
            'response_failure': 'error',
            'response_path': 'test_value_12',
            'response_server': 'test_value_13',
            'streaming_content_bypass': 'disable'
        },
        'vdom': 'root'}

    is_error, changed, response = fortios_icap_profile.fortios_icap(input_data, fos_instance)

    expected_data = {
        'methods': 'delete',
        'name': 'default_name_4',
                'replacemsg-group': 'test_value_5',
                'request': 'disable',
                'request-failure': 'error',
                'request-path': 'test_value_8',
                'request-server': 'test_value_9',
                'response': 'disable',
                'response-failure': 'error',
                'response-path': 'test_value_12',
                'response-server': 'test_value_13',
                'streaming-content-bypass': 'disable'
    }

    set_method_mock.assert_called_with('icap', 'profile', data=expected_data, vdom='root')
    schema_method_mock.assert_not_called()
    assert not is_error
    assert not changed
    assert response['status'] == 'error'
    assert response['http_status'] == 404


def test_icap_profile_filter_foreign_attributes(mocker):
    schema_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.schema')

    set_method_result = {'status': 'success', 'http_method': 'POST', 'http_status': 200}
    set_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.set', return_value=set_method_result)

    input_data = {
        'username': 'admin',
        'state': 'present',
        'icap_profile': {
            'random_attribute_not_valid': 'tag',
            'methods': 'delete',
            'name': 'default_name_4',
            'replacemsg_group': 'test_value_5',
            'request': 'disable',
            'request_failure': 'error',
            'request_path': 'test_value_8',
            'request_server': 'test_value_9',
            'response': 'disable',
            'response_failure': 'error',
            'response_path': 'test_value_12',
            'response_server': 'test_value_13',
            'streaming_content_bypass': 'disable'
        },
        'vdom': 'root'}

    is_error, changed, response = fortios_icap_profile.fortios_icap(input_data, fos_instance)

    expected_data = {
        'methods': 'delete',
        'name': 'default_name_4',
                'replacemsg-group': 'test_value_5',
                'request': 'disable',
                'request-failure': 'error',
                'request-path': 'test_value_8',
                'request-server': 'test_value_9',
                'response': 'disable',
                'response-failure': 'error',
                'response-path': 'test_value_12',
                'response-server': 'test_value_13',
                'streaming-content-bypass': 'disable'
    }

    set_method_mock.assert_called_with('icap', 'profile', data=expected_data, vdom='root')
    schema_method_mock.assert_not_called()
    assert not is_error
    assert changed
    assert response['status'] == 'success'
    assert response['http_status'] == 200
