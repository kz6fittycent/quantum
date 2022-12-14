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
    from quantum.modules.network.fortios import fortios_system_wccp
except ImportError:
    pytest.skip("Could not load required modules for testing", allow_module_level=True)


@pytest.fixture(autouse=True)
def connection_mock(mocker):
    connection_class_mock = mocker.patch('quantum.modules.network.fortios.fortios_system_wccp.Connection')
    return connection_class_mock


fos_instance = FortiOSHandler(connection_mock)


def test_system_wccp_creation(mocker):
    schema_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.schema')

    set_method_result = {'status': 'success', 'http_method': 'POST', 'http_status': 200}
    set_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.set', return_value=set_method_result)

    input_data = {
        'username': 'admin',
        'state': 'present',
        'system_wccp': {
            'assignment_bucket_format': 'wccp-v2',
            'assignment_dstaddr_mask': 'test_value_4',
            'assignment_method': 'HASH',
            'assignment_srcaddr_mask': 'test_value_6',
            'assignment_weight': '7',
            'authentication': 'enable',
            'cache_engine_method': 'GRE',
            'cache_id': 'test_value_10',
            'forward_method': 'GRE',
            'group_address': 'test_value_12',
            'password': 'test_value_13',
            'ports': 'test_value_14',
            'ports_defined': 'source',
            'primary_hash': 'src-ip',
            'priority': '17',
            'protocol': '18',
            'return_method': 'GRE',
            'router_id': 'test_value_20',
            'router_list': 'test_value_21',
            'server_list': 'test_value_22',
            'server_type': 'forward',
            'service_id': 'test_value_24',
            'service_type': 'auto'
        },
        'vdom': 'root'}

    is_error, changed, response = fortios_system_wccp.fortios_system(input_data, fos_instance)

    expected_data = {
        'assignment-bucket-format': 'wccp-v2',
        'assignment-dstaddr-mask': 'test_value_4',
        'assignment-method': 'HASH',
        'assignment-srcaddr-mask': 'test_value_6',
        'assignment-weight': '7',
        'authentication': 'enable',
        'cache-engine-method': 'GRE',
        'cache-id': 'test_value_10',
        'forward-method': 'GRE',
        'group-address': 'test_value_12',
        'password': 'test_value_13',
        'ports': 'test_value_14',
        'ports-defined': 'source',
        'primary-hash': 'src-ip',
        'priority': '17',
        'protocol': '18',
        'return-method': 'GRE',
        'router-id': 'test_value_20',
        'router-list': 'test_value_21',
        'server-list': 'test_value_22',
        'server-type': 'forward',
        'service-id': 'test_value_24',
        'service-type': 'auto'
    }

    set_method_mock.assert_called_with('system', 'wccp', data=expected_data, vdom='root')
    schema_method_mock.assert_not_called()
    assert not is_error
    assert changed
    assert response['status'] == 'success'
    assert response['http_status'] == 200


def test_system_wccp_creation_fails(mocker):
    schema_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.schema')

    set_method_result = {'status': 'error', 'http_method': 'POST', 'http_status': 500}
    set_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.set', return_value=set_method_result)

    input_data = {
        'username': 'admin',
        'state': 'present',
        'system_wccp': {
            'assignment_bucket_format': 'wccp-v2',
            'assignment_dstaddr_mask': 'test_value_4',
            'assignment_method': 'HASH',
            'assignment_srcaddr_mask': 'test_value_6',
            'assignment_weight': '7',
            'authentication': 'enable',
            'cache_engine_method': 'GRE',
            'cache_id': 'test_value_10',
            'forward_method': 'GRE',
            'group_address': 'test_value_12',
            'password': 'test_value_13',
            'ports': 'test_value_14',
            'ports_defined': 'source',
            'primary_hash': 'src-ip',
            'priority': '17',
            'protocol': '18',
            'return_method': 'GRE',
            'router_id': 'test_value_20',
            'router_list': 'test_value_21',
            'server_list': 'test_value_22',
            'server_type': 'forward',
            'service_id': 'test_value_24',
            'service_type': 'auto'
        },
        'vdom': 'root'}

    is_error, changed, response = fortios_system_wccp.fortios_system(input_data, fos_instance)

    expected_data = {
        'assignment-bucket-format': 'wccp-v2',
        'assignment-dstaddr-mask': 'test_value_4',
        'assignment-method': 'HASH',
        'assignment-srcaddr-mask': 'test_value_6',
        'assignment-weight': '7',
        'authentication': 'enable',
        'cache-engine-method': 'GRE',
        'cache-id': 'test_value_10',
        'forward-method': 'GRE',
        'group-address': 'test_value_12',
        'password': 'test_value_13',
        'ports': 'test_value_14',
        'ports-defined': 'source',
        'primary-hash': 'src-ip',
        'priority': '17',
        'protocol': '18',
        'return-method': 'GRE',
        'router-id': 'test_value_20',
        'router-list': 'test_value_21',
        'server-list': 'test_value_22',
        'server-type': 'forward',
        'service-id': 'test_value_24',
        'service-type': 'auto'
    }

    set_method_mock.assert_called_with('system', 'wccp', data=expected_data, vdom='root')
    schema_method_mock.assert_not_called()
    assert is_error
    assert not changed
    assert response['status'] == 'error'
    assert response['http_status'] == 500


def test_system_wccp_removal(mocker):
    schema_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.schema')

    delete_method_result = {'status': 'success', 'http_method': 'POST', 'http_status': 200}
    delete_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.delete', return_value=delete_method_result)

    input_data = {
        'username': 'admin',
        'state': 'absent',
        'system_wccp': {
            'assignment_bucket_format': 'wccp-v2',
            'assignment_dstaddr_mask': 'test_value_4',
            'assignment_method': 'HASH',
            'assignment_srcaddr_mask': 'test_value_6',
            'assignment_weight': '7',
            'authentication': 'enable',
            'cache_engine_method': 'GRE',
            'cache_id': 'test_value_10',
            'forward_method': 'GRE',
            'group_address': 'test_value_12',
            'password': 'test_value_13',
            'ports': 'test_value_14',
            'ports_defined': 'source',
            'primary_hash': 'src-ip',
            'priority': '17',
            'protocol': '18',
            'return_method': 'GRE',
            'router_id': 'test_value_20',
            'router_list': 'test_value_21',
            'server_list': 'test_value_22',
            'server_type': 'forward',
            'service_id': 'test_value_24',
            'service_type': 'auto'
        },
        'vdom': 'root'}

    is_error, changed, response = fortios_system_wccp.fortios_system(input_data, fos_instance)

    delete_method_mock.assert_called_with('system', 'wccp', mkey=ANY, vdom='root')
    schema_method_mock.assert_not_called()
    assert not is_error
    assert changed
    assert response['status'] == 'success'
    assert response['http_status'] == 200


def test_system_wccp_deletion_fails(mocker):
    schema_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.schema')

    delete_method_result = {'status': 'error', 'http_method': 'POST', 'http_status': 500}
    delete_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.delete', return_value=delete_method_result)

    input_data = {
        'username': 'admin',
        'state': 'absent',
        'system_wccp': {
            'assignment_bucket_format': 'wccp-v2',
            'assignment_dstaddr_mask': 'test_value_4',
            'assignment_method': 'HASH',
            'assignment_srcaddr_mask': 'test_value_6',
            'assignment_weight': '7',
            'authentication': 'enable',
            'cache_engine_method': 'GRE',
            'cache_id': 'test_value_10',
            'forward_method': 'GRE',
            'group_address': 'test_value_12',
            'password': 'test_value_13',
            'ports': 'test_value_14',
            'ports_defined': 'source',
            'primary_hash': 'src-ip',
            'priority': '17',
            'protocol': '18',
            'return_method': 'GRE',
            'router_id': 'test_value_20',
            'router_list': 'test_value_21',
            'server_list': 'test_value_22',
            'server_type': 'forward',
            'service_id': 'test_value_24',
            'service_type': 'auto'
        },
        'vdom': 'root'}

    is_error, changed, response = fortios_system_wccp.fortios_system(input_data, fos_instance)

    delete_method_mock.assert_called_with('system', 'wccp', mkey=ANY, vdom='root')
    schema_method_mock.assert_not_called()
    assert is_error
    assert not changed
    assert response['status'] == 'error'
    assert response['http_status'] == 500


def test_system_wccp_idempotent(mocker):
    schema_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.schema')

    set_method_result = {'status': 'error', 'http_method': 'DELETE', 'http_status': 404}
    set_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.set', return_value=set_method_result)

    input_data = {
        'username': 'admin',
        'state': 'present',
        'system_wccp': {
            'assignment_bucket_format': 'wccp-v2',
            'assignment_dstaddr_mask': 'test_value_4',
            'assignment_method': 'HASH',
            'assignment_srcaddr_mask': 'test_value_6',
            'assignment_weight': '7',
            'authentication': 'enable',
            'cache_engine_method': 'GRE',
            'cache_id': 'test_value_10',
            'forward_method': 'GRE',
            'group_address': 'test_value_12',
            'password': 'test_value_13',
            'ports': 'test_value_14',
            'ports_defined': 'source',
            'primary_hash': 'src-ip',
            'priority': '17',
            'protocol': '18',
            'return_method': 'GRE',
            'router_id': 'test_value_20',
            'router_list': 'test_value_21',
            'server_list': 'test_value_22',
            'server_type': 'forward',
            'service_id': 'test_value_24',
            'service_type': 'auto'
        },
        'vdom': 'root'}

    is_error, changed, response = fortios_system_wccp.fortios_system(input_data, fos_instance)

    expected_data = {
        'assignment-bucket-format': 'wccp-v2',
        'assignment-dstaddr-mask': 'test_value_4',
        'assignment-method': 'HASH',
        'assignment-srcaddr-mask': 'test_value_6',
        'assignment-weight': '7',
        'authentication': 'enable',
        'cache-engine-method': 'GRE',
        'cache-id': 'test_value_10',
        'forward-method': 'GRE',
        'group-address': 'test_value_12',
        'password': 'test_value_13',
        'ports': 'test_value_14',
        'ports-defined': 'source',
        'primary-hash': 'src-ip',
        'priority': '17',
        'protocol': '18',
        'return-method': 'GRE',
        'router-id': 'test_value_20',
        'router-list': 'test_value_21',
        'server-list': 'test_value_22',
        'server-type': 'forward',
        'service-id': 'test_value_24',
        'service-type': 'auto'
    }

    set_method_mock.assert_called_with('system', 'wccp', data=expected_data, vdom='root')
    schema_method_mock.assert_not_called()
    assert not is_error
    assert not changed
    assert response['status'] == 'error'
    assert response['http_status'] == 404


def test_system_wccp_filter_foreign_attributes(mocker):
    schema_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.schema')

    set_method_result = {'status': 'success', 'http_method': 'POST', 'http_status': 200}
    set_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.set', return_value=set_method_result)

    input_data = {
        'username': 'admin',
        'state': 'present',
        'system_wccp': {
            'random_attribute_not_valid': 'tag',
            'assignment_bucket_format': 'wccp-v2',
            'assignment_dstaddr_mask': 'test_value_4',
            'assignment_method': 'HASH',
            'assignment_srcaddr_mask': 'test_value_6',
            'assignment_weight': '7',
            'authentication': 'enable',
            'cache_engine_method': 'GRE',
            'cache_id': 'test_value_10',
            'forward_method': 'GRE',
            'group_address': 'test_value_12',
            'password': 'test_value_13',
            'ports': 'test_value_14',
            'ports_defined': 'source',
            'primary_hash': 'src-ip',
            'priority': '17',
            'protocol': '18',
            'return_method': 'GRE',
            'router_id': 'test_value_20',
            'router_list': 'test_value_21',
            'server_list': 'test_value_22',
            'server_type': 'forward',
            'service_id': 'test_value_24',
            'service_type': 'auto'
        },
        'vdom': 'root'}

    is_error, changed, response = fortios_system_wccp.fortios_system(input_data, fos_instance)

    expected_data = {
        'assignment-bucket-format': 'wccp-v2',
        'assignment-dstaddr-mask': 'test_value_4',
        'assignment-method': 'HASH',
        'assignment-srcaddr-mask': 'test_value_6',
        'assignment-weight': '7',
        'authentication': 'enable',
        'cache-engine-method': 'GRE',
        'cache-id': 'test_value_10',
        'forward-method': 'GRE',
        'group-address': 'test_value_12',
        'password': 'test_value_13',
        'ports': 'test_value_14',
        'ports-defined': 'source',
        'primary-hash': 'src-ip',
        'priority': '17',
        'protocol': '18',
        'return-method': 'GRE',
        'router-id': 'test_value_20',
        'router-list': 'test_value_21',
        'server-list': 'test_value_22',
        'server-type': 'forward',
        'service-id': 'test_value_24',
        'service-type': 'auto'
    }

    set_method_mock.assert_called_with('system', 'wccp', data=expected_data, vdom='root')
    schema_method_mock.assert_not_called()
    assert not is_error
    assert changed
    assert response['status'] == 'success'
    assert response['http_status'] == 200
