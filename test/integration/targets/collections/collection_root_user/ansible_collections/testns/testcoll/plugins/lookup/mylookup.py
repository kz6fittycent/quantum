from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from quantum.plugins.lookup import LookupBase


class LookupModule(LookupBase):

    def run(self, terms, variables, **kwargs):

        return ['mylookup_from_user_dir']
