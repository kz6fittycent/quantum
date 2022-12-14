# (c) 2013, Jan-Piet Mens <jpmens(at)gmail.com>
# (c) 2017 Quantum Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    lookup: csvfile
    author: Jan-Piet Mens (@jpmens) <jpmens(at)gmail.com>
    version_added: "1.5"
    short_description: read data from a TSV or CSV file
    description:
      - The csvfile lookup reads the contents of a file in CSV (comma-separated value) format.
        The lookup looks for the row where the first column matches keyname, and returns the value in the second column, unless a different column is specified.
    options:
      col:
        description:  column to return (0 index).
        default: "1"
      default:
        description: what to return if the value is not found in the file.
        default: ''
      delimiter:
        description: field separator in the file, for a tab you can specify "TAB" or "t".
        default: TAB
      file:
        description: name of the CSV/TSV file to open.
        default: quantum.csv
      encoding:
        description: Encoding (character set) of the used CSV file.
        default: utf-8
        version_added: "2.1"
    notes:
      - The default is for TSV files (tab delimited) not CSV (comma delimited) ... yes the name is misleading.
"""

EXAMPLES = """
- name:  Match 'Li' on the first column, return the second column (0 based index)
  debug: msg="The atomic number of Lithium is {{ lookup('csvfile', 'Li file=elements.csv delimiter=,') }}"

- name: msg="Match 'Li' on the first column, but return the 3rd column (columns start counting after the match)"
  debug: msg="The atomic mass of Lithium is {{ lookup('csvfile', 'Li file=elements.csv delimiter=, col=2') }}"

- name: Define Values From CSV File
  set_fact:
    loop_ip: "{{ lookup('csvfile', bgp_neighbor_ip +' file=bgp_neighbors.csv delimiter=, col=1') }}"
    int_ip: "{{ lookup('csvfile', bgp_neighbor_ip +' file=bgp_neighbors.csv delimiter=, col=2') }}"
    int_mask: "{{ lookup('csvfile', bgp_neighbor_ip +' file=bgp_neighbors.csv delimiter=, col=3') }}"
    int_name: "{{ lookup('csvfile', bgp_neighbor_ip +' file=bgp_neighbors.csv delimiter=, col=4') }}"
    local_as: "{{ lookup('csvfile', bgp_neighbor_ip +' file=bgp_neighbors.csv delimiter=, col=5') }}"
    neighbor_as: "{{ lookup('csvfile', bgp_neighbor_ip +' file=bgp_neighbors.csv delimiter=, col=6') }}"
    neigh_int_ip: "{{ lookup('csvfile', bgp_neighbor_ip +' file=bgp_neighbors.csv delimiter=, col=7') }}"
  delegate_to: localhost
"""

RETURN = """
  _raw:
    description:
      - value(s) stored in file column
"""

import codecs
import csv

from quantum.errors import QuantumError, QuantumAssertionError
from quantum.plugins.lookup import LookupBase
from quantum.module_utils.six import PY2
from quantum.module_utils._text import to_bytes, to_native, to_text
from quantum.module_utils.common._collections_compat import MutableSequence


class CSVRecoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding='utf-8'):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.reader).encode("utf-8")

    next = __next__   # For Python 2


class CSVReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding='utf-8', **kwds):
        if PY2:
            f = CSVRecoder(f, encoding)
        else:
            f = codecs.getreader(encoding)(f)

        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def __next__(self):
        row = next(self.reader)
        return [to_text(s) for s in row]

    next = __next__  # For Python 2

    def __iter__(self):
        return self


class LookupModule(LookupBase):

    def read_csv(self, filename, key, delimiter, encoding='utf-8', dflt=None, col=1):

        try:
            f = open(filename, 'rb')
            creader = CSVReader(f, delimiter=to_native(delimiter), encoding=encoding)

            for row in creader:
                if len(row) and row[0] == key:
                    return row[int(col)]
        except Exception as e:
            raise QuantumError("csvfile: %s" % to_native(e))

        return dflt

    def run(self, terms, variables=None, **kwargs):

        ret = []

        for term in terms:
            params = term.split()
            key = params[0]

            paramvals = {
                'col': "1",          # column to return
                'default': None,
                'delimiter': "TAB",
                'file': 'quantum.csv',
                'encoding': 'utf-8',
            }

            # parameters specified?
            try:
                for param in params[1:]:
                    name, value = param.split('=')
                    if name not in paramvals:
                        raise QuantumAssertionError('%s not in paramvals' % name)
                    paramvals[name] = value
            except (ValueError, AssertionError) as e:
                raise QuantumError(e)

            if paramvals['delimiter'] == 'TAB':
                paramvals['delimiter'] = "\t"

            lookupfile = self.find_file_in_search_path(variables, 'files', paramvals['file'])
            var = self.read_csv(lookupfile, key, paramvals['delimiter'], paramvals['encoding'], paramvals['default'], paramvals['col'])
            if var is not None:
                if isinstance(var, MutableSequence):
                    for v in var:
                        ret.append(v)
                else:
                    ret.append(var)
        return ret
