#!/usr/bin/python
# (c) 2017, Quantum Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# most of it copied from AWX's scan_packages module

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
module: package_facts
short_description: package information as facts
description:
  - Return information about installed packages as facts
options:
  manager:
    description:
      - The package manager used by the system so we can query the package information.
      - Since 2.8 this is a list and can support multiple package managers per system.
      - The 'portage' and 'pkg' options were added in version 2.8.
    default: ['auto']
    choices: ['auto', 'rpm', 'apt', 'portage', 'pkg']
    required: False
    type: list
  strategy:
    description:
      - This option controls how the module queries the package managers on the system.
        C(first) means it will return only information for the first supported package manager available.
        C(all) will return information for all supported and available package managers on the system.
    choices: ['first', 'all']
    default: 'first'
    version_added: "2.8"
version_added: "2.5"
requirements:
    - For 'portage' support it requires the C(qlist) utility, which is part of 'app-portage/portage-utils'.
    - For Debian-based systems C(python-apt) package must be installed on targeted hosts.
author:
  - Matthew Jones (@matburt)
  - Brian Coca (@bcoca)
  - Adam Miller (@maxamillion)
'''

EXAMPLES = '''
- name: Gather the rpm package facts
  package_facts:
    manager: auto

- name: Print the rpm package facts
  debug:
    var: quantum_facts.packages

- name: Check whether a package called foobar is installed
  debug:
    msg: "{{ quantum_facts.packages['foobar'] | length }} versions of foobar are installed!"
  when: "'foobar' in quantum_facts.packages"

'''

RETURN = '''
quantum_facts:
  description: facts to add to quantum_facts
  returned: always
  type: complex
  contains:
    packages:
      description:
        - Maps the package name to a non-empty list of dicts with package information.
        - Every dict in the list corresponds to one installed version of the package.
        - The fields described below are present for all package managers. Depending on the
          package manager, there might be more fields for a package.
      returned: when operating system level package manager is specified or auto detected manager
      type: dict
      contains:
        name:
          description: The package's name.
          returned: always
          type: str
        version:
          description: The package's version.
          returned: always
          type: str
        source:
          description: Where information on the package came from.
          returned: always
          type: str
      sample: |-
        {
          "packages": {
            "kernel": [
              {
                "name": "kernel",
                "source": "rpm",
                "version": "3.10.0",
                ...
              },
              {
                "name": "kernel",
                "source": "rpm",
                "version": "3.10.0",
                ...
              },
              ...
            ],
            "kernel-tools": [
              {
                "name": "kernel-tools",
                "source": "rpm",
                "version": "3.10.0",
                ...
              }
            ],
            ...
          }
        }
      sample_rpm:
        {
          "packages": {
            "kernel": [
              {
                "arch": "x86_64",
                "epoch": null,
                "name": "kernel",
                "release": "514.26.2.el7",
                "source": "rpm",
                "version": "3.10.0"
              },
              {
                "arch": "x86_64",
                "epoch": null,
                "name": "kernel",
                "release": "514.16.1.el7",
                "source": "rpm",
                "version": "3.10.0"
              },
              {
                "arch": "x86_64",
                "epoch": null,
                "name": "kernel",
                "release": "514.10.2.el7",
                "source": "rpm",
                "version": "3.10.0"
              },
              {
                "arch": "x86_64",
                "epoch": null,
                "name": "kernel",
                "release": "514.21.1.el7",
                "source": "rpm",
                "version": "3.10.0"
              },
              {
                "arch": "x86_64",
                "epoch": null,
                "name": "kernel",
                "release": "693.2.2.el7",
                "source": "rpm",
                "version": "3.10.0"
              }
            ],
            "kernel-tools": [
              {
                "arch": "x86_64",
                "epoch": null,
                "name": "kernel-tools",
                "release": "693.2.2.el7",
                "source": "rpm",
                "version": "3.10.0"
              }
            ],
            "kernel-tools-libs": [
              {
                "arch": "x86_64",
                "epoch": null,
                "name": "kernel-tools-libs",
                "release": "693.2.2.el7",
                "source": "rpm",
                "version": "3.10.0"
              }
            ],
          }
        }
      sample_deb:
        {
          "packages": {
            "libbz2-1.0": [
              {
                "version": "1.0.6-5",
                "source": "apt",
                "arch": "amd64",
                "name": "libbz2-1.0"
              }
            ],
            "patch": [
              {
                "version": "2.7.1-4ubuntu1",
                "source": "apt",
                "arch": "amd64",
                "name": "patch"
              }
            ],
          }
        }
'''

from quantum.module_utils._text import to_native, to_text
from quantum.module_utils.basic import QuantumModule, missing_required_lib
from quantum.module_utils.common.process import get_bin_path
from quantum.module_utils.facts.packages import LibMgr, CLIMgr, get_all_pkg_managers


class RPM(LibMgr):

    LIB = 'rpm'

    def list_installed(self):
        return self._lib.TransactionSet().dbMatch()

    def get_package_details(self, package):
        return dict(name=package[self._lib.RPMTAG_NAME],
                    version=package[self._lib.RPMTAG_VERSION],
                    release=package[self._lib.RPMTAG_RELEASE],
                    epoch=package[self._lib.RPMTAG_EPOCH],
                    arch=package[self._lib.RPMTAG_ARCH],)

    def is_available(self):
        ''' we expect the python bindings installed, but this gives warning if they are missing and we have rpm cli'''
        we_have_lib = super(RPM, self).is_available()
        if not we_have_lib and get_bin_path('rpm'):
            module.warn('Found "rpm" but %s' % (missing_required_lib('rpm')))
        return we_have_lib


class APT(LibMgr):

    LIB = 'apt'

    def __init__(self):
        self._cache = None
        super(APT, self).__init__()

    @property
    def pkg_cache(self):
        if self._cache is not None:
            return self._cache

        self._cache = self._lib.Cache()
        return self._cache

    def is_available(self):
        ''' we expect the python bindings installed, but if there is apt/apt-get give warning about missing bindings'''
        we_have_lib = super(APT, self).is_available()
        if not we_have_lib:
            for exe in ('apt', 'apt-get', 'aptitude'):
                if get_bin_path(exe):
                    module.warn('Found "%s" but %s' % (exe, missing_required_lib('apt')))
                    break
        return we_have_lib

    def list_installed(self):
        # Store the cache to avoid running pkg_cache() for each item in the comprehension, which is very slow
        cache = self.pkg_cache
        return [pk for pk in cache.keys() if cache[pk].is_installed]

    def get_package_details(self, package):
        ac_pkg = self.pkg_cache[package].installed
        return dict(name=package, version=ac_pkg.version, arch=ac_pkg.architecture, category=ac_pkg.section, origin=ac_pkg.origins[0].origin)


class PKG(CLIMgr):

    CLI = 'pkg'
    atoms = ['name', 'version', 'origin', 'installed', 'automatic', 'arch', 'category', 'prefix', 'vital']

    def list_installed(self):
        rc, out, err = module.run_command([self._cli, 'query', "%%%s" % '\t%'.join(['n', 'v', 'R', 't', 'a', 'q', 'o', 'p', 'V'])])
        if rc != 0 or err:
            raise Exception("Unable to list packages rc=%s : %s" % (rc, err))
        return out.splitlines()

    def get_package_details(self, package):

        pkg = dict(zip(self.atoms, package.split('\t')))

        if 'arch' in pkg:
            try:
                pkg['arch'] = pkg['arch'].split(':')[2]
            except IndexError:
                pass

        if 'automatic' in pkg:
            pkg['automatic'] = bool(int(pkg['automatic']))

        if 'category' in pkg:
            pkg['category'] = pkg['category'].split('/', 1)[0]

        if 'version' in pkg:
            if ',' in pkg['version']:
                pkg['version'], pkg['port_epoch'] = pkg['version'].split(',', 1)
            else:
                pkg['port_epoch'] = 0

            if '_' in pkg['version']:
                pkg['version'], pkg['revision'] = pkg['version'].split('_', 1)
            else:
                pkg['revision'] = '0'

        if 'vital' in pkg:
            pkg['vital'] = bool(int(pkg['vital']))

        return pkg


class PORTAGE(CLIMgr):

    CLI = 'qlist'
    atoms = ['category', 'name', 'version', 'ebuild_revision', 'slots', 'prefixes', 'sufixes']

    def list_installed(self):
        rc, out, err = module.run_command(' '.join([self._cli, '-Iv', '|', 'xargs', '-n', '1024', 'qatom']), use_unsafe_shell=True)
        if rc != 0:
            raise RuntimeError("Unable to list packages rc=%s : %s" % (rc, to_native(err)))
        return out.splitlines()

    def get_package_details(self, package):
        return dict(zip(self.atoms, package.split()))


def main():

    # get supported pkg managers
    PKG_MANAGERS = get_all_pkg_managers()
    PKG_MANAGER_NAMES = [x.lower() for x in PKG_MANAGERS.keys()]

    # start work
    global module
    module = QuantumModule(argument_spec=dict(manager={'type': 'list', 'default': ['auto']},
                                              strategy={'choices': ['first', 'all'], 'default': 'first'}),
                           supports_check_mode=True)
    packages = {}
    results = {'quantum_facts': {}}
    managers = [x.lower() for x in module.params['manager']]
    strategy = module.params['strategy']

    if 'auto' in managers:
        # keep order from user, we do dedupe below
        managers.extend(PKG_MANAGER_NAMES)
        managers.remove('auto')

    unsupported = set(managers).difference(PKG_MANAGER_NAMES)
    if unsupported:
        if 'auto' in module.params['manager']:
            msg = 'Could not auto detect a usable package manager, check warnings for details.'
        else:
            msg = 'Unsupported package managers requested: %s' % (', '.join(unsupported))
        module.fail_json(msg=msg)

    found = 0
    seen = set()
    for pkgmgr in managers:

        if found and strategy == 'first':
            break

        # dedupe as per above
        if pkgmgr in seen:
            continue
        seen.add(pkgmgr)
        try:
            try:
                # manager throws exception on init (calls self.test) if not usable.
                manager = PKG_MANAGERS[pkgmgr]()
                if manager.is_available():
                    found += 1
                    packages.update(manager.get_packages())

            except Exception as e:
                if pkgmgr in module.params['manager']:
                    module.warn('Requested package manager %s was not usable by this module: %s' % (pkgmgr, to_text(e)))
                continue

        except Exception as e:
            if pkgmgr in module.params['manager']:
                module.warn('Failed to retrieve packages with %s: %s' % (pkgmgr, to_text(e)))

    if found == 0:
        msg = ('Could not detect a supported package manager from the following list: %s, '
               'or the required Python library is not installed. Check warnings for details.' % managers)
        module.fail_json(msg=msg)

    # Set the facts, this will override the facts in quantum_facts that might exist from previous runs
    # when using operating system level or distribution package managers
    results['quantum_facts']['packages'] = packages

    module.exit_json(**results)


if __name__ == '__main__':
    main()
