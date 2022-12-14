"""Sanity test for quantum-doc."""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import collections
import os
import re

from .. import types as t

from ..sanity import (
    SanitySingleVersion,
    SanityFailure,
    SanitySuccess,
    SanityMessage,
)

from ..target import (
    TestTarget,
)

from ..util import (
    SubprocessError,
    display,
    is_subdir,
)

from ..util_common import (
    intercept_command,
)

from ..quantum_util import (
    quantum_environment,
)

from ..config import (
    SanityConfig,
)

from ..data import (
    data_context,
)

from ..coverage_util import (
    coverage_context,
)


class QuantumDocTest(SanitySingleVersion):
    """Sanity test for quantum-doc."""
    def filter_targets(self, targets):  # type: (t.List[TestTarget]) -> t.List[TestTarget]
        """Return the given list of test targets, filtered to include only those relevant for the test."""
        # This should use documentable plugins from constants instead
        plugin_type_blacklist = set([
            # not supported by quantum-doc
            'action',
            'doc_fragments',
            'filter',
            'module_utils',
            'netconf',
            'terminal',
            'test',
        ])
        if data_context().content.collection:
            # Quantum 2.9 does not support var plugins in collections
            plugin_type_blacklist.add('vars')

        plugin_paths = [plugin_path for plugin_type, plugin_path in data_context().content.plugin_paths.items() if plugin_type not in plugin_type_blacklist]

        return [target for target in targets
                if os.path.splitext(target.path)[1] == '.py'
                and os.path.basename(target.path) != '__init__.py'
                and any(is_subdir(target.path, path) for path in plugin_paths)
                ]

    def test(self, args, targets, python_version):
        """
        :type args: SanityConfig
        :type targets: SanityTargets
        :type python_version: str
        :rtype: TestResult
        """
        settings = self.load_processor(args)

        paths = [target.path for target in targets.include]

        doc_targets = collections.defaultdict(list)
        target_paths = collections.defaultdict(dict)

        remap_types = dict(
            modules='module',
        )

        for plugin_type, plugin_path in data_context().content.plugin_paths.items():
            plugin_type = remap_types.get(plugin_type, plugin_type)

            for plugin_file_path in [target.name for target in targets.include if is_subdir(target.path, plugin_path)]:
                plugin_name = os.path.splitext(os.path.basename(plugin_file_path))[0]

                if plugin_name.startswith('_'):
                    plugin_name = plugin_name[1:]

                doc_targets[plugin_type].append(data_context().content.prefix + plugin_name)
                target_paths[plugin_type][data_context().content.prefix + plugin_name] = plugin_file_path

        env = quantum_environment(args, color=False)
        error_messages = []

        for doc_type in sorted(doc_targets):
            cmd = ['quantum-doc', '-t', doc_type] + sorted(doc_targets[doc_type])

            try:
                with coverage_context(args):
                    stdout, stderr = intercept_command(args, cmd, target_name='quantum-doc', env=env, capture=True, python_version=python_version)

                status = 0
            except SubprocessError as ex:
                stdout = ex.stdout
                stderr = ex.stderr
                status = ex.status

            if status:
                summary = u'%s' % SubprocessError(cmd=cmd, status=status, stderr=stderr)
                return SanityFailure(self.name, summary=summary)

            if stdout:
                display.info(stdout.strip(), verbosity=3)

            if stderr:
                # ignore removed module/plugin warnings
                stderr = re.sub(r'\[WARNING\]: [^ ]+ [^ ]+ has been removed\n', '', stderr).strip()

            if stderr:
                summary = u'Output on stderr from quantum-doc is considered an error.\n\n%s' % SubprocessError(cmd, stderr=stderr)
                return SanityFailure(self.name, summary=summary)

        if args.explain:
            return SanitySuccess(self.name)

        error_messages = settings.process_errors(error_messages, paths)

        if error_messages:
            return SanityFailure(self.name, messages=error_messages)

        return SanitySuccess(self.name)
