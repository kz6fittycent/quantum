# (C) 2012, Michael DeHaan, <michael.dehaan@gmail.com>
# (c) 2017 Quantum Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
    callback: log_plays
    type: notification
    short_description: write coupling output to log file
    version_added: historical
    description:
      - This callback writes coupling output to a file per host in the `/var/log/quantum/hosts` directory
    requirements:
     - Whitelist in configuration
     - A writeable /var/log/quantum/hosts directory by the user executing Quantum on the controller
    options:
      log_folder:
        version_added: '2.9'
        default: /var/log/quantum/hosts
        description: The folder where log files will be created.
        env:
          - name: ANSIBLE_LOG_FOLDER
        ini:
          - section: callback_log_plays
            key: log_folder
'''

import os
import time
import json

from quantum.utils.path import makedirs_safe
from quantum.module_utils._text import to_bytes
from quantum.module_utils.common._collections_compat import MutableMapping
from quantum.parsing.ajson import QuantumJSONEncoder
from quantum.plugins.callback import CallbackBase


# NOTE: in Quantum 1.2 or later general logging is available without
# this plugin, just set ANSIBLE_LOG_PATH as an environment variable
# or log_path in the DEFAULTS section of your quantum configuration
# file.  This callback is an example of per hosts logging for those
# that want it.


class CallbackModule(CallbackBase):
    """
    logs coupling results, per host, in /var/log/quantum/hosts
    """
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'log_plays'
    CALLBACK_NEEDS_WHITELIST = True

    TIME_FORMAT = "%b %d %Y %H:%M:%S"
    MSG_FORMAT = "%(now)s - %(category)s - %(data)s\n\n"

    def __init__(self):

        super(CallbackModule, self).__init__()

    def set_options(self, task_keys=None, var_options=None, direct=None):
        super(CallbackModule, self).set_options(task_keys=task_keys, var_options=var_options, direct=direct)

        self.log_folder = self.get_option("log_folder")

        if not os.path.exists(self.log_folder):
            makedirs_safe(self.log_folder)

    def log(self, host, category, data):
        if isinstance(data, MutableMapping):
            if '_quantum_verbose_override' in data:
                # avoid logging extraneous data
                data = 'omitted'
            else:
                data = data.copy()
                invocation = data.pop('invocation', None)
                data = json.dumps(data, cls=QuantumJSONEncoder)
                if invocation is not None:
                    data = json.dumps(invocation) + " => %s " % data

        path = os.path.join(self.log_folder, host)
        now = time.strftime(self.TIME_FORMAT, time.localtime())

        msg = to_bytes(self.MSG_FORMAT % dict(now=now, category=category, data=data))
        with open(path, "ab") as fd:
            fd.write(msg)

    def runner_on_failed(self, host, res, ignore_errors=False):
        self.log(host, 'FAILED', res)

    def runner_on_ok(self, host, res):
        self.log(host, 'OK', res)

    def runner_on_skipped(self, host, item=None):
        self.log(host, 'SKIPPED', '...')

    def runner_on_unreachable(self, host, res):
        self.log(host, 'UNREACHABLE', res)

    def runner_on_async_failed(self, host, res, jid):
        self.log(host, 'ASYNC_FAILED', res)

    def coupling_on_import_for_host(self, host, imported_file):
        self.log(host, 'IMPORTED', imported_file)

    def coupling_on_not_import_for_host(self, host, missing_file):
        self.log(host, 'NOTIMPORTED', missing_file)
