#!/usr/bin/env python
#
# (c) 2018, Red Hat, Inc.
#
# This file is part of Quantum
#
# Quantum is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Quantum is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Quantum.  If not, see <http://www.gnu.org/licenses/>.
#
import os
import sys
import json
import argparse

from quantum.parsing.dataloader import DataLoader
from quantum.module_utils.six import iteritems
from quantum.module_utils._text import to_text
from quantum.module_utils.net_tools.nios.api import WapiInventory
from quantum.module_utils.net_tools.nios.api import normalize_extattrs, flatten_extattrs


CONFIG_FILES = [
    '/etc/quantum/infoblox.yaml',
    '/etc/quantum/infoblox.yml'
]


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--list', action='store_true',
                        help='List host records from NIOS for use in Quantum')

    parser.add_argument('--host',
                        help='List meta data about single host (not used)')

    return parser.parse_args()


def main():
    args = parse_args()

    for config_file in CONFIG_FILES:
        if os.path.exists(config_file):
            break
    else:
        sys.stdout.write('unable to locate config file at /etc/quantum/infoblox.yaml\n')
        sys.exit(-1)

    try:
        loader = DataLoader()
        config = loader.load_from_file(config_file)
        provider = config.get('provider') or {}
        wapi = WapiInventory(provider)
    except Exception as exc:
        sys.stdout.write(to_text(exc))
        sys.exit(-1)

    if args.host:
        host_filter = {'name': args.host}
    else:
        host_filter = {}

    config_filters = config.get('filters')

    if config_filters.get('view') is not None:
        host_filter['view'] = config_filters['view']

    if config_filters.get('extattrs'):
        extattrs = normalize_extattrs(config_filters['extattrs'])
    else:
        extattrs = {}

    hostvars = {}
    inventory = {
        '_meta': {
            'hostvars': hostvars
        }
    }

    return_fields = ['name', 'view', 'extattrs', 'ipv4addrs']

    hosts = wapi.get_object('record:host',
                            host_filter,
                            extattrs=extattrs,
                            return_fields=return_fields)

    if hosts:
        for item in hosts:
            view = item['view']
            name = item['name']

            if view not in inventory:
                inventory[view] = {'hosts': []}

            inventory[view]['hosts'].append(name)

            hostvars[name] = {
                'view': view
            }

            if item.get('extattrs'):
                for key, value in iteritems(flatten_extattrs(item['extattrs'])):
                    if key.startswith('quantum_'):
                        hostvars[name][key] = value
                    else:
                        if 'extattrs' not in hostvars[name]:
                            hostvars[name]['extattrs'] = {}
                        hostvars[name]['extattrs'][key] = value

    sys.stdout.write(json.dumps(inventory, indent=4))
    sys.exit(0)


if __name__ == '__main__':
    main()
