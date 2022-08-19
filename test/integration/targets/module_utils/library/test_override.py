#!/usr/bin/python
from quantum.module_utils.basic import QuantumModule
from quantum.module_utils.facts import data

results = {"data": data}

QuantumModule(argument_spec=dict()).exit_json(**results)
