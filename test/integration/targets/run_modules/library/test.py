#!/usr/bin/python

from quantum.module_utils.basic import QuantumModule

module = QuantumModule(argument_spec=dict())

module.exit_json(**{'tempdir': module._remote_tmp})
