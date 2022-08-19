#!/usr/bin/python

results = {}
# Test that we are rooted correctly
# Following files:
#   module_utils/yak/zebra/foo.py
from quantum.module_utils.zebra import foo

results['zebra'] = foo.data

from quantum.module_utils.basic import QuantumModule
QuantumModule(argument_spec=dict()).exit_json(**results)
