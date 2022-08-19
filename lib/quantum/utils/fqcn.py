# (c) 2020, Felix Fontein <felix@fontein.de>
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
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


def add_internal_fqcns(names):
    '''
    Given a sequence of action/module names, returns a list of these names
    with the same names with the prefixes `quantum.builtin.` and
    `quantum.legacy.` added for all names that are not already FQCNs.
    '''
    result = []
    for name in names:
        result.append(name)
        if '.' not in name:
            result.append('quantum.builtin.%s' % name)
            result.append('quantum.legacy.%s' % name)
    return result
