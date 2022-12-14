#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2017, Simon Dodsley (simon@purestorage.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: purefa_pgsnap
version_added: '2.6'
short_description: Manage protection group snapshots on Pure Storage FlashArrays
description:
- Create or delete protection group snapshots on Pure Storage FlashArray.
- Recovery of replicated snapshots on the replica target array is enabled.
author:
- Pure Storage Quantum Team (@sdodsley) <pure-quantum-team@purestorage.com>
options:
  name:
    description:
    - The name of the source protection group.
    type: str
    required: true
  suffix:
    description:
    - Suffix of snapshot name.
  state:
    description:
    - Define whether the protection group snapshot should exist or not.
      Copy (added in 2.7) will create a full read/write clone of the
      snapshot.
    type: str
    choices: [ absent, present, copy ]
    default: present
  eradicate:
    description:
    - Define whether to eradicate the snapshot on delete or leave in trash.
    type: bool
    default: 'no'
  restore:
    description:
    - Restore a specific volume from a protection group snapshot.
    type: str
    version_added: 2.7
  overwrite:
    description:
    - Define whether to overwrite the target volume if it already exists.
    type: bool
    default: 'no'
    version_added: 2.8
  target:
    description:
    - Volume to restore a specified volume to.
    - If not supplied this will default to the volume defined in I(restore)
    type: str
    version_added: 2.8
  now:
    description: Whether to initiate a snapshot of the protection group immediately
    type: bool
    default: False
    version_added: 2.9
  apply_retention:
    description: Apply retention schedule settings to the snapshot
    type: bool
    default: False
    version_added: 2.9
  remote:
    description: Force immeadiate snapshot to remote targets
    type: bool
    default: False
    version_added: 2.9
extends_documentation_fragment:
- purestorage.fa
'''

EXAMPLES = r'''
- name: Create protection group snapshot foo.quantum
  purefa_pgsnap:
    name: foo
    suffix: quantum
    fa_url: 10.10.10.2
    api_token: e31060a7-21fc-e277-6240-25983c6c4592
    state: present

- name: Delete and eradicate protection group snapshot named foo.snap
  purefa_pgsnap:
    name: foo
    suffix: snap
    eradicate: true
    fa_url: 10.10.10.2
    api_token: e31060a7-21fc-e277-6240-25983c6c4592
    state: absent

- name: Restore volume data from local protection group snapshot named foo.snap to volume data2
  purefa_pgsnap:
    name: foo
    suffix: snap
    restore: data
    target: data2
    overwrite: true
    fa_url: 10.10.10.2
    api_token: e31060a7-21fc-e277-6240-25983c6c4592
    state: copy

- name: Restore remote protection group snapshot arrayA:pgname.snap.data to local copy
  purefa_pgsnap:
    name: arrayA:pgname
    suffix: snap
    restore: data
    fa_url: 10.10.10.2
    api_token: e31060a7-21fc-e277-6240-25983c6c4592
    state: copy

- name: Create snapshot of existing pgroup foo with suffix and force immeadiate copy to remote targets
  purefa_pgsnap:
    name: pgname
    suffix: force
    now: True
    apply_retention: True
    remote: True
    fa_url: 10.10.10.2
    api_token: e31060a7-21fc-e277-6240-25983c6c4592
    state: copy
'''

RETURN = r'''
'''

from quantum.module_utils.basic import QuantumModule
from quantum.module_utils.pure import get_system, purefa_argument_spec

from datetime import datetime


def get_pgroup(module, array):
    """Return Protection Group or None"""
    try:
        return array.get_pgroup(module.params['name'])
    except Exception:
        return None


def get_pgroupvolume(module, array):
    """Return Protection Group Volume or None"""
    try:
        pgroup = array.get_pgroup(module.params['name'])
        for volume in pgroup['volumes']:
            if volume == module.params['restore']:
                return volume
    except Exception:
        return None


def get_rpgsnapshot(module, array):
    """Return iReplicated Snapshot or None"""
    try:
        snapname = module.params['name'] + "." + module.params['suffix'] + "." + module.params['restore']
        for snap in array.list_volumes(snap=True):
            if snap['name'] == snapname:
                return snapname
    except Exception:
        return None


def get_pgsnapshot(module, array):
    """Return Snapshot (active or deleted) or None"""
    try:
        snapname = module.params['name'] + "." + module.params['suffix']
        for snap in array.get_pgroup(module.params['name'], snap=True, pending=True):
            if snap['name'] == snapname:
                return snapname
    except Exception:
        return None


def create_pgsnapshot(module, array):
    """Create Protection Group Snapshot"""
    changed = True
    if not module.check_mode:
        try:
            if module.params['now'] and array.get_pgroup(module.params['name'])['targets'] is not None:
                array.create_pgroup_snapshot(source=module.params['name'],
                                             suffix=module.params['suffix'],
                                             snap=True,
                                             apply_retention=module.params['apply_retention'],
                                             replicate_now=module.params['remote'])
            else:
                array.create_pgroup_snapshot(source=module.params['name'],
                                             suffix=module.params['suffix'],
                                             snap=True,
                                             apply_retention=module.params['apply_retention'])
        except Exception:
            module.fail_json(msg="Snapshot of pgroup {0} failed.".format(module.params['name']))
    module.exit_json(changed=changed)


def restore_pgsnapvolume(module, array):
    """Restore a Protection Group Snapshot Volume"""
    changed = True
    if not module.check_mode:
        if ":" in module.params['name']:
            if get_rpgsnapshot(module, array)is None:
                module.fail_json(msg="Selected restore snapshot {0} does not exist in the Protection Group".format(module.params['restore']))
        else:
            if get_pgroupvolume(module, array) is None:
                module.fail_json(msg="Selected restore volume {0} does not exist in the Protection Group".format(module.params['restore']))
        volume = module.params['name'] + "." + module.params['suffix'] + "." + module.params['restore']
        try:
            array.copy_volume(volume, module.params['target'], overwrite=module.params['overwrite'])
        except Exception:
            module.fail_json(msg="Failed to restore {0} from pgroup {1}".format(volume, module.params['name']))
    module.exit_json(changed=changed)


def update_pgsnapshot(module, array):
    """Update Protection Group Snapshot"""
    changed = True
    module.exit_json(changed=changed)


def delete_pgsnapshot(module, array):
    """ Delete Protection Group Snapshot"""
    changed = True
    if not module.check_mode:
        snapname = module.params['name'] + "." + module.params['suffix']
        try:
            array.destroy_pgroup(snapname)
            if module.params['eradicate']:
                try:
                    array.eradicate_pgroup(snapname)
                except Exception:
                    module.fail_json(msg="Failed to eradicate pgroup {0}".format(snapname))
        except Exception:
            module.fail_json(msg="Failed to delete pgroup {0}".format(snapname))
    module.exit_json(changed=changed)


def main():
    argument_spec = purefa_argument_spec()
    argument_spec.update(dict(
        name=dict(type='str', required=True),
        suffix=dict(type='str'),
        restore=dict(type='str'),
        overwrite=dict(type='bool', default=False),
        target=dict(type='str'),
        eradicate=dict(type='bool', default=False),
        now=dict(type='bool', default=False),
        apply_retention=dict(type='bool', default=False),
        remote=dict(type='bool', default=False),
        state=dict(type='str', default='present', choices=['absent', 'present', 'copy']),
    ))

    required_if = [('state', 'copy', ['suffix', 'restore'])]

    module = QuantumModule(argument_spec,
                           required_if=required_if,
                           supports_check_mode=True)

    if module.params['suffix'] is None:
        suffix = "snap-" + str((datetime.utcnow() - datetime(1970, 1, 1, 0, 0, 0, 0)).total_seconds())
        module.params['suffix'] = suffix.replace(".", "")

    if not module.params['target'] and module.params['restore']:
        module.params['target'] = module.params['restore']

    state = module.params['state']
    array = get_system(module)
    pgroup = get_pgroup(module, array)
    if pgroup is None:
        module.fail_json(msg="Protection Group {0} does not exist.".format(module.params['name']))
    pgsnap = get_pgsnapshot(module, array)

    if state == 'copy':
        restore_pgsnapvolume(module, array)
    elif state == 'present' and not pgsnap:
        create_pgsnapshot(module, array)
    elif state == 'present' and pgsnap:
        update_pgsnapshot(module, array)
    elif state == 'absent' and pgsnap:
        delete_pgsnapshot(module, array)
    elif state == 'absent' and not pgsnap:
        module.exit_json(changed=False)

    module.exit_json(changed=False)


if __name__ == '__main__':
    main()
