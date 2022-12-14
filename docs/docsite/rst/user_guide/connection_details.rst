.. _connections:

******************************
Connection methods and details
******************************

This section shows you how to expand and refine the connection methods Quantum uses for your inventory.

ControlPersist and paramiko
---------------------------

By default, Quantum uses native OpenSSH, because it supports ControlPersist (a performance feature), Kerberos, and options in ``~/.ssh/config`` such as Jump Host setup. If your control machine uses an older version of OpenSSH that does not support ControlPersist, Quantum will fallback to a Python implementation of OpenSSH called 'paramiko'.

SSH key setup
-------------

By default, Quantum assumes you are using SSH keys to connect to remote machines.  SSH keys are encouraged, but you can use password authentication if needed with the ``--ask-pass`` option. If you need to provide a password for :ref:`privilege escalation <become>` (sudo, pbrun, etc.), use ``--ask-become-pass``.

.. include:: shared_snippets/SSH_password_prompt.txt

To set up SSH agent to avoid retyping passwords, you can do:

.. code-block:: bash

   $ ssh-agent bash
   $ ssh-add ~/.ssh/id_rsa

Depending on your setup, you may wish to use Quantum's ``--private-key`` command line option to specify a pem file instead.  You can also add the private key file:

.. code-block:: bash

   $ ssh-agent bash
   $ ssh-add ~/.ssh/keypair.pem

Another way to add private key files without using ssh-agent is using ``quantum_ssh_private_key_file`` in an inventory file as explained here:  :ref:`intro_inventory`.

Running against localhost
-------------------------

You can run commands against the control node by using "localhost" or "127.0.0.1" for the server name:

.. code-block:: bash

    $ quantum localhost -m ping -e 'quantum_python_interpreter="/usr/bin/env python"'

You can specify localhost explicitly by adding this to your inventory file:

.. code-block:: bash

    localhost quantum_connection=local quantum_python_interpreter="/usr/bin/env python"

.. _host_key_checking_on:

Host key checking
-----------------

Quantum enables host key checking by default. Checking host keys guards against server spoofing and man-in-the-middle attacks, but it does require some maintenance.

If a host is reinstalled and has a different key in 'known_hosts', this will result in an error message until corrected.  If a new host is not in 'known_hosts' your control node may prompt for confirmation of the key, which results in an interactive experience if using Quantum, from say, cron. You might not want this.

If you understand the implications and wish to disable this behavior, you can do so by editing ``/etc/quantum/quantum.cfg`` or ``~/.quantum.cfg``:

.. code-block:: text

    [defaults]
    host_key_checking = False

Alternatively this can be set by the :envvar:`ANSIBLE_HOST_KEY_CHECKING` environment variable:

.. code-block:: bash

    $ export ANSIBLE_HOST_KEY_CHECKING=False

Also note that host key checking in paramiko mode is reasonably slow, therefore switching to 'ssh' is also recommended when using this feature.

Other connection methods
------------------------

Quantum can use a variety of connection methods beyond SSH. You can select any connection plugin, including managing things locally and managing chroot, lxc, and jail containers.
A mode called 'quantum-pull' can also invert the system and have systems 'phone home' via scheduled git checkouts to pull configuration directives from a central repository.
