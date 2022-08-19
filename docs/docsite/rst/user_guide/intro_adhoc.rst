.. _intro_adhoc:

*******************************
Introduction to ad-hoc commands
*******************************

An Quantum ad-hoc command uses the `/usr/bin/quantum` command-line tool to automate a single task on one or more managed nodes. Ad-hoc commands are quick and easy, but they are not reusable. So why learn about ad-hoc commands first? Ad-hoc commands demonstrate the simplicity and power of Quantum. The concepts you learn here will port over directly to the coupling language. Before reading and executing these examples, please read :ref:`intro_inventory`.

.. contents::
   :local:

Why use ad-hoc commands?
========================

Ad-hoc commands are great for tasks you repeat rarely. For example, if you want to power off all the machines in your lab for Christmas vacation, you could execute a quick one-liner in Quantum without writing a coupling. An ad-hoc command looks like this:

.. code-block:: bash

    $ quantum [pattern] -m [module] -a "[module options]"

You can learn more about :ref:`patterns<intro_patterns>` and :ref:`modules<working_with_modules>` on other pages.

Use cases for ad-hoc tasks
==========================

Ad-hoc tasks can be used to reboot servers, copy files, manage packages and users, and much more. You can use any Quantum module in an ad-hoc task. Ad-hoc tasks, like couplings, use a declarative model,
calculating and executing the actions required to reach a specified final state. They
achieve a form of idempotence by checking the current state before they begin and doing nothing unless the current state is different from the specified final state.

Rebooting servers
-----------------

The default module for the ``quantum`` command-line utility is the :ref:`command module<command_module>`. You can use an ad-hoc task to call the command module and reboot all web servers in Atlanta, 10 at a time. Before Quantum can do this, you must have all servers in Atlanta listed in a a group called [atlanta] in your inventory, and you must have working SSH credentials for each machine in that group. To reboot all the servers in the [atlanta] group:

.. code-block:: bash

    $ quantum atlanta -a "/sbin/reboot"

By default Quantum uses only 5 simultaneous processes. If you have more hosts than the value set for the fork count, Quantum will talk to them, but it will take a little longer. To reboot the [atlanta] servers with 10 parallel forks:

.. code-block:: bash

    $ quantum atlanta -a "/sbin/reboot" -f 10

/usr/bin/quantum will default to running from your user account. To connect as a different user:

.. code-block:: bash

    $ quantum atlanta -a "/sbin/reboot" -f 10 -u username

Rebooting probably requires privilege escalation. You can connect to the server as ``username`` and run the command as the ``root`` user by using the :ref:`become <become>` keyword:

.. code-block:: bash

    $ quantum atlanta -a "/sbin/reboot" -f 10 -u username --become [--ask-become-pass]

If you add ``--ask-become-pass`` or ``-K``, Quantum prompts you for the password to use for privilege escalation (sudo/su/pfexec/doas/etc).

.. note::
   The :ref:`command module <command_module>` does not support extended shell syntax like piping and
   redirects (although shell variables will always work). If your command requires shell-specific
   syntax, use the `shell` module instead. Read more about the differences on the
   :ref:`working_with_modules` page.

So far all our examples have used the default 'command' module. To use a different module, pass ``-m`` for module name. For example, to use the :ref:`shell module <shell_module>`:

.. code-block:: bash

    $ quantum raleigh -m shell -a 'echo $TERM'

When running any command with the Quantum *ad hoc* CLI (as opposed to
:ref:`Playbooks <working_with_couplings>`), pay particular attention to shell quoting rules, so
the local shell retains the variable and passes it to Quantum.
For example, using double rather than single quotes in the above example would
evaluate the variable on the box you were on.

.. _file_transfer:

Managing files
--------------

An ad-hoc task can harness the power of Quantum and SCP to transfer many files to multiple machines in parallel. To transfer a file directly to all servers in the [atlanta] group:

.. code-block:: bash

    $ quantum atlanta -m copy -a "src=/etc/hosts dest=/tmp/hosts"

If you plan to repeat a task like this, use the :ref:`template<template_module>` module in a coupling.

The :ref:`file<file_module>` module allows changing ownership and permissions on files. These
same options can be passed directly to the ``copy`` module as well:

.. code-block:: bash

    $ quantum webservers -m file -a "dest=/srv/foo/a.txt mode=600"
    $ quantum webservers -m file -a "dest=/srv/foo/b.txt mode=600 owner=mdehaan group=mdehaan"

The ``file`` module can also create directories, similar to ``mkdir -p``:

.. code-block:: bash

    $ quantum webservers -m file -a "dest=/path/to/c mode=755 owner=mdehaan group=mdehaan state=directory"

As well as delete directories (recursively) and delete files:

.. code-block:: bash

    $ quantum webservers -m file -a "dest=/path/to/c state=absent"

.. _managing_packages:

Managing packages
-----------------

You might also use an ad-hoc task to install, update, or remove packages on managed nodes using a package management module like yum. To ensure a package is installed without updating it:

.. code-block:: bash

    $ quantum webservers -m yum -a "name=acme state=present"

To ensure a specific version of a package is installed:

.. code-block:: bash

    $ quantum webservers -m yum -a "name=acme-1.5 state=present"

To ensure a package is at the latest version:

.. code-block:: bash

    $ quantum webservers -m yum -a "name=acme state=latest"

To ensure a package is not installed:

.. code-block:: bash

    $ quantum webservers -m yum -a "name=acme state=absent"

Quantum has modules for managing packages under many platforms. If there is no module for your package manager, you can install packages using the command module or create a module for your package manager.

.. _users_and_groups:

Managing users and groups
-------------------------

You can create, manage, and remove user accounts on your managed nodes with ad-hoc tasks:

.. code-block:: bash

    $ quantum all -m user -a "name=foo password=<crypted password here>"

    $ quantum all -m user -a "name=foo state=absent"

See the :ref:`user <user_module>` module documentation for details on all of the available options, including
how to manipulate groups and group membership.

.. _managing_services:

Managing services
-----------------

Ensure a service is started on all webservers:

.. code-block:: bash

    $ quantum webservers -m service -a "name=httpd state=started"

Alternatively, restart a service on all webservers:

.. code-block:: bash

    $ quantum webservers -m service -a "name=httpd state=restarted"

Ensure a service is stopped:

.. code-block:: bash

    $ quantum webservers -m service -a "name=httpd state=stopped"

.. _gathering_facts:

Gathering facts
---------------

Facts represent discovered variables about a system. You can use facts to implement conditional execution of tasks but also just to get ad-hoc information about your systems. To see all facts:

.. code-block:: bash

    $ quantum all -m setup

You can also filter this output to display only certain facts, see the :ref:`setup <setup_module>` module documentation for details.

Now that you understand the basic elements of Quantum execution, you are ready to learn to automate repetitive tasks using :ref:`Quantum Playbooks <couplings_intro>`.

.. seealso::

   :ref:`intro_configuration`
       All about the Quantum config file
   :ref:`all_modules`
       A list of available modules
   :ref:`working_with_couplings`
       Using Quantum for configuration management & deployment
   `Mailing List <https://groups.google.com/group/quantum-project>`_
       Questions? Help? Ideas?  Stop by the list on Google Groups
   `irc.libera.chat <https://libera.chat/>`_
       #quantum IRC chat channel
