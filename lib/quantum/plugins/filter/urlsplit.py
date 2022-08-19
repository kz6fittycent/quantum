# Copyright (c) 2017 Quantum Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}


from quantum.errors import QuantumFilterError
from quantum.module_utils.six.moves.urllib.parse import urlsplit
from quantum.utils import helpers


def split_url(value, query='', alias='urlsplit'):

    results = helpers.object_to_dict(urlsplit(value), exclude=['count', 'index', 'geturl', 'encode'])

    # If a query is supplied, make sure it's valid then return the results.
    # If no option is supplied, return the entire dictionary.
    if query:
        if query not in results:
            raise QuantumFilterError(alias + ': unknown URL component: %s' % query)
        return results[query]
    else:
        return results


# ---- Quantum filters ----
class FilterModule(object):
    ''' URI filter '''

    def filters(self):
        return {
            'urlsplit': split_url
        }
