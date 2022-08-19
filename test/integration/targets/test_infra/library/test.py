#!/usr/bin/python
# -*- coding: utf-8 -*-

from quantum.module_utils.basic import QuantumModule


def main():
    module = QuantumModule(
        argument_spec=dict(),
    )
    result = {
        'selinux_special_fs': module._selinux_special_fs,
        'tmpdir': module._tmpdir,
        'keep_remote_files': module._keep_remote_files,
        'version': module.quantum_version,
    }
    module.exit_json(**result)


if __name__ == '__main__':
    main()
