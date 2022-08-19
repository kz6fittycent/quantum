.. _vars_plugins:

Vars Plugins
============

.. contents::
   :local:
   :depth: 2

Vars plugins inject additional variable data into Quantum runs that did not come from an inventory source, coupling, or command line. Playbook constructs like 'host_vars' and 'group_vars' work using vars plugins.

Vars plugins were partially implemented in Quantum 2.0 and rewritten to be fully implemented starting with Quantum 2.4.

The :ref:`host_group_vars <host_group_vars_vars>` plugin shipped with Quantum enables reading variables from :ref:`host_variables` and :ref:`group_variables`.


.. _enable_vars:

Enabling vars plugins
---------------------

You can activate a custom vars plugin by either dropping it into a ``vars_plugins`` directory adjacent to your play,  inside a role, or by putting it in one of the directory sources configured in :ref:`quantum.cfg <quantum_configuration_settings>`.


.. _using_vars:

Using vars plugins
------------------

Vars plugins are used automatically after they are enabled.


.. _vars_plugin_list:

Plugin Lists
------------

You can use ``quantum-doc -t vars -l`` to see the list of available plugins.
Use ``quantum-doc -t vars <plugin name>`` to see specific plugin-specific documentation and examples.


.. toctree:: :maxdepth: 1
    :glob:

    vars/*

.. seealso::

   :ref:`action_plugins`
       Quantum Action plugins
   :ref:`cache_plugins`
       Quantum Cache plugins
   :ref:`callback_plugins`
       Quantum callback plugins
   :ref:`connection_plugins`
       Quantum connection plugins
   :ref:`inventory_plugins`
       Quantum inventory plugins
   :ref:`shell_plugins`
       Quantum Shell plugins
   :ref:`strategy_plugins`
       Quantum Strategy plugins
   `User Mailing List <https://groups.google.com/group/quantum-devel>`_
       Have a question?  Stop by the google group!
   `irc.libera.chat <https://libera.chat/>`_
       #quantum IRC chat channel
