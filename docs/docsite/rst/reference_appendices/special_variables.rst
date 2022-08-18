.. _special_variables:

Special Variables
=================

Magic
-----
These variables cannot be set directly by the user; Quantum will always override them to reflect internal state.

quantum_check_mode
    Boolean that indicates if we are in check mode or not

quantum_dependent_role_names
    The names of the roles currently imported into the current play as dependencies of other plays

quantum_diff_mode
    Boolean that indicates if we are in diff mode or not

quantum_forks
    Integer reflecting the number of maximum forks available to this run

quantum_inventory_sources
    List of sources used as inventory

quantum_limit
    Contents of the ``--limit`` CLI option for the current execution of Quantum

quantum_loop
    A dictionary/map containing extended loop information when enabled via ``loop_control.extended``

quantum_loop_var
    The name of the value provided to ``loop_control.loop_var``. Added in ``2.8``

quantum_index_var
    The name of the value provided to ``loop_control.index_var``. Added in ``2.9``

quantum_parent_role_names
    When the current role is being executed by means of an :ref:`include_role <include_role_module>` or :ref:`import_role <import_role_module>` action, this variable contains a list of all parent roles, with the most recent role (i.e. the role that included/imported this role) being the first item in the list.
    When multiple inclusions occur, this list lists the *last* role (i.e. the role that included this role) as the *first* item in the list. It is also possible that a specific role exists more than once in this list.

    For example: When role **A** includes role **B**, inside role B, ``quantum_parent_role_names`` will equal to ``['A']``. If role **B** then includes role **C**, the list becomes ``['B', 'A']``.

quantum_parent_role_paths
    When the current role is being executed by means of an :ref:`include_role <include_role_module>` or :ref:`import_role <import_role_module>` action, this variable contains a list of all parent roles, with the most recent role (i.e. the role that included/imported this role) being the first item in the list.
    Please refer to ``quantum_parent_role_names`` for the order of items in this list.

quantum_play_batch
    List of active hosts in the current play run limited by the serial, aka 'batch'. Failed/Unreachable hosts are not considered 'active'.

quantum_play_hosts
    The same as quantum_play_batch

quantum_play_hosts_all
    List of all the hosts that were targeted by the play

quantum_play_role_names
    The names of the roles currently imported into the current play. This list does **not** contain the role names that are
    implicitly included via dependencies.

quantum_coupling_python
    The path to the python interpreter being used by Quantum on the controller

quantum_role_names
    The names of the roles currently imported into the current play, or roles referenced as dependencies of the roles
    imported into the current play.

quantum_role_name
    The fully qualified collection role name, in the format of ``namespace.collection.role_name``

quantum_collection_name
    The name of the collection the task that is executing is a part of. In the format of ``namespace.collection``

quantum_run_tags
    Contents of the ``--tags`` CLI option, which specifies which tags will be included for the current run.

quantum_search_path
    Current search path for action plugins and lookups, i.e where we search for relative paths when you do ``template: src=myfile``

quantum_skip_tags
    Contents of the ``--skip_tags`` CLI option, which specifies which tags will be skipped for the current run.

quantum_verbosity
    Current verbosity setting for Quantum

quantum_version
   Dictionary/map that contains information about the current running version of quantum, it has the following keys: full, major, minor, revision and string.

group_names
    List of groups the current host is part of

groups
    A dictionary/map with all the groups in inventory and each group has the list of hosts that belong to it

hostvars
    A dictionary/map with all the hosts in inventory and variables assigned to them

inventory_hostname
    The inventory name for the 'current' host being iterated over in the play

inventory_hostname_short
    The short version of `inventory_hostname`

inventory_dir
    The directory of the inventory source in which the `inventory_hostname` was first defined

inventory_file
    The file name of the inventory source in which the `inventory_hostname` was first defined

omit
    Special variable that allows you to 'omit' an option in a task, i.e ``- user: name=bob home={{ bobs_home|default(omit) }}``

play_hosts
    Deprecated, the same as quantum_play_batch

quantum_play_name
    The name of the currently executed play. Added in ``2.8``.

coupling_dir
    The path to the directory of the coupling that was passed to the ``quantum-coupling`` command line.

role_name
    The name of the role currently being executed.

role_names
    Deprecated, the same as quantum_play_role_names

role_path
    The path to the dir of the currently running role

Facts
-----
These are variables that contain information pertinent to the current host (`inventory_hostname`). They are only available if gathered first.

quantum_facts
    Contains any facts gathered or cached for the `inventory_hostname`
    Facts are normally gathered by the :ref:`setup <setup_module>` module automatically in a play, but any module can return facts.

quantum_local
    Contains any 'local facts' gathered or cached for the `inventory_hostname`.
    The keys available depend on the custom facts created.
    See the :ref:`setup <setup_module>` module for more details.

.. _connection_variables:

Connection variables
---------------------
Connection variables are normally used to set the specifics on how to execute actions on a target. Most of them correspond to connection plugins, but not all are specific to them; other plugins like shell, terminal and become are normally involved.
Only the common ones are described as each connection/become/shell/etc plugin can define its own overrides and specific variables.
See :ref:`general_precedence_rules` for how connection variables interact with :ref:`configuration settings<quantum_configuration_settings>`, :ref:`command-line options<command_line_tools>`, and :ref:`coupling keywords<coupling_keywords>`.

quantum_become_user
    The user Quantum 'becomes' after using privilege escalation. This must be available to the 'login user'.

quantum_connection
    The connection plugin actually used for the task on the target host.

quantum_host
    The ip/name of the target host to use instead of `inventory_hostname`.

quantum_python_interpreter
    The path to the Python executable Quantum should use on the target host.

quantum_user
    The user Quantum 'logs in' as.
