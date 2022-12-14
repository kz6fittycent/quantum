import json
import sys

from quantum.module_utils.basic import QuantumModule


def main():
    if "--interactive" in sys.argv:
        import quantum.module_utils.basic
        quantum.module_utils.basic._ANSIBLE_ARGS = json.dumps(dict(
            ANSIBLE_MODULE_ARGS=dict(
                fail_mode="graceful"
            )
        ))

    module = QuantumModule(
        argument_spec=dict(
            fail_mode=dict(type='list', default=['success'])
        )
    )

    result = dict(changed=True)

    fail_mode = module.params['fail_mode']

    try:
        if 'leading_junk' in fail_mode:
            print("leading junk before module output")

        if 'graceful' in fail_mode:
            module.fail_json(msg="failed gracefully")

        if 'exception' in fail_mode:
            raise Exception('failing via exception')

        module.exit_json(**result)

    finally:
        if 'trailing_junk' in fail_mode:
            print("trailing junk after module output")


main()
