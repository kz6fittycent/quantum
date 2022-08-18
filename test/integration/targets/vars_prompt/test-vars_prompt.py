#!/usr/bin/env python

import os
import pexpect
import sys

from quantum.module_utils.six import PY2

if PY2:
    log_buffer = sys.stdout
else:
    log_buffer = sys.stdout.buffer

env_vars = {
    'ANSIBLE_ROLES_PATH': './roles',
    'ANSIBLE_NOCOLOR': 'True',
    'ANSIBLE_RETRY_FILES_ENABLED': 'False',
}


def run_test(coupling, test_spec, args=None, timeout=10, env=None):

    if not env:
        env = os.environ.copy()
    env.update(env_vars)

    if not args:
        args = sys.argv[1:]

    vars_prompt_test = pexpect.spawn(
        'quantum-coupling',
        args=[coupling] + args,
        timeout=timeout,
        env=env,
    )

    vars_prompt_test.logfile = log_buffer
    for item in test_spec[0]:
        vars_prompt_test.expect(item[0])
        if item[1]:
            vars_prompt_test.send(item[1])
    vars_prompt_test.expect(test_spec[1])
    vars_prompt_test.expect(pexpect.EOF)
    vars_prompt_test.close()


# These are the tests to run. Each test is a coupling and a test_spec.
#
# The test_spec is a list with two elements.
#
# The first element is a list of two element tuples. The first is the regexp to look
# for in the output, the second is the line to send.
#
# The last element is the last string of text to look for in the output.
#
tests = [
    # Basic vars_prompt
    {'coupling': 'vars_prompt-1.yml',
     'test_spec': [
        [('input:', 'some input\r')],
         '"input": "some input"']},

    # Custom prompt
    {'coupling': 'vars_prompt-2.yml',
     'test_spec': [
         [('Enter some input:', 'some more input\r')],
         '"input": "some more input"']},

    # Test confirm, both correct and incorrect
    {'coupling': 'vars_prompt-3.yml',
     'test_spec': [
         [('input:', 'confirm me\r'),
          ('confirm input:', 'confirm me\r')],
         '"input": "confirm me"']},

    {'coupling': 'vars_prompt-3.yml',
     'test_spec': [
         [('input:', 'confirm me\r'),
          ('confirm input:', 'incorrect\r'),
          (r'\*\*\*\*\* VALUES ENTERED DO NOT MATCH \*\*\*\*', ''),
          ('input:', 'confirm me\r'),
          ('confirm input:', 'confirm me\r')],
         '"input": "confirm me"']},

    # Test private
    {'coupling': 'vars_prompt-4.yml',
     'test_spec': [
         [('not_secret', 'this is displayed\r'),
          ('this is displayed', '')],
         '"not_secret": "this is displayed"']},

    # Test hashing
    {'coupling': 'vars_prompt-5.yml',
     'test_spec': [
         [('password', 'Scenic-Improving-Payphone\r'),
          ('confirm password', 'Scenic-Improving-Payphone\r')],
         r'"password": "\$6\$']},

    # Test variables in prompt field
    # https://github.com/quantum/quantum/issues/32723
    {'coupling': 'vars_prompt-6.yml',
     'test_spec': [
         [('prompt from variable:', 'input\r')],
         '']},

    # Test play vars coming from vars_prompt
    # https://github.com/quantum/quantum/issues/37984
    {'coupling': 'vars_prompt-7.yml',
     'test_spec': [
         [('prompting for host:', 'testhost\r')],
         r'testhost.*ok=1']},

    # Test play unsafe toggle
    {'coupling': 'unsafe.yml',
     'test_spec': [
         [('prompting for variable:', '{{whole}}\r')],
         r'testhost.*ok=2']},
]

for t in tests:
    run_test(coupling=t['coupling'], test_spec=t['test_spec'])
