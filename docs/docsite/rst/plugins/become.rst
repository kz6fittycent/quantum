.. _become_plugins:

Become Plugins
==============

.. contents::
   :local:
   :depth: 2

.. versionadded:: 2.8

Become plugins work to ensure that Quantum can use certain privilege escalation systems when running the basic
commands to work with the target machine as well as the modules required to execute the tasks specified in
the play.

These utilities (``sudo``, ``su``, ``doas``, etc) generally let you 'become' another user to execute a command
with the permissions of that user.


.. _enabling_become:

Enabling Become Plugins
-----------------------

The become plugins shipped with Quantum are already enabled. Custom plugins can be added by placing
them into a ``become_plugins`` directory adjacent to your play, inside a role, or by placing them in one of
the become plugin directory sources configured in :ref:`quantum.cfg <quantum_configuration_settings>`.


.. _using_become:

Using Become Plugins
--------------------

In addition to the default configuration settings in :ref:`quantum_configuration_settings` or the
``--become-method`` command line option, you can use the ``become_method`` keyword in a play or, if you need
to be 'host specific', the connection variable ``quantum_become_method`` to select the plugin to use.

You can further control the settings for each plugin via other configuration options detailed in the plugin
themselves (linked below).

.. _become_plugin_list:

Plugin List
-----------

You can use ``quantum-doc -t become -l`` to see the list of available plugins.
Use ``quantum-doc -t become <plugin name>`` to see specific documentation and examples.

.. toctree:: :maxdepth: 1
    :glob:

    become/*

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
