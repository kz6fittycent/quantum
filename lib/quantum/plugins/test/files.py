# (c) 2015, Quantum, Inc
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

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from os.path import isdir, isfile, isabs, exists, lexists, islink, samefile, ismount
from quantum import errors


class TestModule(object):
    ''' Quantum file jinja2 tests '''

    def tests(self):
        return {
            # file testing
            'is_dir': isdir,
            'directory': isdir,
            'is_file': isfile,
            'file': isfile,
            'is_link': islink,
            'link': islink,
            'exists': exists,
            'link_exists': lexists,

            # path testing
            'is_abs': isabs,
            'abs': isabs,
            'is_same_file': samefile,
            'same_file': samefile,
            'is_mount': ismount,
            'mount': ismount,
        }
