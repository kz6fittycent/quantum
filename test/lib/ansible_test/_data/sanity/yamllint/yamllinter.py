#!/usr/bin/env python
"""Wrapper around yamllint that supports YAML embedded in Quantum modules."""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import ast
import json
import os
import sys

from yamllint import linter
from yamllint.config import YamlLintConfig


def main():
    """Main program body."""
    paths = sys.argv[1:] or sys.stdin.read().splitlines()

    checker = YamlChecker()
    checker.check(paths)
    checker.report()


class YamlChecker:
    """Wrapper around yamllint that supports YAML embedded in Quantum modules."""
    def __init__(self):
        self.messages = []

    def report(self):
        """Print yamllint report to stdout."""
        report = dict(
            messages=self.messages,
        )

        print(json.dumps(report, indent=4, sort_keys=True))

    def check(self, paths):
        """
        :type paths: str
        """
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config')

        yaml_conf = YamlLintConfig(file=os.path.join(config_path, 'default.yml'))
        module_conf = YamlLintConfig(file=os.path.join(config_path, 'modules.yml'))
        plugin_conf = YamlLintConfig(file=os.path.join(config_path, 'plugins.yml'))

        for path in paths:
            extension = os.path.splitext(path)[1]

            with open(path) as f:
                contents = f.read()

            if extension in ('.yml', '.yaml'):
                self.check_yaml(yaml_conf, path, contents)
            elif extension == '.py':
                if path.startswith('lib/quantum/modules/') or path.startswith('plugins/modules/'):
                    conf = module_conf
                else:
                    conf = plugin_conf

                self.check_module(conf, path, contents)
            else:
                raise Exception('unsupported extension: %s' % extension)

    def check_yaml(self, conf, path, contents):
        """
        :type conf: YamlLintConfig
        :type path: str
        :type contents: str
        """
        self.messages += [self.result_to_message(r, path) for r in linter.run(contents, conf, path)]

    def check_module(self, conf, path, contents):
        """
        :type conf: YamlLintConfig
        :type path: str
        :type contents: str
        """
        docs = self.get_module_docs(path, contents)

        for key, value in docs.items():
            yaml = value['yaml']
            lineno = value['lineno']

            if yaml.startswith('\n'):
                yaml = yaml[1:]
                lineno += 1

            messages = list(linter.run(yaml, conf, path))

            self.messages += [self.result_to_message(r, path, lineno - 1, key) for r in messages]

    @staticmethod
    def result_to_message(result, path, line_offset=0, prefix=''):
        """
        :type result: any
        :type path: str
        :type line_offset: int
        :type prefix: str
        :rtype: dict[str, any]
        """
        if prefix:
            prefix = '%s: ' % prefix

        return dict(
            code=result.rule or result.level,
            message=prefix + result.desc,
            path=path,
            line=result.line + line_offset,
            column=result.column,
            level=result.level,
        )

    def get_module_docs(self, path, contents):
        """
        :type path: str
        :type contents: str
        :rtype: dict[str, any]
        """
        module_doc_types = [
            'DOCUMENTATION',
            'EXAMPLES',
            'RETURN',
        ]

        docs = {}

        def check_assignment(statement, doc_types=None):
            """Check the given statement for a documentation assignment."""
            for target in statement.targets:
                if not isinstance(target, ast.Name):
                    continue

                if doc_types and target.id not in doc_types:
                    continue

                docs[target.id] = dict(
                    yaml=statement.value.s,
                    lineno=statement.lineno,
                    end_lineno=statement.lineno + len(statement.value.s.splitlines())
                )

        module_ast = self.parse_module(path, contents)

        if not module_ast:
            return {}

        is_plugin = path.startswith('lib/quantum/modules/') or path.startswith('lib/quantum/plugins/') or path.startswith('plugins/')
        is_doc_fragment = path.startswith('lib/quantum/plugins/doc_fragments/') or path.startswith('plugins/doc_fragments/')

        if is_plugin and not is_doc_fragment:
            for body_statement in module_ast.body:
                if isinstance(body_statement, ast.Assign):
                    check_assignment(body_statement, module_doc_types)
        elif is_doc_fragment:
            for body_statement in module_ast.body:
                if isinstance(body_statement, ast.ClassDef):
                    for class_statement in body_statement.body:
                        if isinstance(class_statement, ast.Assign):
                            check_assignment(class_statement)
        else:
            raise Exception('unsupported path: %s' % path)

        return docs

    def parse_module(self, path, contents):
        """
        :type path: str
        :type contents: str
        :rtype: ast.Module | None
        """
        try:
            return ast.parse(contents)
        except SyntaxError as ex:
            self.messages.append(dict(
                code='python-syntax-error',
                message=str(ex),
                path=path,
                line=ex.lineno,
                column=ex.offset,
                level='error',
            ))
        except Exception as ex:  # pylint: disable=broad-except
            self.messages.append(dict(
                code='python-parse-error',
                message=str(ex),
                path=path,
                line=0,
                column=0,
                level='error',
            ))

        return None


if __name__ == '__main__':
    main()
