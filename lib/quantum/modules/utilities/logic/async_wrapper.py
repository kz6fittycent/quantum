#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2012, Michael DeHaan <michael.dehaan@gmail.com>, and others
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


import errno
import json
import shlex
import shutil
import os
import subprocess
import sys
import traceback
import signal
import time
import syslog
import multiprocessing

from quantum.module_utils._text import to_text, to_bytes

PY3 = sys.version_info[0] == 3

syslog.openlog('quantum-%s' % os.path.basename(__file__))
syslog.syslog(syslog.LOG_NOTICE, 'Invoked with %s' % " ".join(sys.argv[1:]))

# pipe for communication between forked process and parent
ipc_watcher, ipc_notifier = multiprocessing.Pipe()


def notice(msg):
    syslog.syslog(syslog.LOG_NOTICE, msg)


def daemonize_self():
    # daemonizing code: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66012
    try:
        pid = os.fork()
        if pid > 0:
            # exit first parent
            sys.exit(0)
    except OSError:
        e = sys.exc_info()[1]
        sys.exit("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))

    # decouple from parent environment (does not chdir / to keep the directory context the same as for non async tasks)
    os.setsid()
    os.umask(int('022', 8))

    # do second fork
    try:
        pid = os.fork()
        if pid > 0:
            # print "Daemon PID %d" % pid
            sys.exit(0)
    except OSError:
        e = sys.exc_info()[1]
        sys.exit("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))

    dev_null = open('/dev/null', 'w')
    os.dup2(dev_null.fileno(), sys.stdin.fileno())
    os.dup2(dev_null.fileno(), sys.stdout.fileno())
    os.dup2(dev_null.fileno(), sys.stderr.fileno())


# NB: this function copied from module_utils/json_utils.py. Ensure any changes are propagated there.
# FUTURE: QuantumModule-ify this module so it's Ansiballz-compatible and can use the module_utils copy of this function.
def _filter_non_json_lines(data):
    '''
    Used to filter unrelated output around module JSON output, like messages from
    tcagetattr, or where dropbear spews MOTD on every single command (which is nuts).

    Filters leading lines before first line-starting occurrence of '{' or '[', and filter all
    trailing lines after matching close character (working from the bottom of output).
    '''
    warnings = []

    # Filter initial junk
    lines = data.splitlines()

    for start, line in enumerate(lines):
        line = line.strip()
        if line.startswith(u'{'):
            endchar = u'}'
            break
        elif line.startswith(u'['):
            endchar = u']'
            break
    else:
        raise ValueError('No start of json char found')

    # Filter trailing junk
    lines = lines[start:]

    for reverse_end_offset, line in enumerate(reversed(lines)):
        if line.strip().endswith(endchar):
            break
    else:
        raise ValueError('No end of json char found')

    if reverse_end_offset > 0:
        # Trailing junk is uncommon and can point to things the user might
        # want to change.  So print a warning if we find any
        trailing_junk = lines[len(lines) - reverse_end_offset:]
        warnings.append('Module invocation had junk after the JSON data: %s' % '\n'.join(trailing_junk))

    lines = lines[:(len(lines) - reverse_end_offset)]

    return ('\n'.join(lines), warnings)


def _get_interpreter(module_path):
    with open(module_path, 'rb') as module_fd:
        head = module_fd.read(1024)
        if head[0:2] != b'#!':
            return None
        return head[2:head.index(b'\n')].strip().split(b' ')


def _make_temp_dir(path):
    # TODO: Add checks for permissions on path.
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def _run_module(wrapped_cmd, jid, job_path):

    tmp_job_path = job_path + ".tmp"
    jobfile = open(tmp_job_path, "w")
    jobfile.write(json.dumps({"started": 1, "finished": 0, "quantum_job_id": jid}))
    jobfile.close()
    os.rename(tmp_job_path, job_path)
    jobfile = open(tmp_job_path, "w")
    result = {}

    # signal grandchild process started and isolated from being terminated
    # by the connection being closed sending a signal to the job group
    ipc_notifier.send(True)
    ipc_notifier.close()

    outdata = ''
    filtered_outdata = ''
    stderr = ''
    try:
        cmd = [to_bytes(c, errors='surrogate_or_strict') for c in shlex.split(wrapped_cmd)]
        # call the module interpreter directly (for non-binary modules)
        # this permits use of a script for an interpreter on non-Linux platforms
        interpreter = _get_interpreter(cmd[0])
        if interpreter:
            cmd = interpreter + cmd
        script = subprocess.Popen(cmd, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)

        (outdata, stderr) = script.communicate()
        if PY3:
            outdata = outdata.decode('utf-8', 'surrogateescape')
            stderr = stderr.decode('utf-8', 'surrogateescape')

        (filtered_outdata, json_warnings) = _filter_non_json_lines(outdata)

        result = json.loads(filtered_outdata)

        if json_warnings:
            # merge JSON junk warnings with any existing module warnings
            module_warnings = result.get('warnings', [])
            if not isinstance(module_warnings, list):
                module_warnings = [module_warnings]
            module_warnings.extend(json_warnings)
            result['warnings'] = module_warnings

        if stderr:
            result['stderr'] = stderr
        jobfile.write(json.dumps(result))

    except (OSError, IOError):
        e = sys.exc_info()[1]
        result = {
            "failed": 1,
            "cmd": wrapped_cmd,
            "msg": to_text(e),
            "outdata": outdata,  # temporary notice only
            "stderr": stderr
        }
        result['quantum_job_id'] = jid
        jobfile.write(json.dumps(result))

    except (ValueError, Exception):
        result = {
            "failed": 1,
            "cmd": wrapped_cmd,
            "data": outdata,  # temporary notice only
            "stderr": stderr,
            "msg": traceback.format_exc()
        }
        result['quantum_job_id'] = jid
        jobfile.write(json.dumps(result))

    jobfile.close()
    os.rename(tmp_job_path, job_path)


def main():
    if len(sys.argv) < 5:
        print(json.dumps({
            "failed": True,
            "msg": "usage: async_wrapper <jid> <time_limit> <modulescript> <argsfile> [-preserve_tmp]  "
                   "Humans, do not call directly!"
        }))
        sys.exit(1)

    jid = "%s.%d" % (sys.argv[1], os.getpid())
    time_limit = sys.argv[2]
    wrapped_module = sys.argv[3]
    argsfile = sys.argv[4]
    if '-tmp-' not in os.path.dirname(wrapped_module):
        preserve_tmp = True
    elif len(sys.argv) > 5:
        preserve_tmp = sys.argv[5] == '-preserve_tmp'
    else:
        preserve_tmp = False
    # consider underscore as no argsfile so we can support passing of additional positional parameters
    if argsfile != '_':
        cmd = "%s %s" % (wrapped_module, argsfile)
    else:
        cmd = wrapped_module
    step = 5

    async_dir = os.environ.get('ANSIBLE_ASYNC_DIR', '~/.quantum_async')

    # setup job output directory
    jobdir = os.path.expanduser(async_dir)
    job_path = os.path.join(jobdir, jid)

    try:
        _make_temp_dir(jobdir)
    except Exception as e:
        print(json.dumps({
            "failed": 1,
            "msg": "could not create: %s - %s" % (jobdir, to_text(e)),
            "exception": to_text(traceback.format_exc()),
        }))
        sys.exit(1)

    # immediately exit this process, leaving an orphaned process
    # running which immediately forks a supervisory timing process

    try:
        pid = os.fork()
        if pid:
            # Notify the overlord that the async process started

            # we need to not return immediately such that the launched command has an attempt
            # to initialize PRIOR to quantum trying to clean up the launch directory (and argsfile)
            # this probably could be done with some IPC later.  Modules should always read
            # the argsfile at the very first start of their execution anyway

            # close off notifier handle in grandparent, probably unnecessary as
            # this process doesn't hang around long enough
            ipc_notifier.close()

            # allow waiting up to 2.5 seconds in total should be long enough for worst
            # loaded environment in practice.
            retries = 25
            while retries > 0:
                if ipc_watcher.poll(0.1):
                    break
                else:
                    retries = retries - 1
                    continue

            notice("Return async_wrapper task started.")
            print(json.dumps({"started": 1, "finished": 0, "quantum_job_id": jid, "results_file": job_path,
                              "_quantum_suppress_tmpdir_delete": not preserve_tmp}))
            sys.stdout.flush()
            sys.exit(0)
        else:
            # The actual wrapper process

            # close off the receiving end of the pipe from child process
            ipc_watcher.close()

            # Daemonize, so we keep on running
            daemonize_self()

            # we are now daemonized, create a supervisory process
            notice("Starting module and watcher")

            sub_pid = os.fork()
            if sub_pid:
                # close off inherited pipe handles
                ipc_watcher.close()
                ipc_notifier.close()

                # the parent stops the process after the time limit
                remaining = int(time_limit)

                # set the child process group id to kill all children
                os.setpgid(sub_pid, sub_pid)

                notice("Start watching %s (%s)" % (sub_pid, remaining))
                time.sleep(step)
                while os.waitpid(sub_pid, os.WNOHANG) == (0, 0):
                    notice("%s still running (%s)" % (sub_pid, remaining))
                    time.sleep(step)
                    remaining = remaining - step
                    if remaining <= 0:
                        notice("Now killing %s" % (sub_pid))
                        os.killpg(sub_pid, signal.SIGKILL)
                        notice("Sent kill to group %s " % sub_pid)
                        time.sleep(1)
                        if not preserve_tmp:
                            shutil.rmtree(os.path.dirname(wrapped_module), True)
                        sys.exit(0)
                notice("Done in kid B.")
                if not preserve_tmp:
                    shutil.rmtree(os.path.dirname(wrapped_module), True)
                sys.exit(0)
            else:
                # the child process runs the actual module
                notice("Start module (%s)" % os.getpid())
                _run_module(cmd, jid, job_path)
                notice("Module complete (%s)" % os.getpid())
                sys.exit(0)

    except SystemExit:
        # On python2.4, SystemExit is a subclass of Exception.
        # This block makes python2.4 behave the same as python2.5+
        raise

    except Exception:
        e = sys.exc_info()[1]
        notice("error: %s" % e)
        print(json.dumps({
            "failed": True,
            "msg": "FATAL ERROR: %s" % e
        }))
        sys.exit(1)


if __name__ == '__main__':
    main()
