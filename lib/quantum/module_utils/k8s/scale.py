#
#  Copyright 2018 Red Hat | Quantum
#
# This file is part of Quantum
#
# Quantum is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Quantum is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Quantum.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import, division, print_function

import copy
import math
import time

from quantum.module_utils.k8s.common import AUTH_ARG_SPEC, COMMON_ARG_SPEC
from quantum.module_utils.k8s.common import KubernetesQuantumModule
from quantum.module_utils.six import string_types

try:
    import yaml
    from openshift import watch
    from openshift.dynamic.client import ResourceInstance
    from openshift.helper.exceptions import KubernetesException
except ImportError as exc:
    class KubernetesException(Exception):
        pass


SCALE_ARG_SPEC = {
    'replicas': {'type': 'int', 'required': True},
    'current_replicas': {'type': 'int'},
    'resource_version': {},
    'wait': {'type': 'bool', 'default': True},
    'wait_timeout': {'type': 'int', 'default': 20},
}


class KubernetesQuantumScaleModule(KubernetesQuantumModule):

    def __init__(self, k8s_kind=None, *args, **kwargs):
        self.client = None
        self.warnings = []

        mutually_exclusive = [
            ('resource_definition', 'src'),
        ]

        KubernetesQuantumModule.__init__(self, *args,
                                         mutually_exclusive=mutually_exclusive,
                                         supports_check_mode=True,
                                         **kwargs)
        self.kind = k8s_kind or self.params.get('kind')
        self.api_version = self.params.get('api_version')
        self.name = self.params.get('name')
        self.namespace = self.params.get('namespace')
        resource_definition = self.params.get('resource_definition')

        if resource_definition:
            if isinstance(resource_definition, string_types):
                try:
                    self.resource_definitions = yaml.safe_load_all(resource_definition)
                except (IOError, yaml.YAMLError) as exc:
                    self.fail(msg="Error loading resource_definition: {0}".format(exc))
            elif isinstance(resource_definition, list):
                self.resource_definitions = resource_definition
            else:
                self.resource_definitions = [resource_definition]
        src = self.params.get('src')
        if src:
            self.resource_definitions = self.load_resource_definitions(src)

        if not resource_definition and not src:
            implicit_definition = dict(
                kind=self.kind,
                apiVersion=self.api_version,
                metadata=dict(name=self.name)
            )
            if self.namespace:
                implicit_definition['metadata']['namespace'] = self.namespace
            self.resource_definitions = [implicit_definition]

    def execute_module(self):
        definition = self.resource_definitions[0]

        self.client = self.get_api_client()

        name = definition['metadata']['name']
        namespace = definition['metadata'].get('namespace')
        api_version = definition['apiVersion']
        kind = definition['kind']
        current_replicas = self.params.get('current_replicas')
        replicas = self.params.get('replicas')
        resource_version = self.params.get('resource_version')

        wait = self.params.get('wait')
        wait_time = self.params.get('wait_timeout')
        existing = None
        existing_count = None
        return_attributes = dict(changed=False, result=dict())

        resource = self.find_resource(kind, api_version, fail=True)

        try:
            existing = resource.get(name=name, namespace=namespace)
            return_attributes['result'] = existing.to_dict()
        except KubernetesException as exc:
            self.fail_json(msg='Failed to retrieve requested object: {0}'.format(exc),
                           error=exc.value.get('status'))

        if self.kind == 'job':
            existing_count = existing.spec.parallelism
        elif hasattr(existing.spec, 'replicas'):
            existing_count = existing.spec.replicas

        if existing_count is None:
            self.fail_json(msg='Failed to retrieve the available count for the requested object.')

        if resource_version and resource_version != existing.metadata.resourceVersion:
            self.exit_json(**return_attributes)

        if current_replicas is not None and existing_count != current_replicas:
            self.exit_json(**return_attributes)

        if existing_count != replicas:
            return_attributes['changed'] = True
            if not self.check_mode:
                if self.kind == 'job':
                    existing.spec.parallelism = replicas
                    k8s_obj = resource.patch(existing.to_dict())
                else:
                    k8s_obj = self.scale(resource, existing, replicas, wait, wait_time)
                return_attributes['result'] = k8s_obj.to_dict()

        self.exit_json(**return_attributes)

    @property
    def argspec(self):
        args = copy.deepcopy(COMMON_ARG_SPEC)
        args.pop('state')
        args.pop('force')
        args.update(AUTH_ARG_SPEC)
        args.update(SCALE_ARG_SPEC)
        return args

    def scale(self, resource, existing_object, replicas, wait, wait_time):
        name = existing_object.metadata.name
        namespace = existing_object.metadata.namespace

        if not hasattr(resource, 'scale'):
            self.fail_json(
                msg="Cannot perform scale on resource of kind {0}".format(resource.kind)
            )

        scale_obj = {'metadata': {'name': name, 'namespace': namespace}, 'spec': {'replicas': replicas}}

        return_obj = None
        stream = None

        if wait:
            w, stream = self._create_stream(resource, namespace, wait_time)

        try:
            resource.scale.patch(body=scale_obj)
        except Exception as exc:
            self.fail_json(
                msg="Scale request failed: {0}".format(exc)
            )

        if wait and stream is not None:
            return_obj = self._read_stream(resource, w, stream, name, replicas)

        if not return_obj:
            return_obj = self._wait_for_response(resource, name, namespace)

        return return_obj

    def _create_stream(self, resource, namespace, wait_time):
        """ Create a stream of events for the object """
        w = None
        stream = None
        try:
            w = watch.Watch()
            w._api_client = self.client.client
            if namespace:
                stream = w.stream(resource.get, serialize=False, namespace=namespace, timeout_seconds=wait_time)
            else:
                stream = w.stream(resource.get, serialize=False, namespace=namespace, timeout_seconds=wait_time)
        except KubernetesException:
            pass
        return w, stream

    def _read_stream(self, resource, watcher, stream, name, replicas):
        """ Wait for ready_replicas to equal the requested number of replicas. """
        return_obj = None
        try:
            for event in stream:
                if event.get('object'):
                    obj = ResourceInstance(resource, event['object'])
                    if obj.metadata.name == name and hasattr(obj, 'status'):
                        if replicas == 0:
                            if not hasattr(obj.status, 'readyReplicas') or not obj.status.readyReplicas:
                                return_obj = obj
                                watcher.stop()
                                break
                        if hasattr(obj.status, 'readyReplicas') and obj.status.readyReplicas == replicas:
                            return_obj = obj
                            watcher.stop()
                            break
        except Exception as exc:
            self.fail_json(msg="Exception reading event stream: {0}".format(exc))

        if not return_obj:
            self.fail_json(msg="Error fetching the patched object. Try a higher wait_timeout value.")
        if replicas and return_obj.status.readyReplicas is None:
            self.fail_json(msg="Failed to fetch the number of ready replicas. Try a higher wait_timeout value.")
        if replicas and return_obj.status.readyReplicas != replicas:
            self.fail_json(msg="Number of ready replicas is {0}. Failed to reach {1} ready replicas within "
                               "the wait_timeout period.".format(return_obj.status.ready_replicas, replicas))
        return return_obj

    def _wait_for_response(self, resource, name, namespace):
        """ Wait for an API response """
        tries = 0
        half = math.ceil(20 / 2)
        obj = None

        while tries <= half:
            obj = resource.get(name=name, namespace=namespace)
            if obj:
                break
            tries += 2
            time.sleep(2)
        return obj
