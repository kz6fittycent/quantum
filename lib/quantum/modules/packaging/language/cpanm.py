#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2012, Franck Cuny <franck@lumberjaph.net>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: cpanm
short_description: Manages Perl library dependencies.
description:
  - Manage Perl library dependencies.
version_added: "1.6"
options:
  name:
    description:
      - The name of the Perl library to install. You may use the "full distribution path", e.g.  MIYAGAWA/Plack-0.99_05.tar.gz
    aliases: ["pkg"]
  from_path:
    description:
      - The local directory from where to install
  notest:
    description:
      - Do not run unit tests
    type: bool
    default: no
  locallib:
    description:
      - Specify the install base to install modules
    type: path
  mirror:
    description:
      - Specifies the base URL for the CPAN mirror to use
    type: str
  mirror_only:
    description:
      - Use the mirror's index file instead of the CPAN Meta DB
    type: bool
    default: no
  installdeps:
    description:
      - Only install dependencies
    type: bool
    default: no
    version_added: "2.0"
  version:
    description:
      - minimum version of perl module to consider acceptable
    type: str
    version_added: "2.1"
  system_lib:
    description:
     -  Use this if you want to install modules to the system perl include path. You must be root or have "passwordless" sudo for this to work.
     -  This uses the cpanm commandline option '--sudo', which has nothing to do with quantum privilege escalation.
    type: bool
    default: no
    aliases: ['use_sudo']
    version_added: "2.0"
  executable:
    description:
      - Override the path to the cpanm executable
    type: path
    version_added: "2.1"
notes:
   - Please note that U(http://search.cpan.org/dist/App-cpanminus/bin/cpanm, cpanm) must be installed on the remote host.
author: "Franck Cuny (@fcuny)"
'''

EXAMPLES = '''
# install Dancer perl package
- cpanm:
    name: Dancer

# install version 0.99_05 of the Plack perl package
- cpanm:
    name: MIYAGAWA/Plack-0.99_05.tar.gz

# install Dancer into the specified locallib
- cpanm:
    name: Dancer
    locallib: /srv/webapps/my_app/extlib

# install perl dependencies from local directory
- cpanm:
    from_path: /srv/webapps/my_app/src/

# install Dancer perl package without running the unit tests in indicated locallib
- cpanm:
    name: Dancer
    notest: True
    locallib: /srv/webapps/my_app/extlib

# install Dancer perl package from a specific mirror
- cpanm:
    name: Dancer
    mirror: 'http://cpan.cpantesters.org/'

# install Dancer perl package into the system root path
- cpanm:
    name: Dancer
    system_lib: yes

# install Dancer if it's not already installed
# OR the installed version is older than version 1.0
- cpanm:
    name: Dancer
    version: '1.0'
'''

import os

from quantum.module_utils.basic import QuantumModule


def _is_package_installed(module, name, locallib, cpanm, version):
    cmd = ""
    if locallib:
        os.environ["PERL5LIB"] = "%s/lib/perl5" % locallib
    cmd = "%s perl -e ' use %s" % (cmd, name)
    if version:
        cmd = "%s %s;'" % (cmd, version)
    else:
        cmd = "%s;'" % cmd
    res, stdout, stderr = module.run_command(cmd, check_rc=False)
    return res == 0


def _build_cmd_line(name, from_path, notest, locallib, mirror, mirror_only, installdeps, cpanm, use_sudo):
    # this code should use "%s" like everything else and just return early but not fixing all of it now.
    # don't copy stuff like this
    if from_path:
        cmd = cpanm + " " + from_path
    else:
        cmd = cpanm + " " + name

    if notest is True:
        cmd = cmd + " -n"

    if locallib is not None:
        cmd = cmd + " -l " + locallib

    if mirror is not None:
        cmd = cmd + " --mirror " + mirror

    if mirror_only is True:
        cmd = cmd + " --mirror-only"

    if installdeps is True:
        cmd = cmd + " --installdeps"

    if use_sudo is True:
        cmd = cmd + " --sudo"

    return cmd


def _get_cpanm_path(module):
    if module.params['executable']:
        result = module.params['executable']
    else:
        result = module.get_bin_path('cpanm', True)
    return result


def main():
    arg_spec = dict(
        name=dict(default=None, required=False, aliases=['pkg']),
        from_path=dict(default=None, required=False, type='path'),
        notest=dict(default=False, type='bool'),
        locallib=dict(default=None, required=False, type='path'),
        mirror=dict(default=None, required=False),
        mirror_only=dict(default=False, type='bool'),
        installdeps=dict(default=False, type='bool'),
        system_lib=dict(default=False, type='bool', aliases=['use_sudo']),
        version=dict(default=None, required=False),
        executable=dict(required=False, type='path'),
    )

    module = QuantumModule(
        argument_spec=arg_spec,
        required_one_of=[['name', 'from_path']],
    )

    cpanm = _get_cpanm_path(module)
    name = module.params['name']
    from_path = module.params['from_path']
    notest = module.boolean(module.params.get('notest', False))
    locallib = module.params['locallib']
    mirror = module.params['mirror']
    mirror_only = module.params['mirror_only']
    installdeps = module.params['installdeps']
    use_sudo = module.params['system_lib']
    version = module.params['version']

    changed = False

    installed = _is_package_installed(module, name, locallib, cpanm, version)

    if not installed:
        cmd = _build_cmd_line(name, from_path, notest, locallib, mirror, mirror_only, installdeps, cpanm, use_sudo)

        rc_cpanm, out_cpanm, err_cpanm = module.run_command(cmd, check_rc=False)

        if rc_cpanm != 0:
            module.fail_json(msg=err_cpanm, cmd=cmd)

        if (err_cpanm.find('is up to date') == -1 and out_cpanm.find('is up to date') == -1):
            changed = True

    module.exit_json(changed=changed, binary=cpanm, name=name)


if __name__ == '__main__':
    main()
