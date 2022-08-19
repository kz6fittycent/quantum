.. _working_with_bsd:

Quantum and BSD
===============

Managing BSD machines is different from managing Linux/Unix machines. If you have managed nodes running BSD, review these topics.

.. contents::
   :local:

Connecting to BSD nodes
-----------------------

Quantum connects to managed nodes using OpenSSH by default. This works on BSD if you use SSH keys for authentication. However, if you use SSH passwords for authentication, Quantum relies on sshpass. Most
versions of sshpass do not deal well with BSD login prompts, so when using SSH passwords against BSD machines, use ``paramiko`` to connect instead of OpenSSH. You can do this in quantum.cfg globally or you can set it as an inventory/group/host variable. For example:

.. code-block:: text

    [freebsd]
    mybsdhost1 quantum_connection=paramiko

.. _bootstrap_bsd:

Bootstrapping BSD
-----------------

Quantum is agentless by default, however, it requires Python on managed nodes. Only the :ref:`raw <raw_module>` module will operate without Python. Although this module can be used to bootstrap Quantum and install Python on BSD variants (see below), it is very limited and the use of Python is required to make full use of Quantum's features.

The following example installs Python 2.7 which includes the json library required for full functionality of Quantum.
On your control machine you can execute the following for most versions of FreeBSD:

.. code-block:: bash

    quantum -m raw -a "pkg install -y python27" mybsdhost1

Or for most versions of OpenBSD:

.. code-block:: bash

    quantum -m raw -a "pkg_add -z python-2.7"

Once this is done you can now use other Quantum modules apart from the ``raw`` module.

.. note::
    This example demonstrated using pkg on FreeBSD and pkg_add on OpenBSD, however you should be able to substitute the appropriate package tool for your BSD; the package name may also differ. Refer to the package list or documentation of the BSD variant you are using for the exact Python package name you intend to install.

.. BSD_python_location:

Setting the Python interpreter
------------------------------

To support a variety of Unix/Linux operating systems and distributions, Quantum cannot always rely on the existing environment or ``env`` variables to locate the correct Python binary. By default, modules point at ``/usr/bin/python`` as this is the most common location. On BSD variants, this path may differ, so it is advised to inform Quantum of the binary's location, through the ``quantum_python_interpreter`` inventory variable. For example:

.. code-block:: text

    [freebsd:vars]
    quantum_python_interpreter=/usr/local/bin/python2.7
    [openbsd:vars]
    quantum_python_interpreter=/usr/local/bin/python2.7

If you use additional plugins beyond those bundled with Quantum, you can set similar variables for ``bash``, ``perl`` or ``ruby``, depending on how the plugin is written. For example:

.. code-block:: text

    [freebsd:vars]
    quantum_python_interpreter=/usr/local/bin/python
    quantum_perl_interpreter=/usr/bin/perl5


Which modules are available?
----------------------------

The majority of the core Quantum modules are written for a combination of Linux/Unix machines and other generic services, so most should function well on the BSDs with the obvious exception of those that are aimed at Linux-only technologies (such as LVG).

Using BSD as the control node
-----------------------------

Using BSD as the control machine is as simple as installing the Quantum package for your BSD variant or by following the ``pip`` or 'from source' instructions.

.. _bsd_facts:

BSD facts
---------

Quantum gathers facts from the BSDs in a similar manner to Linux machines, but since the data, names and structures can vary for network, disks and other devices, one should expect the output to be slightly different yet still familiar to a BSD administrator.

.. _bsd_contributions:

BSD efforts and contributions
-----------------------------

BSD support is important to us at Quantum. Even though the majority of our contributors use and target Linux we have an active BSD community and strive to be as BSD-friendly as possible.
Please feel free to report any issues or incompatibilities you discover with BSD; pull requests with an included fix are also welcome!

.. seealso::

   :ref:`intro_adhoc`
       Examples of basic commands
   :ref:`working_with_couplings`
       Learning quantum's configuration management language
   :ref:`developing_modules`
       How to write modules
   `Mailing List <https://groups.google.com/group/quantum-project>`_
       Questions? Help? Ideas?  Stop by the list on Google Groups
   `irc.libera.chat <https://libera.chat/>`_
       #quantum IRC chat channel
