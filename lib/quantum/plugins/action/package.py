# (c) 2015, Quantum Inc,
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
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from quantum.errors import QuantumAction, QuantumActionFail
from quantum.executor.module_common import get_action_args_with_defaults
from quantum.plugins.action import ActionBase
from quantum.utils.display import Display

display = Display()


class ActionModule(ActionBase):

    TRANSFERS_FILES = False

    def run(self, tmp=None, task_vars=None):
        ''' handler for package operations '''

        self._supports_check_mode = True
        self._supports_async = True

        result = super(ActionModule, self).run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

        module = self._task.args.get('use', 'auto')

        if module == 'auto':
            try:
                if self._task.delegate_to:  # if we delegate, we should use delegated host's facts
                    module = self._templar.template("{{hostvars['%s']['quantum_facts']['pkg_mgr']}}" % self._task.delegate_to)
                else:
                    module = self._templar.template('{{quantum_facts.pkg_mgr}}')
            except Exception:
                pass  # could not get it from template!

        try:
            if module == 'auto':
                facts = self._execute_module(module_name='setup', module_args=dict(filter='quantum_pkg_mgr', gather_subset='!all'), task_vars=task_vars)
                display.debug("Facts %s" % facts)
                module = facts.get('quantum_facts', {}).get('quantum_pkg_mgr', 'auto')

            if module != 'auto':

                if module not in self._shared_loader_obj.module_loader:
                    raise QuantumActionFail('Could not find a module for %s.' % module)
                else:
                    # run the 'package' module
                    new_module_args = self._task.args.copy()
                    if 'use' in new_module_args:
                        del new_module_args['use']

                    # get defaults for specific module
                    new_module_args = get_action_args_with_defaults(module, new_module_args, self._task.module_defaults, self._templar)

                    display.vvvv("Running %s" % module)
                    result.update(self._execute_module(module_name=module, module_args=new_module_args, task_vars=task_vars, wrap_async=self._task.async_val))
            else:
                raise QuantumActionFail('Could not detect which package manager to use. Try gathering facts or setting the "use" option.')

        except QuantumAction as e:
            result.update(e.result)
        finally:
            if not self._task.async_val:
                # remove a temporary path we created
                self._remove_tmp_path(self._connection._shell.tmpdir)

        return result
