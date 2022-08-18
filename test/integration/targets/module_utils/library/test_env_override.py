#!/usr/bin/python
# Most of these names are only available via PluginLoader so pylint doesn't
# know they exist
# pylint: disable=no-name-in-module
from quantum.module_utils.basic import QuantumModule
from quantum.module_utils.json_utils import data
from quantum.module_utils.mork import data as mork_data

results = {"json_utils": data, "mork": mork_data}

QuantumModule(argument_spec=dict()).exit_json(**results)
