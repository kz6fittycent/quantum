# (c) 2018, Matt Martz <matt@sivel.net>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from distutils.version import LooseVersion

import astroid

from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker
from pylint.checkers.utils import check_messages

from quantum.release import __version__ as quantum_version_raw

MSGS = {
    'E9501': ("Deprecated version (%r) found in call to Display.deprecated "
              "or QuantumModule.deprecate",
              "quantum-deprecated-version",
              "Used when a call to Display.deprecated specifies a version "
              "less than or equal to the current version of Quantum",
              {'minversion': (2, 6)}),
    'E9502': ("Display.deprecated call without a version",
              "quantum-deprecated-no-version",
              "Used when a call to Display.deprecated does not specify a "
              "version",
              {'minversion': (2, 6)}),
    'E9503': ("Invalid deprecated version (%r) found in call to "
              "Display.deprecated or QuantumModule.deprecate",
              "quantum-invalid-deprecated-version",
              "Used when a call to Display.deprecated specifies an invalid "
              "version number",
              {'minversion': (2, 6)}),
}


ANSIBLE_VERSION = LooseVersion('.'.join(quantum_version_raw.split('.')[:3]))


def _get_expr_name(node):
    """Funciton to get either ``attrname`` or ``name`` from ``node.func.expr``

    Created specifically for the case of ``display.deprecated`` or ``self._display.deprecated``
    """
    try:
        return node.func.expr.attrname
    except AttributeError:
        # If this fails too, we'll let it raise, the caller should catch it
        return node.func.expr.name


class QuantumDeprecatedChecker(BaseChecker):
    """Checks for Display.deprecated calls to ensure that the ``version``
    has not passed or met the time for removal
    """

    __implements__ = (IAstroidChecker,)
    name = 'deprecated'
    msgs = MSGS

    @check_messages(*(MSGS.keys()))
    def visit_call(self, node):
        version = None
        try:
            if (node.func.attrname == 'deprecated' and 'display' in _get_expr_name(node) or
                    node.func.attrname == 'deprecate' and 'module' in _get_expr_name(node)):
                if node.keywords:
                    for keyword in node.keywords:
                        if len(node.keywords) == 1 and keyword.arg is None:
                            # This is likely a **kwargs splat
                            return
                        if keyword.arg == 'version':
                            if isinstance(keyword.value.value, astroid.Name):
                                # This is likely a variable
                                return
                            version = keyword.value.value
                if not version:
                    try:
                        version = node.args[1].value
                    except IndexError:
                        self.add_message('quantum-deprecated-no-version', node=node)
                        return

                try:
                    if ANSIBLE_VERSION >= LooseVersion(str(version)):
                        self.add_message('quantum-deprecated-version', node=node, args=(version,))
                except ValueError:
                    self.add_message('quantum-invalid-deprecated-version', node=node, args=(version,))
                except TypeError:
                    # This happens if version starts with string components, and LooseVersion
                    # comparison tries to compare int with str. This can happen for tagged
                    # versions from Quantum 2.10.
                    pass
        except AttributeError:
            # Not the type of node we are interested in
            pass


def register(linter):
    """required method to auto register this checker """
    linter.register_checker(QuantumDeprecatedChecker(linter))
