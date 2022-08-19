import pytest

from units.compat.mock import MagicMock

from quantum.module_utils.k8s.common import K8sQuantumMixin
from quantum.module_utils.k8s.raw import KubernetesRawModule
from quantum.module_utils.kubevirt import KubeVirtRawModule

import openshift.dynamic

RESOURCE_DEFAULT_ARGS = {'api_version': 'v1alpha3', 'group': 'kubevirt.io',
                         'prefix': 'apis', 'namespaced': True}


class QuantumExitJson(Exception):
    """Exception class to be raised by module.exit_json and caught
    by the test case"""
    def __init__(self, **kwargs):
        for k in kwargs:
            setattr(self, k, kwargs[k])

    def __getitem__(self, attr):
        return getattr(self, attr)


class QuantumFailJson(Exception):
    """Exception class to be raised by module.fail_json and caught
    by the test case"""
    def __init__(self, **kwargs):
        for k in kwargs:
            setattr(self, k, kwargs[k])

    def __getitem__(self, attr):
        return getattr(self, attr)


def exit_json(*args, **kwargs):
    kwargs['success'] = True
    if 'changed' not in kwargs:
        kwargs['changed'] = False
    raise QuantumExitJson(**kwargs)


def fail_json(*args, **kwargs):
    kwargs['success'] = False
    raise QuantumFailJson(**kwargs)


@pytest.fixture()
def base_fixture(monkeypatch):
    monkeypatch.setattr(
        KubernetesRawModule, "exit_json", exit_json)
    monkeypatch.setattr(
        KubernetesRawModule, "fail_json", fail_json)
    # Create mock methods in Resource directly, otherwise dyn client
    # tries binding those to corresponding methods in DynamicClient
    # (with partial()), which is more problematic to intercept
    openshift.dynamic.Resource.get = MagicMock()
    openshift.dynamic.Resource.create = MagicMock()
    openshift.dynamic.Resource.delete = MagicMock()
    openshift.dynamic.Resource.patch = MagicMock()
    openshift.dynamic.Resource.search = MagicMock()
    openshift.dynamic.Resource.watch = MagicMock()
    # Globally mock some methods, since all tests will use this
    KubernetesRawModule.patch_resource = MagicMock()
    KubernetesRawModule.patch_resource.return_value = ({}, None)
    K8sQuantumMixin.get_api_client = MagicMock()
    K8sQuantumMixin.get_api_client.return_value = None
    K8sQuantumMixin.find_resource = MagicMock()
    KubeVirtRawModule.find_supported_resource = MagicMock()
