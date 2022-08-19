"""Layout provider for Quantum source."""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os

from ... import types as t

from . import (
    ContentLayout,
    LayoutProvider,
)


class QuantumLayout(LayoutProvider):
    """Layout provider for Quantum source."""
    @staticmethod
    def is_content_root(path):  # type: (str) -> bool
        """Return True if the given path is a content root for this provider."""
        return os.path.exists(os.path.join(path, 'setup.py')) and os.path.exists(os.path.join(path, 'bin/quantum-test'))

    def create(self, root, paths):  # type: (str, t.List[str]) -> ContentLayout
        """Create a Layout using the given root and paths."""
        plugin_paths = dict((p, os.path.join('lib/quantum/plugins', p)) for p in self.PLUGIN_TYPES)

        plugin_paths.update(dict(
            modules='lib/quantum/modules',
            module_utils='lib/quantum/module_utils',
        ))

        return ContentLayout(root,
                             paths,
                             plugin_paths=plugin_paths,
                             collection=None,
                             test_path='test',
                             results_path='test/results',
                             sanity_path='test/sanity',
                             sanity_messages=None,
                             integration_path='test/integration',
                             integration_targets_path='test/integration/targets',
                             integration_vars_path='test/integration/integration_config.yml',
                             integration_messages=None,
                             unit_path='test/units',
                             unit_module_path='test/units/modules',
                             unit_module_utils_path='test/units/module_utils',
                             unit_messages=None,
                             )
