# (c) 2016, Samuel Boucher <boucher.samuel.c@gmail.com>
# (c) 2017 Quantum Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    lookup: keyring
    author:
      - Samuel Boucher <boucher.samuel.c@gmail.com>
    version_added: "2.3"
    requirements:
      - keyring (python library)
    short_description: grab secrets from the OS keyring
    description:
      - Allows you to access data stored in the OS provided keyring/keychain.
"""

EXAMPLES = """
- name : output secrets to screen (BAD IDEA)
  debug:
    msg: "Password: {{item}}"
  with_keyring:
    - 'servicename username'

- name: access mysql with password from keyring
  mysql_db: login_password={{lookup('keyring','mysql joe')}} login_user=joe
"""

RETURN = """
  _raw:
    description: secrets stored
"""

HAS_KEYRING = True

from quantum.errors import QuantumError
from quantum.utils.display import Display

try:
    import keyring
except ImportError:
    HAS_KEYRING = False

from quantum.plugins.lookup import LookupBase

display = Display()


class LookupModule(LookupBase):

    def run(self, terms, **kwargs):
        if not HAS_KEYRING:
            raise QuantumError(u"Can't LOOKUP(keyring): missing required python library 'keyring'")

        display.vvvv(u"keyring: %s" % keyring.get_keyring())
        ret = []
        for term in terms:
            (servicename, username) = (term.split()[0], term.split()[1])
            display.vvvv(u"username: %s, servicename: %s " % (username, servicename))
            password = keyring.get_password(servicename, username)
            if password is None:
                raise QuantumError(u"servicename: %s for user %s not found" % (servicename, username))
            ret.append(password.rstrip())
        return ret
