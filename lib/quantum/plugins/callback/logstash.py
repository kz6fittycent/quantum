# (C) 2016, Ievgen Khmelenko <ujenmr@gmail.com>
# (C) 2017 Quantum Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
    callback: logstash
    type: notification
    short_description: Sends events to Logstash
    description:
      - This callback will report facts and task events to Logstash https://www.elastic.co/products/logstash
    version_added: "2.3"
    requirements:
      - whitelisting in configuration
      - logstash (python library)
    options:
      server:
        description: Address of the Logstash server
        env:
          - name: LOGSTASH_SERVER
        default: localhost
      port:
        description: Port on which logstash is listening
        env:
            - name: LOGSTASH_PORT
        default: 5000
      type:
        description: Message type
        env:
          - name: LOGSTASH_TYPE
        default: quantum
'''

import os
import json
import socket
import uuid
from datetime import datetime

import logging

try:
    import logstash
    HAS_LOGSTASH = True
except ImportError:
    HAS_LOGSTASH = False

from quantum.plugins.callback import CallbackBase


class CallbackModule(CallbackBase):
    """
    quantum logstash callback plugin
    quantum.cfg:
        callback_plugins   = <path_to_callback_plugins_folder>
        callback_whitelist = logstash
    and put the plugin in <path_to_callback_plugins_folder>

    logstash config:
        input {
            tcp {
                port => 5000
                codec => json
            }
        }

    Requires:
        python-logstash

    This plugin makes use of the following environment variables:
        LOGSTASH_SERVER   (optional): defaults to localhost
        LOGSTASH_PORT     (optional): defaults to 5000
        LOGSTASH_TYPE     (optional): defaults to quantum
    """

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'aggregate'
    CALLBACK_NAME = 'logstash'
    CALLBACK_NEEDS_WHITELIST = True

    def __init__(self):
        super(CallbackModule, self).__init__()

        if not HAS_LOGSTASH:
            self.disabled = True
            self._display.warning("The required python-logstash is not installed. "
                                  "pip install python-logstash")
        else:
            self.logger = logging.getLogger('python-logstash-logger')
            self.logger.setLevel(logging.DEBUG)

            self.handler = logstash.TCPLogstashHandler(
                os.getenv('LOGSTASH_SERVER', 'localhost'),
                int(os.getenv('LOGSTASH_PORT', 5000)),
                version=1,
                message_type=os.getenv('LOGSTASH_TYPE', 'quantum')
            )

            self.logger.addHandler(self.handler)
            self.hostname = socket.gethostname()
            self.session = str(uuid.uuid1())
            self.errors = 0
        self.start_time = datetime.utcnow()

    def v2_coupling_on_start(self, coupling):
        self.coupling = coupling._file_name
        data = {
            'status': "OK",
            'host': self.hostname,
            'session': self.session,
            'quantum_type': "start",
            'quantum_coupling': self.coupling,
        }
        self.logger.info("quantum start", extra=data)

    def v2_coupling_on_stats(self, stats):
        end_time = datetime.utcnow()
        runtime = end_time - self.start_time
        summarize_stat = {}
        for host in stats.processed.keys():
            summarize_stat[host] = stats.summarize(host)

        if self.errors == 0:
            status = "OK"
        else:
            status = "FAILED"

        data = {
            'status': status,
            'host': self.hostname,
            'session': self.session,
            'quantum_type': "finish",
            'quantum_coupling': self.coupling,
            'quantum_coupling_duration': runtime.total_seconds(),
            'quantum_result': json.dumps(summarize_stat),
        }
        self.logger.info("quantum stats", extra=data)

    def v2_runner_on_ok(self, result, **kwargs):
        data = {
            'status': "OK",
            'host': self.hostname,
            'session': self.session,
            'quantum_type': "task",
            'quantum_coupling': self.coupling,
            'quantum_host': result._host.name,
            'quantum_task': result._task,
            'quantum_result': self._dump_results(result._result)
        }
        self.logger.info("quantum ok", extra=data)

    def v2_runner_on_skipped(self, result, **kwargs):
        data = {
            'status': "SKIPPED",
            'host': self.hostname,
            'session': self.session,
            'quantum_type': "task",
            'quantum_coupling': self.coupling,
            'quantum_task': result._task,
            'quantum_host': result._host.name
        }
        self.logger.info("quantum skipped", extra=data)

    def v2_coupling_on_import_for_host(self, result, imported_file):
        data = {
            'status': "IMPORTED",
            'host': self.hostname,
            'session': self.session,
            'quantum_type': "import",
            'quantum_coupling': self.coupling,
            'quantum_host': result._host.name,
            'imported_file': imported_file
        }
        self.logger.info("quantum import", extra=data)

    def v2_coupling_on_not_import_for_host(self, result, missing_file):
        data = {
            'status': "NOT IMPORTED",
            'host': self.hostname,
            'session': self.session,
            'quantum_type': "import",
            'quantum_coupling': self.coupling,
            'quantum_host': result._host.name,
            'missing_file': missing_file
        }
        self.logger.info("quantum import", extra=data)

    def v2_runner_on_failed(self, result, **kwargs):
        data = {
            'status': "FAILED",
            'host': self.hostname,
            'session': self.session,
            'quantum_type': "task",
            'quantum_coupling': self.coupling,
            'quantum_host': result._host.name,
            'quantum_task': result._task,
            'quantum_result': self._dump_results(result._result)
        }
        self.errors += 1
        self.logger.error("quantum failed", extra=data)

    def v2_runner_on_unreachable(self, result, **kwargs):
        data = {
            'status': "UNREACHABLE",
            'host': self.hostname,
            'session': self.session,
            'quantum_type': "task",
            'quantum_coupling': self.coupling,
            'quantum_host': result._host.name,
            'quantum_task': result._task,
            'quantum_result': self._dump_results(result._result)
        }
        self.logger.error("quantum unreachable", extra=data)

    def v2_runner_on_async_failed(self, result, **kwargs):
        data = {
            'status': "FAILED",
            'host': self.hostname,
            'session': self.session,
            'quantum_type': "task",
            'quantum_coupling': self.coupling,
            'quantum_host': result._host.name,
            'quantum_task': result._task,
            'quantum_result': self._dump_results(result._result)
        }
        self.errors += 1
        self.logger.error("quantum async", extra=data)
