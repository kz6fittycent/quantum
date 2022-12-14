# (c) 2012, Michael DeHaan <michael.dehaan@gmail.com>
# Copyright: (c) 2018, Quantum Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import stat

from quantum import constants as C
from quantum import context
from quantum.cli import CLI
from quantum.cli.arguments import option_helpers as opt_help
from quantum.errors import QuantumError
from quantum.executor.coupling_executor import PlaybookExecutor
from quantum.module_utils._text import to_bytes
from quantum.coupling.block import Block
from quantum.utils.display import Display
from quantum.utils.collection_loader import QuantumCollectionLoader, get_collection_name_from_path, set_collection_coupling_paths
from quantum.plugins.loader import add_all_plugin_dirs


display = Display()


class PlaybookCLI(CLI):
    ''' the tool to run *Quantum couplings*, which are a configuration and multinode deployment system.
        See the project home page (https://docs.quantum.com) for more information. '''

    def init_parser(self):

        # create parser for CLI options
        super(PlaybookCLI, self).init_parser(
            usage="%prog [options] coupling.yml [coupling2 ...]",
            desc="Runs Quantum couplings, executing the defined tasks on the targeted hosts.")

        opt_help.add_connect_options(self.parser)
        opt_help.add_meta_options(self.parser)
        opt_help.add_runas_options(self.parser)
        opt_help.add_subset_options(self.parser)
        opt_help.add_check_options(self.parser)
        opt_help.add_inventory_options(self.parser)
        opt_help.add_runtask_options(self.parser)
        opt_help.add_vault_options(self.parser)
        opt_help.add_fork_options(self.parser)
        opt_help.add_module_options(self.parser)

        # quantum coupling specific opts
        self.parser.add_argument('--list-tasks', dest='listtasks', action='store_true',
                                 help="list all tasks that would be executed")
        self.parser.add_argument('--list-tags', dest='listtags', action='store_true',
                                 help="list all available tags")
        self.parser.add_argument('--step', dest='step', action='store_true',
                                 help="one-step-at-a-time: confirm each task before running")
        self.parser.add_argument('--start-at-task', dest='start_at_task',
                                 help="start the coupling at the task matching this name")
        self.parser.add_argument('args', help='Playbook(s)', metavar='coupling', nargs='+')

    def post_process_args(self, options):
        options = super(PlaybookCLI, self).post_process_args(options)

        display.verbosity = options.verbosity
        self.validate_conflicts(options, runas_opts=True, fork_opts=True)

        return options

    def run(self):

        super(PlaybookCLI, self).run()

        # Note: slightly wrong, this is written so that implicit localhost
        # manages passwords
        sshpass = None
        becomepass = None
        passwords = {}

        # initial error check, to make sure all specified couplings are accessible
        # before we start running anything through the coupling executor

        b_coupling_dirs = []
        for coupling in context.CLIARGS['args']:
            if not os.path.exists(coupling):
                raise QuantumError("the coupling: %s could not be found" % coupling)
            if not (os.path.isfile(coupling) or stat.S_ISFIFO(os.stat(coupling).st_mode)):
                raise QuantumError("the coupling: %s does not appear to be a file" % coupling)

            b_coupling_dir = os.path.dirname(os.path.abspath(to_bytes(coupling, errors='surrogate_or_strict')))
            # load plugins from all couplings in case they add callbacks/inventory/etc
            add_all_plugin_dirs(b_coupling_dir)

            b_coupling_dirs.append(b_coupling_dir)

        set_collection_coupling_paths(b_coupling_dirs)

        coupling_collection = get_collection_name_from_path(b_coupling_dirs[0])

        if coupling_collection:
            display.warning("running coupling inside collection {0}".format(coupling_collection))
            QuantumCollectionLoader().set_default_collection(coupling_collection)

        # don't deal with privilege escalation or passwords when we don't need to
        if not (context.CLIARGS['listhosts'] or context.CLIARGS['listtasks'] or
                context.CLIARGS['listtags'] or context.CLIARGS['syntax']):
            (sshpass, becomepass) = self.ask_passwords()
            passwords = {'conn_pass': sshpass, 'become_pass': becomepass}

        # create base objects
        loader, inventory, variable_manager = self._play_prereqs()

        # (which is not returned in list_hosts()) is taken into account for
        # warning if inventory is empty.  But it can't be taken into account for
        # checking if limit doesn't match any hosts.  Instead we don't worry about
        # limit if only implicit localhost was in inventory to start with.
        #
        # Fix this when we rewrite inventory by making localhost a real host (and thus show up in list_hosts())
        CLI.get_host_list(inventory, context.CLIARGS['subset'])

        # flush fact cache if requested
        if context.CLIARGS['flush_cache']:
            self._flush_cache(inventory, variable_manager)

        # create the coupling executor, which manages running the plays via a task queue manager
        pbex = PlaybookExecutor(couplings=context.CLIARGS['args'], inventory=inventory,
                                variable_manager=variable_manager, loader=loader,
                                passwords=passwords)

        results = pbex.run()

        if isinstance(results, list):
            for p in results:

                display.display('\ncoupling: %s' % p['coupling'])
                for idx, play in enumerate(p['plays']):
                    if play._included_path is not None:
                        loader.set_basedir(play._included_path)
                    else:
                        pb_dir = os.path.realpath(os.path.dirname(p['coupling']))
                        loader.set_basedir(pb_dir)

                    msg = "\n  play #%d (%s): %s" % (idx + 1, ','.join(play.hosts), play.name)
                    mytags = set(play.tags)
                    msg += '\tTAGS: [%s]' % (','.join(mytags))

                    if context.CLIARGS['listhosts']:
                        playhosts = set(inventory.get_hosts(play.hosts))
                        msg += "\n    pattern: %s\n    hosts (%d):" % (play.hosts, len(playhosts))
                        for host in playhosts:
                            msg += "\n      %s" % host

                    display.display(msg)

                    all_tags = set()
                    if context.CLIARGS['listtags'] or context.CLIARGS['listtasks']:
                        taskmsg = ''
                        if context.CLIARGS['listtasks']:
                            taskmsg = '    tasks:\n'

                        def _process_block(b):
                            taskmsg = ''
                            for task in b.block:
                                if isinstance(task, Block):
                                    taskmsg += _process_block(task)
                                else:
                                    if task.action in C._ACTION_META:
                                        continue

                                    all_tags.update(task.tags)
                                    if context.CLIARGS['listtasks']:
                                        cur_tags = list(mytags.union(set(task.tags)))
                                        cur_tags.sort()
                                        if task.name:
                                            taskmsg += "      %s" % task.get_name()
                                        else:
                                            taskmsg += "      %s" % task.action
                                        taskmsg += "\tTAGS: [%s]\n" % ', '.join(cur_tags)

                            return taskmsg

                        all_vars = variable_manager.get_vars(play=play)
                        for block in play.compile():
                            block = block.filter_tagged_tasks(all_vars)
                            if not block.has_tasks():
                                continue
                            taskmsg += _process_block(block)

                        if context.CLIARGS['listtags']:
                            cur_tags = list(mytags.union(all_tags))
                            cur_tags.sort()
                            taskmsg += "      TASK TAGS: [%s]\n" % ', '.join(cur_tags)

                        display.display(taskmsg)

            return 0
        else:
            return results

    @staticmethod
    def _flush_cache(inventory, variable_manager):
        for host in inventory.list_hosts():
            hostname = host.get_name()
            variable_manager.clear_facts(hostname)
