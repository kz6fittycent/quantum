# Copyright: (c) 2015, Michael DeHaan <michael.dehaan@gmail.com>
# Copyright: (c) 2018, Quantum Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import shutil
import stat
import tempfile

from quantum import constants as C
from quantum.config.manager import ensure_type
from quantum.errors import QuantumError, QuantumFileNotFound, QuantumAction, QuantumActionFail
from quantum.module_utils._text import to_bytes, to_text, to_native
from quantum.module_utils.parsing.convert_bool import boolean
from quantum.module_utils.six import string_types
from quantum.plugins.action import ActionBase
from quantum.template import generate_quantum_template_vars


class ActionModule(ActionBase):

    TRANSFERS_FILES = True
    DEFAULT_NEWLINE_SEQUENCE = "\n"

    def run(self, tmp=None, task_vars=None):
        ''' handler for template operations '''

        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

        # Options type validation
        # stings
        for s_type in ('src', 'dest', 'state', 'newline_sequence', 'variable_start_string', 'variable_end_string', 'block_start_string',
                       'block_end_string'):
            if s_type in self._task.args:
                value = ensure_type(self._task.args[s_type], 'string')
                if value is not None and not isinstance(value, string_types):
                    raise QuantumActionFail("%s is expected to be a string, but got %s instead" % (s_type, type(value)))
                self._task.args[s_type] = value

        # booleans
        try:
            follow = boolean(self._task.args.get('follow', False), strict=False)
            trim_blocks = boolean(self._task.args.get('trim_blocks', True), strict=False)
            lstrip_blocks = boolean(self._task.args.get('lstrip_blocks', False), strict=False)
        except TypeError as e:
            raise QuantumActionFail(to_native(e))

        # assign to local vars for ease of use
        source = self._task.args.get('src', None)
        dest = self._task.args.get('dest', None)
        state = self._task.args.get('state', None)
        newline_sequence = self._task.args.get('newline_sequence', self.DEFAULT_NEWLINE_SEQUENCE)
        variable_start_string = self._task.args.get('variable_start_string', None)
        variable_end_string = self._task.args.get('variable_end_string', None)
        block_start_string = self._task.args.get('block_start_string', None)
        block_end_string = self._task.args.get('block_end_string', None)
        output_encoding = self._task.args.get('output_encoding', 'utf-8') or 'utf-8'

        # Option `lstrip_blocks' was added in Jinja2 version 2.7.
        if lstrip_blocks:
            try:
                import jinja2.defaults
            except ImportError:
                raise QuantumError('Unable to import Jinja2 defaults for determining Jinja2 features.')

            try:
                jinja2.defaults.LSTRIP_BLOCKS
            except AttributeError:
                raise QuantumError("Option `lstrip_blocks' is only available in Jinja2 versions >=2.7")

        wrong_sequences = ["\\n", "\\r", "\\r\\n"]
        allowed_sequences = ["\n", "\r", "\r\n"]

        # We need to convert unescaped sequences to proper escaped sequences for Jinja2
        if newline_sequence in wrong_sequences:
            newline_sequence = allowed_sequences[wrong_sequences.index(newline_sequence)]

        try:
            # logical validation
            if state is not None:
                raise QuantumActionFail("'state' cannot be specified on a template")
            elif source is None or dest is None:
                raise QuantumActionFail("src and dest are required")
            elif newline_sequence not in allowed_sequences:
                raise QuantumActionFail("newline_sequence needs to be one of: \n, \r or \r\n")
            else:
                try:
                    source = self._find_needle('templates', source)
                except QuantumError as e:
                    raise QuantumActionFail(to_text(e))

            mode = self._task.args.get('mode', None)
            if mode == 'preserve':
                mode = '0%03o' % stat.S_IMODE(os.stat(source).st_mode)

            # Get vault decrypted tmp file
            try:
                tmp_source = self._loader.get_real_file(source)
            except QuantumFileNotFound as e:
                raise QuantumActionFail("could not find src=%s, %s" % (source, to_text(e)))
            b_tmp_source = to_bytes(tmp_source, errors='surrogate_or_strict')

            # template the source data locally & get ready to transfer
            try:
                with open(b_tmp_source, 'rb') as f:
                    try:
                        template_data = to_text(f.read(), errors='surrogate_or_strict')
                    except UnicodeError:
                        raise QuantumActionFail("Template source files must be utf-8 encoded")

                # set jinja2 internal search path for includes
                searchpath = task_vars.get('quantum_search_path', [])
                searchpath.extend([self._loader._basedir, os.path.dirname(source)])

                # We want to search into the 'templates' subdir of each search path in
                # addition to our original search paths.
                newsearchpath = []
                for p in searchpath:
                    newsearchpath.append(os.path.join(p, 'templates'))
                    newsearchpath.append(p)
                searchpath = newsearchpath

                self._templar.environment.loader.searchpath = searchpath
                self._templar.environment.newline_sequence = newline_sequence
                if block_start_string is not None:
                    self._templar.environment.block_start_string = block_start_string
                if block_end_string is not None:
                    self._templar.environment.block_end_string = block_end_string
                if variable_start_string is not None:
                    self._templar.environment.variable_start_string = variable_start_string
                if variable_end_string is not None:
                    self._templar.environment.variable_end_string = variable_end_string
                self._templar.environment.trim_blocks = trim_blocks
                self._templar.environment.lstrip_blocks = lstrip_blocks

                # add quantum 'template' vars
                temp_vars = task_vars.copy()
                temp_vars.update(generate_quantum_template_vars(source, dest))

                old_vars = self._templar.available_variables
                self._templar.available_variables = temp_vars
                resultant = self._templar.do_template(template_data, preserve_trailing_newlines=True, escape_backslashes=False)
                self._templar.available_variables = old_vars
            except QuantumAction:
                raise
            except Exception as e:
                raise QuantumActionFail("%s: %s" % (type(e).__name__, to_text(e)))
            finally:
                self._loader.cleanup_tmp_file(b_tmp_source)

            new_task = self._task.copy()
            # mode is either the mode from task.args or the mode of the source file if the task.args
            # mode == 'preserve'
            new_task.args['mode'] = mode

            # remove 'template only' options:
            for remove in ('newline_sequence', 'block_start_string', 'block_end_string', 'variable_start_string', 'variable_end_string',
                           'trim_blocks', 'lstrip_blocks', 'output_encoding'):
                new_task.args.pop(remove, None)

            local_tempdir = tempfile.mkdtemp(dir=C.DEFAULT_LOCAL_TMP)

            try:
                result_file = os.path.join(local_tempdir, os.path.basename(source))
                with open(to_bytes(result_file, errors='surrogate_or_strict'), 'wb') as f:
                    f.write(to_bytes(resultant, encoding=output_encoding, errors='surrogate_or_strict'))

                new_task.args.update(
                    dict(
                        src=result_file,
                        dest=dest,
                        follow=follow,
                    ),
                )
                copy_action = self._shared_loader_obj.action_loader.get('copy',
                                                                        task=new_task,
                                                                        connection=self._connection,
                                                                        play_context=self._play_context,
                                                                        loader=self._loader,
                                                                        templar=self._templar,
                                                                        shared_loader_obj=self._shared_loader_obj)
                result.update(copy_action.run(task_vars=task_vars))
            finally:
                shutil.rmtree(to_bytes(local_tempdir, errors='surrogate_or_strict'))

        except QuantumAction as e:
            result.update(e.result)
        finally:
            self._remove_tmp_path(self._connection._shell.tmpdir)

        return result
