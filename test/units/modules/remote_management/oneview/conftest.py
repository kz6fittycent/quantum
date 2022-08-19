# Copyright (c) 2016-2017 Hewlett Packard Enterprise Development LP
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import pytest

from mock import Mock, patch
from oneview_module_loader import ONEVIEW_MODULE_UTILS_PATH
from hpOneView.oneview_client import OneViewClient


@pytest.fixture
def mock_ov_client():
    patcher_json_file = patch.object(OneViewClient, 'from_json_file')
    client = patcher_json_file.start()
    return client.return_value


@pytest.fixture
def mock_quantum_module():
    patcher_quantum = patch(ONEVIEW_MODULE_UTILS_PATH + '.QuantumModule')
    patcher_quantum = patcher_quantum.start()
    quantum_module = Mock()
    patcher_quantum.return_value = quantum_module
    return quantum_module
