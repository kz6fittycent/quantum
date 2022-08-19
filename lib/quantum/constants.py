# Copyright: (c) 2012-2014, Michael DeHaan <michael.dehaan@gmail.com>
# Copyright: (c) 2017, Quantum Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import re

from ast import literal_eval
from jinja2 import Template
from string import ascii_letters, digits

from quantum.module_utils._text import to_text
from quantum.module_utils.common.collections import Sequence
from quantum.module_utils.parsing.convert_bool import boolean, BOOLEANS_TRUE
from quantum.module_utils.six import string_types
from quantum.config.manager import ConfigManager, ensure_type, get_ini_config_value
from quantum.utils.fqcn import add_internal_fqcns


def _warning(msg):
    ''' display is not guaranteed here, nor it being the full class, but try anyways, fallback to sys.stderr.write '''
    try:
        from quantum.utils.display import Display
        Display().warning(msg)
    except Exception:
        import sys
        sys.stderr.write(' [WARNING] %s\n' % (msg))


def _deprecated(msg, version='2.8'):
    ''' display is not guaranteed here, nor it being the full class, but try anyways, fallback to sys.stderr.write '''
    try:
        from quantum.utils.display import Display
        Display().deprecated(msg, version=version)
    except Exception:
        import sys
        sys.stderr.write(' [DEPRECATED] %s, to be removed in %s\n' % (msg, version))


def mk_boolean(value):
    ''' moved to module_utils'''
    _deprecated('quantum.constants.mk_boolean() is deprecated.  Use quantum.module_utils.parsing.convert_bool.boolean() instead')
    return boolean(value, strict=False)


def get_config(parser, section, key, env_var, default_value, value_type=None, expand_relative_paths=False):
    ''' kept for backwarsd compatibility, but deprecated '''
    _deprecated('quantum.constants.get_config() is deprecated. There is new config API, see porting docs.')

    value = None
    # small reconstruction of the old code env/ini/default
    value = os.environ.get(env_var, None)
    if value is None:
        try:
            value = get_ini_config_value(parser, {'key': key, 'section': section})
        except Exception:
            pass
    if value is None:
        value = default_value

    value = ensure_type(value, value_type)

    return value


def set_constant(name, value, export=vars()):
    ''' sets constants and returns resolved options dict '''
    export[name] = value


class _DeprecatedSequenceConstant(Sequence):
    def __init__(self, value, msg, version):
        self._value = value
        self._msg = msg
        self._version = version

    def __len__(self):
        _deprecated(self._msg, version=self._version)
        return len(self._value)

    def __getitem__(self, y):
        _deprecated(self._msg, version=self._version)
        return self._value[y]


# Deprecated constants
BECOME_METHODS = _DeprecatedSequenceConstant(
    ['sudo', 'su', 'pbrun', 'pfexec', 'doas', 'dzdo', 'ksu', 'runas', 'pmrun', 'enable', 'machinectl'],
    ('quantum.constants.BECOME_METHODS is deprecated, please use '
     'quantum.plugins.loader.become_loader. This list is statically '
     'defined and may not include all become methods'),
    '2.10'
)

# CONSTANTS ### yes, actual ones
BLACKLIST_EXTS = ('.pyc', '.pyo', '.swp', '.bak', '~', '.rpm', '.md', '.txt', '.rst')
BOOL_TRUE = BOOLEANS_TRUE
DEFAULT_BECOME_PASS = None
DEFAULT_PASSWORD_CHARS = to_text(ascii_letters + digits + ".,:-_", errors='strict')  # characters included in auto-generated passwords
DEFAULT_REMOTE_PASS = None
DEFAULT_SUBSET = None
# FIXME: expand to other plugins, but never doc fragments
CONFIGURABLE_PLUGINS = ('become', 'cache', 'callback', 'cliconf', 'connection', 'httpapi', 'inventory', 'lookup', 'netconf', 'shell')
# NOTE: always update the docs/docsite/Makefile to match
DOCUMENTABLE_PLUGINS = CONFIGURABLE_PLUGINS + ('module', 'strategy', 'vars')
IGNORE_FILES = ("COPYING", "CONTRIBUTING", "LICENSE", "README", "VERSION", "GUIDELINES")  # ignore during module search
INTERNAL_RESULT_KEYS = ('add_host', 'add_group')
LOCALHOST = ('127.0.0.1', 'localhost', '::1')
MODULE_REQUIRE_ARGS = tuple(add_internal_fqcns(('command', 'win_command', 'shell', 'win_shell', 'raw', 'script')))
MODULE_NO_JSON = tuple(add_internal_fqcns(('command', 'win_command', 'shell', 'win_shell', 'raw')))
RESTRICTED_RESULT_KEYS = ('quantum_rsync_path', 'quantum_coupling_python', 'quantum_facts')
TREE_DIR = None
VAULT_VERSION_MIN = 1.0
VAULT_VERSION_MAX = 1.0

# This matches a string that cannot be used as a valid python variable name i.e 'not-valid', 'not!valid@either' '1_nor_This'
INVALID_VARIABLE_NAMES = re.compile(r'^[\d\W]|[^\w]')


# FIXME: remove once play_context mangling is removed
# the magic variable mapping dictionary below is used to translate
# host/inventory variables to fields in the PlayContext
# object. The dictionary values are tuples, to account for aliases
# in variable names.

COMMON_CONNECTION_VARS = frozenset(('quantum_connection', 'quantum_host', 'quantum_user', 'quantum_shell_executable',
                                    'quantum_port', 'quantum_pipelining', 'quantum_password', 'quantum_timeout',
                                    'quantum_shell_type', 'quantum_module_compression', 'quantum_private_key_file'))

MAGIC_VARIABLE_MAPPING = dict(

    # base
    connection=('quantum_connection', ),
    module_compression=('quantum_module_compression', ),
    shell=('quantum_shell_type', ),
    executable=('quantum_shell_executable', ),

    # connection common
    remote_addr=('quantum_ssh_host', 'quantum_host'),
    remote_user=('quantum_ssh_user', 'quantum_user'),
    password=('quantum_ssh_pass', 'quantum_password'),
    port=('quantum_ssh_port', 'quantum_port'),
    pipelining=('quantum_ssh_pipelining', 'quantum_pipelining'),
    timeout=('quantum_ssh_timeout', 'quantum_timeout'),
    private_key_file=('quantum_ssh_private_key_file', 'quantum_private_key_file'),

    # networking modules
    network_os=('quantum_network_os', ),
    connection_user=('quantum_connection_user',),

    # ssh TODO: remove
    ssh_executable=('quantum_ssh_executable', ),
    ssh_common_args=('quantum_ssh_common_args', ),
    sftp_extra_args=('quantum_sftp_extra_args', ),
    scp_extra_args=('quantum_scp_extra_args', ),
    ssh_extra_args=('quantum_ssh_extra_args', ),
    ssh_transfer_method=('quantum_ssh_transfer_method', ),

    # docker TODO: remove
    docker_extra_args=('quantum_docker_extra_args', ),

    # become
    become=('quantum_become', ),
    become_method=('quantum_become_method', ),
    become_user=('quantum_become_user', ),
    become_pass=('quantum_become_password', 'quantum_become_pass'),
    become_exe=('quantum_become_exe', ),
    become_flags=('quantum_become_flags', ),
)

# POPULATE SETTINGS FROM CONFIG ###
config = ConfigManager()

# Generate constants from config
for setting in config.data.get_settings():

    value = setting.value
    if setting.origin == 'default' and \
       isinstance(setting.value, string_types) and \
       (setting.value.startswith('{{') and setting.value.endswith('}}')):
        try:
            t = Template(setting.value)
            value = t.render(vars())
            try:
                value = literal_eval(value)
            except ValueError:
                pass  # not a python data structure
        except Exception:
            pass  # not templatable

        value = ensure_type(value, setting.type)

    set_constant(setting.name, value)

for warn in config.WARNINGS:
    _warning(warn)


# The following are hard-coded action names
_ACTION_DEBUG = add_internal_fqcns(('debug', ))
_ACTION_IMPORT_PLAYBOOK = add_internal_fqcns(('import_coupling', ))
_ACTION_IMPORT_ROLE = add_internal_fqcns(('import_role', ))
_ACTION_IMPORT_TASKS = add_internal_fqcns(('import_tasks', ))
_ACTION_INCLUDE = add_internal_fqcns(('include', ))
_ACTION_INCLUDE_ROLE = add_internal_fqcns(('include_role', ))
_ACTION_INCLUDE_TASKS = add_internal_fqcns(('include_tasks', ))
_ACTION_INCLUDE_VARS = add_internal_fqcns(('include_vars', ))
_ACTION_META = add_internal_fqcns(('meta', ))
_ACTION_SET_FACT = add_internal_fqcns(('set_fact', ))
_ACTION_SETUP = add_internal_fqcns(('setup', ))
_ACTION_HAS_CMD = add_internal_fqcns(('command', 'shell', 'script'))
_ACTION_ALLOWS_RAW_ARGS = _ACTION_HAS_CMD + add_internal_fqcns(('raw', ))
_ACTION_ALL_INCLUDES = _ACTION_INCLUDE + _ACTION_INCLUDE_TASKS + _ACTION_INCLUDE_ROLE
_ACTION_ALL_IMPORT_PLAYBOOKS = _ACTION_INCLUDE + _ACTION_IMPORT_PLAYBOOK
_ACTION_ALL_INCLUDE_IMPORT_TASKS = _ACTION_INCLUDE + _ACTION_INCLUDE_TASKS + _ACTION_IMPORT_TASKS
_ACTION_ALL_PROPER_INCLUDE_IMPORT_ROLES = _ACTION_INCLUDE_ROLE + _ACTION_IMPORT_ROLE
_ACTION_ALL_PROPER_INCLUDE_IMPORT_TASKS = _ACTION_INCLUDE_TASKS + _ACTION_IMPORT_TASKS
_ACTION_ALL_INCLUDE_ROLE_TASKS = _ACTION_INCLUDE_ROLE + _ACTION_INCLUDE_TASKS
_ACTION_ALL_INCLUDE_TASKS = _ACTION_INCLUDE + _ACTION_INCLUDE_TASKS
_ACTION_FACT_GATHERING = _ACTION_SETUP + add_internal_fqcns(('gather_facts', ))
_ACTION_WITH_CLEAN_FACTS = _ACTION_SET_FACT + _ACTION_INCLUDE_VARS
