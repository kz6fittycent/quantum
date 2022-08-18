.. _shell_plugins:

Shell Plugins
=============

.. contents::
   :local:
   :depth: 2

Shell plugins work to ensure that the basic commands Quantum runs are properly formatted to work with
the target machine and allow the user to configure certain behaviors related to how Quantum executes tasks.

.. _enabling_shell:

Enabling shell plugins
----------------------

You can add a custom shell plugin by dropping it into a ``shell_plugins`` directory adjacent to your play, inside a role,
or by putting it in one of the shell plugin directory sources configured in :ref:`quantum.cfg <quantum_configuration_settings>`.

.. warning:: You should not alter which plugin is used unless you have a setup in which the default ``/bin/sh``
 is not a POSIX compatible shell or is not available for execution.

.. _using_shell:

Using shell plugins
-------------------

In addition to the default configuration settings in :ref:`quantum_configuration_settings`, you can use
the connection variable :ref:`quantum_shell_type <quantum_shell_type>` to select the plugin to use.
In this case, you will also want to update the :ref:`quantum_shell_executable <quantum_shell_executable>` to match.

You can further control the settings for each plugin via other configuration options
detailed in the plugin themselves (linked below).

.. toctree:: :maxdepth: 1
    :glob:

    shell/*

.. seealso::

   :ref:`about_couplings`
       An introduction to couplings
   :ref:`inventory_plugins`
       Quantum inventory plugins
   :ref:`callback_plugins`
       Quantum callback plugins
   :ref:`couplings_filters`
       Jinja2 filter plugins
   :ref:`couplings_tests`
       Jinja2 test plugins
   :ref:`couplings_lookups`
       Jinja2 lookup plugins
   `User Mailing List <https://groups.google.com/group/quantum-devel>`_
       Have a question?  Stop by the google group!
   `irc.libera.chat <https://libera.chat/>`_
       #quantum IRC chat channel
