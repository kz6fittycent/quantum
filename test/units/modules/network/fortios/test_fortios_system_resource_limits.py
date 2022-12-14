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
    from quantum.modules.network.fortios import fortios_system_resource_limits
except ImportError:
    pytest.skip("Could not load required modules for testing", allow_module_level=True)


@pytest.fixture(autouse=True)
def connection_mock(mocker):
    connection_class_mock = mocker.patch('quantum.modules.network.fortios.fortios_system_resource_limits.Connection')
    return connection_class_mock


fos_instance = FortiOSHandler(connection_mock)


def test_system_resource_limits_creation(mocker):
    schema_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.schema')

    set_method_result = {'status': 'success', 'http_method': 'POST', 'http_status': 200}
    set_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.set', return_value=set_method_result)

    input_data = {
        'username': 'admin',
        'state': 'present',
        'system_resource_limits': {
            'custom_service': '3',
            'dialup_tunnel': '4',
            'firewall_address': '5',
            'firewall_addrgrp': '6',
            'firewall_policy': '7',
            'ipsec_phase1': '8',
            'ipsec_phase1_interface': '9',
            'ipsec_phase2': '10',
            'ipsec_phase2_interface': '11',
            'log_disk_quota': '12',
            'onetime_schedule': '13',
            'proxy': '14',
            'recurring_schedule': '15',
            'service_group': '16',
            'session': '17',
            'sslvpn': '18',
            'user': '19',
            'user_group': '20'
        },
        'vdom': 'root'}

    is_error, changed, response = fortios_system_resource_limits.fortios_system(input_data, fos_instance)

    expected_data = {
        'custom-service': '3',
        'dialup-tunnel': '4',
        'firewall-address': '5',
        'firewall-addrgrp': '6',
        'firewall-policy': '7',
        'ipsec-phase1': '8',
        'ipsec-phase1-interface': '9',
        'ipsec-phase2': '10',
        'ipsec-phase2-interface': '11',
        'log-disk-quota': '12',
        'onetime-schedule': '13',
        'proxy': '14',
        'recurring-schedule': '15',
        'service-group': '16',
        'session': '17',
        'sslvpn': '18',
        'user': '19',
                'user-group': '20'
    }

    set_method_mock.assert_called_with('system', 'resource-limits', data=expected_data, vdom='root')
    schema_method_mock.assert_not_called()
    assert not is_error
    assert changed
    assert response['status'] == 'success'
    assert response['http_status'] == 200


def test_system_resource_limits_creation_fails(mocker):
    schema_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.schema')

    set_method_result = {'status': 'error', 'http_method': 'POST', 'http_status': 500}
    set_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.set', return_value=set_method_result)

    input_data = {
        'username': 'admin',
        'state': 'present',
        'system_resource_limits': {
            'custom_service': '3',
            'dialup_tunnel': '4',
            'firewall_address': '5',
            'firewall_addrgrp': '6',
            'firewall_policy': '7',
            'ipsec_phase1': '8',
            'ipsec_phase1_interface': '9',
            'ipsec_phase2': '10',
            'ipsec_phase2_interface': '11',
            'log_disk_quota': '12',
            'onetime_schedule': '13',
            'proxy': '14',
            'recurring_schedule': '15',
            'service_group': '16',
            'session': '17',
            'sslvpn': '18',
            'user': '19',
            'user_group': '20'
        },
        'vdom': 'root'}

    is_error, changed, response = fortios_system_resource_limits.fortios_system(input_data, fos_instance)

    expected_data = {
        'custom-service': '3',
        'dialup-tunnel': '4',
        'firewall-address': '5',
        'firewall-addrgrp': '6',
        'firewall-policy': '7',
        'ipsec-phase1': '8',
        'ipsec-phase1-interface': '9',
        'ipsec-phase2': '10',
        'ipsec-phase2-interface': '11',
        'log-disk-quota': '12',
        'onetime-schedule': '13',
        'proxy': '14',
        'recurring-schedule': '15',
        'service-group': '16',
        'session': '17',
        'sslvpn': '18',
        'user': '19',
                'user-group': '20'
    }

    set_method_mock.assert_called_with('system', 'resource-limits', data=expected_data, vdom='root')
    schema_method_mock.assert_not_called()
    assert is_error
    assert not changed
    assert response['status'] == 'error'
    assert response['http_status'] == 500


def test_system_resource_limits_idempotent(mocker):
    schema_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.schema')

    set_method_result = {'status': 'error', 'http_method': 'DELETE', 'http_status': 404}
    set_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.set', return_value=set_method_result)

    input_data = {
        'username': 'admin',
        'state': 'present',
        'system_resource_limits': {
            'custom_service': '3',
            'dialup_tunnel': '4',
            'firewall_address': '5',
            'firewall_addrgrp': '6',
            'firewall_policy': '7',
            'ipsec_phase1': '8',
            'ipsec_phase1_interface': '9',
            'ipsec_phase2': '10',
            'ipsec_phase2_interface': '11',
            'log_disk_quota': '12',
            'onetime_schedule': '13',
            'proxy': '14',
            'recurring_schedule': '15',
            'service_group': '16',
            'session': '17',
            'sslvpn': '18',
            'user': '19',
            'user_group': '20'
        },
        'vdom': 'root'}

    is_error, changed, response = fortios_system_resource_limits.fortios_system(input_data, fos_instance)

    expected_data = {
        'custom-service': '3',
        'dialup-tunnel': '4',
        'firewall-address': '5',
        'firewall-addrgrp': '6',
        'firewall-policy': '7',
        'ipsec-phase1': '8',
        'ipsec-phase1-interface': '9',
        'ipsec-phase2': '10',
        'ipsec-phase2-interface': '11',
        'log-disk-quota': '12',
        'onetime-schedule': '13',
        'proxy': '14',
        'recurring-schedule': '15',
        'service-group': '16',
        'session': '17',
        'sslvpn': '18',
        'user': '19',
                'user-group': '20'
    }

    set_method_mock.assert_called_with('system', 'resource-limits', data=expected_data, vdom='root')
    schema_method_mock.assert_not_called()
    assert not is_error
    assert not changed
    assert response['status'] == 'error'
    assert response['http_status'] == 404


def test_system_resource_limits_filter_foreign_attributes(mocker):
    schema_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.schema')

    set_method_result = {'status': 'success', 'http_method': 'POST', 'http_status': 200}
    set_method_mock = mocker.patch('quantum.module_utils.network.fortios.fortios.FortiOSHandler.set', return_value=set_method_result)

    input_data = {
        'username': 'admin',
        'state': 'present',
        'system_resource_limits': {
            'random_attribute_not_valid': 'tag',
            'custom_service': '3',
            'dialup_tunnel': '4',
            'firewall_address': '5',
            'firewall_addrgrp': '6',
            'firewall_policy': '7',
            'ipsec_phase1': '8',
            'ipsec_phase1_interface': '9',
            'ipsec_phase2': '10',
            'ipsec_phase2_interface': '11',
            'log_disk_quota': '12',
            'onetime_schedule': '13',
            'proxy': '14',
            'recurring_schedule': '15',
            'service_group': '16',
            'session': '17',
            'sslvpn': '18',
            'user': '19',
            'user_group': '20'
        },
        'vdom': 'root'}

    is_error, changed, response = fortios_system_resource_limits.fortios_system(input_data, fos_instance)

    expected_data = {
        'custom-service': '3',
        'dialup-tunnel': '4',
        'firewall-address': '5',
        'firewall-addrgrp': '6',
        'firewall-policy': '7',
        'ipsec-phase1': '8',
        'ipsec-phase1-interface': '9',
        'ipsec-phase2': '10',
        'ipsec-phase2-interface': '11',
        'log-disk-quota': '12',
        'onetime-schedule': '13',
        'proxy': '14',
        'recurring-schedule': '15',
        'service-group': '16',
        'session': '17',
        'sslvpn': '18',
        'user': '19',
                'user-group': '20'
    }

    set_method_mock.assert_called_with('system', 'resource-limits', data=expected_data, vdom='root')
    schema_method_mock.assert_not_called()
    assert not is_error
    assert changed
    assert response['status'] == 'success'
    assert response['http_status'] == 200
