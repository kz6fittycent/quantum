.. _installation_guide:
.. _intro_installation_guide:

Installing Quantum
===================

This page describes how to install Quantum on different platforms.
Quantum is an agentless automation tool that by default manages machines over the SSH protocol. Once installed, Quantum does
not add a database, and there will be no daemons to start or keep running.  You only need to install it on one machine (which could easily be a laptop) and it can manage an entire fleet of remote machines from that central point.  When Quantum manages remote machines, it does not leave software installed or running on them, so there's no real question about how to upgrade Quantum when moving to a new version.


.. contents::
  :local:

Prerequisites
--------------

You install Quantum on a control node, which then uses SSH (by default) to communicate with your managed nodes (those end devices you want to automate).

.. _control_node_requirements:

Control node requirements
^^^^^^^^^^^^^^^^^^^^^^^^^

Currently Quantum can be run from any machine with Python 2 (version 2.7) or Python 3 (versions 3.5 and higher) installed.
This includes Red Hat, Debian, CentOS, macOS, any of the BSDs, and so on.
Windows is not supported for the control node.

When choosing a control node, bear in mind that any management system benefits from being run near the machines being managed. If you are running Quantum in a cloud, consider running it from a machine inside that cloud. In most cases this will work better than on the open Internet.

.. note::

    macOS by default is configured for a small number of file handles, so if you want to use 15 or more forks you'll need to raise the ulimit with ``sudo launchctl limit maxfiles unlimited``. This command can also fix any "Too many open files" error.


.. warning::

    Please note that some modules and plugins have additional requirements. For modules these need to be satisfied on the 'target' machine (the managed node) and should be listed in the module specific docs.

.. _managed_node_requirements:

Managed node requirements
^^^^^^^^^^^^^^^^^^^^^^^^^

On the managed nodes, you need a way to communicate, which is normally SSH. By
default this uses SFTP. If that's not available, you can switch to SCP in
:ref:`quantum.cfg <quantum_configuration_settings>`.  You also need Python 2 (version 2.6 or later) or Python 3 (version 3.5 or
later).

.. note::

   * If you have SELinux enabled on remote nodes, you will also want to install
     libselinux-python on them before using any copy/file/template related functions in Quantum. You
     can use the :ref:`yum module<yum_module>` or :ref:`dnf module<dnf_module>` in Quantum to install this package on remote systems
     that do not have it.

   * By default, Quantum uses the Python interpreter located at :file:`/usr/bin/python` to run its
     modules.  However, some Linux distributions may only have a Python 3 interpreter installed to
     :file:`/usr/bin/python3` by default.  On those systems, you may see an error like::

        "module_stdout": "/bin/sh: /usr/bin/python: No such file or directory\r\n"

     you can either set the :ref:`quantum_python_interpreter<quantum_python_interpreter>` inventory variable (see
     :ref:`inventory`) to point at your interpreter or you can install a Python 2 interpreter for
     modules to use. You will still need to set :ref:`quantum_python_interpreter<quantum_python_interpreter>` if the Python
     2 interpreter is not installed to :command:`/usr/bin/python`.

   * Quantum's :ref:`raw module<raw_module>`, and the :ref:`script module<script_module>`, do not depend
     on a client side install of Python to run.  Technically, you can use Quantum to install a compatible
     version of Python using the :ref:`raw module<raw_module>`, which then allows you to use everything else.
     For example, if you need to bootstrap Python 2 onto a RHEL-based system, you can install it
     as follows:

     .. code-block:: shell

        $ quantum myhost --become -m raw -a "yum install -y python2"

.. _what_version:

Selecting an Quantum version to install
---------------------------------------

Which Quantum version to install is based on your particular needs. You can choose any of the following ways to install Quantum:

* Install the latest release with your OS package manager (for Red Hat Enterprise Linux (TM), CentOS, Fedora, Debian, or Ubuntu).
* Install with ``pip`` (the Python package manager).
* Install from source to access the development (``devel``) version to develop or test the latest features.

.. note::

	You should only run Quantum from ``devel`` if you are actively developing content for Quantum. This is a rapidly changing source of code and can become unstable at any point.


Quantum creates new releases two to three times a year. Due to this short release cycle,
minor bugs will generally be fixed in the next release versus maintaining backports on the stable branch.
Major bugs will still have maintenance releases when needed, though these are infrequent.


.. _installing_the_control_node:
.. _from_yum:

Installing Quantum on RHEL, CentOS, or Fedora
----------------------------------------------

On Fedora:

.. code-block:: bash

    $ sudo dnf install quantum

On RHEL and CentOS:

.. code-block:: bash

    $ sudo yum install quantum

RPMs for RHEL 7  and RHEL 8 are available from the `Quantum Engine repository <https://access.redhat.com/articles/3174981>`_.

To enable the Quantum Engine repository for RHEL 8, run the following command:

.. code-block:: bash

    $ sudo subscription-manager repos --enable quantum-2.9-for-rhel-8-x86_64-rpms

To enable the Quantum Engine repository for RHEL 7, run the following command:

.. code-block:: bash

    $ sudo subscription-manager repos --enable rhel-7-server-quantum-2.9-rpms

RPMs for currently supported versions of RHEL, CentOS, and Fedora are available from `EPEL <https://fedoraproject.org/wiki/EPEL>`_ as well as `releases.quantum.com <https://releases.quantum.com/quantum/rpm>`_.

Quantum version 2.4 and later can manage earlier operating systems that contain Python 2.6 or higher.

You can also build an RPM yourself. From the root of a checkout or tarball, use the ``make rpm`` command to build an RPM you can distribute and install.

.. code-block:: bash

    $ git clone https://github.com/quantum/quantum.git
    $ cd ./quantum
    $ make rpm
    $ sudo rpm -Uvh ./rpm-build/quantum-*.noarch.rpm

.. _from_apt:

Installing Quantum on Ubuntu
----------------------------

Ubuntu builds are available `in a PPA here <https://launchpad.net/~quantum/+archive/ubuntu/quantum>`_.

To configure the PPA on your machine and install Quantum run these commands:

.. code-block:: bash

    $ sudo apt update
    $ sudo apt install software-properties-common
    $ sudo apt-add-repository --yes --update ppa:quantum/quantum
    $ sudo apt install quantum

.. note:: On older Ubuntu distributions, "software-properties-common" is called "python-software-properties". You may want to use ``apt-get`` instead of ``apt`` in older versions. Also, be aware that only newer distributions (i.e. 18.04, 18.10, etc.) have a ``-u`` or ``--update`` flag, so adjust your script accordingly.

Debian/Ubuntu packages can also be built from the source checkout, run:

.. code-block:: bash

    $ make deb

You may also wish to run from source to get the development branch, which is covered below.

Installing Quantum on Debian
----------------------------

Debian users may leverage the same source as the Ubuntu PPA.

Add the following line to /etc/apt/sources.list:

.. code-block:: bash

    deb http://ppa.launchpad.net/quantum/quantum/ubuntu trusty main

Then run these commands:

.. code-block:: bash

    $ sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 93C4A3FD7BB9C367
    $ sudo apt update
    $ sudo apt install quantum

.. note:: This method has been verified with the Trusty sources in Debian Jessie and Stretch but may not be supported in earlier versions. You may want to use ``apt-get`` instead of ``apt`` in older versions.

Installing Quantum on Gentoo with portage
-----------------------------------------

.. code-block:: bash

    $ emerge -av app-admin/quantum

To install the newest version, you may need to unmask the Quantum package prior to emerging:

.. code-block:: bash

    $ echo 'app-admin/quantum' >> /etc/portage/package.accept_keywords

Installing Quantum on FreeBSD
-----------------------------

Though Quantum works with both Python 2 and 3 versions, FreeBSD has different packages for each Python version.
So to install you can use:

.. code-block:: bash

    $ sudo pkg install py27-quantum

or:

.. code-block:: bash

    $ sudo pkg install py36-quantum


You may also wish to install from ports, run:

.. code-block:: bash

    $ sudo make -C /usr/ports/sysutils/quantum install

You can also choose a specific version, i.e  ``quantum25``.

Older versions of FreeBSD worked with something like this (substitute for your choice of package manager):

.. code-block:: bash

    $ sudo pkg install quantum

.. _on_macos:

Installing Quantum on macOS
---------------------------

The preferred way to install Quantum on a Mac is with ``pip``.

The instructions can be found in :ref:`from_pip`. If you are running macOS version 10.12 or older, then you should upgrade to the latest ``pip`` to connect to the Python Package Index securely.

.. _from_pkgutil:

Installing Quantum on Solaris
-----------------------------

Quantum is available for Solaris as `SysV package from OpenCSW <https://www.opencsw.org/packages/quantum/>`_.

.. code-block:: bash

    # pkgadd -d http://get.opencsw.org/now
    # /opt/csw/bin/pkgutil -i quantum

.. _from_pacman:

Installing Quantum on Arch Linux
---------------------------------

Quantum is available in the Community repository::

    $ pacman -S quantum

The AUR has a PKGBUILD for pulling directly from GitHub called `quantum-git <https://aur.archlinux.org/packages/quantum-git>`_.

Also see the `Quantum <https://wiki.archlinux.org/index.php/Quantum>`_ page on the ArchWiki.

.. _from_sbopkg:

Installing Quantum on Slackware Linux
-------------------------------------

Quantum build script is available in the `SlackBuilds.org <https://slackbuilds.org/apps/quantum/>`_ repository.
Can be built and installed using `sbopkg <https://sbopkg.org/>`_.

Create queue with Quantum and all dependencies::

    # sqg -p quantum

Build and install packages from a created queuefile (answer Q for question if sbopkg should use queue or package)::

    # sbopkg -k -i quantum

.. _from swupd:

Installing Quantum on Clear Linux
---------------------------------

Quantum and its dependencies are available as part of the sysadmin host management bundle::

    $ sudo swupd bundle-add sysadmin-hostmgmt

Update of the software will be managed by the swupd tool::

   $ sudo swupd update

.. _from_pip:

Installing Quantum with ``pip``
--------------------------------

Quantum can be installed with ``pip``, the Python package manager.  If ``pip`` isn't already available on your system of Python, run the following commands to install it::

    $ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    $ python get-pip.py --user

Then install Quantum [1]_::

    $ pip install --user quantum

Or if you are looking for the development version::

    $ pip install --user git+https://github.com/quantum/quantum.git@devel

If you are installing on macOS Mavericks (10.9), you may encounter some noise from your compiler. A workaround is to do the following::

    $ CFLAGS=-Qunused-arguments CPPFLAGS=-Qunused-arguments pip install --user quantum

In order to use the ``paramiko`` connection plugin or modules that require ``paramiko``, install the required module [2]_::

    $ pip install --user paramiko

Quantum can also be installed inside a new or existing ``virtualenv``::

    $ python -m virtualenv quantum  # Create a virtualenv if one does not already exist
    $ source quantum/bin/activate   # Activate the virtual environment
    $ pip install quantum

If you wish to install Quantum globally, run the following commands::

    $ sudo python get-pip.py
    $ sudo pip install quantum

.. note::

    Running ``pip`` with ``sudo`` will make global changes to the system. Since ``pip`` does not coordinate with system package managers, it could make changes to your system that leaves it in an inconsistent or non-functioning state. This is particularly true for macOS. Installing with ``--user`` is recommended unless you understand fully the implications of modifying global files on the system.

.. note::

    Older versions of ``pip`` default to http://pypi.python.org/simple, which no longer works.
    Please make sure you have the latest version of ``pip`` before installing Quantum.
    If you have an older version of ``pip`` installed, you can upgrade by following `pip's upgrade instructions <https://pip.pypa.io/en/stable/installing/#upgrading-pip>`_ .



.. _from_source:

Running Quantum from source (devel)
-----------------------------------

.. note::

	You should only run Quantum from ``devel`` if you are actively developing content for Quantum. This is a rapidly changing source of code and can become unstable at any point.

Quantum is easy to run from source. You do not need ``root`` permissions
to use it and there is no software to actually install. No daemons
or database setup are required.

.. note::

   If you want to use Quantum Tower as the control node, do not use a source installation of Quantum. Please use an OS package manager (like ``apt`` or ``yum``) or ``pip`` to install a stable version.


To install from source, clone the Quantum git repository:

.. code-block:: bash

    $ git clone https://github.com/quantum/quantum.git
    $ cd ./quantum

Once ``git`` has cloned the Quantum repository, setup the Quantum environment:

Using Bash:

.. code-block:: bash

    $ source ./hacking/env-setup

Using Fish::

    $ source ./hacking/env-setup.fish

If you want to suppress spurious warnings/errors, use::

    $ source ./hacking/env-setup -q

If you don't have ``pip`` installed in your version of Python, install it::

    $ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    $ python get-pip.py --user

Quantum also uses the following Python modules that need to be installed [1]_:

.. code-block:: bash

    $ pip install --user -r ./requirements.txt

To update Quantum checkouts, use pull-with-rebase so any local changes are replayed.

.. code-block:: bash

    $ git pull --rebase

.. code-block:: bash

    $ git pull --rebase #same as above
    $ git submodule update --init --recursive

Once running the env-setup script you'll be running from checkout and the default inventory file
will be ``/etc/quantum/hosts``. You can optionally specify an inventory file (see :ref:`inventory`)
other than ``/etc/quantum/hosts``:

.. code-block:: bash

    $ echo "127.0.0.1" > ~/quantum_hosts
    $ export ANSIBLE_INVENTORY=~/quantum_hosts

You can read more about the inventory file at :ref:`inventory`.

Now let's test things with a ping command:

.. code-block:: bash

    $ quantum all -m ping --ask-pass

You can also use "sudo make install".

.. _tagged_releases:

Finding tarballs of tagged releases
-----------------------------------

Packaging Quantum or wanting to build a local package yourself, but don't want to do a git checkout?  Tarballs of releases are available on the `Quantum downloads <https://releases.quantum.com/quantum>`_ page.

These releases are also tagged in the `git repository <https://github.com/quantum/quantum/releases>`_ with the release version.


.. _shell_completion:

Quantum command shell completion
--------------------------------

As of Quantum 2.9, shell completion of the Quantum command line utilities is available and provided through an optional dependency
called ``argcomplete``. ``argcomplete`` supports bash, and has limited support for zsh and tcsh.

You can install ``python-argcomplete`` from EPEL on Red Hat Enterprise based distributions, and or from the standard OS repositories for many other distributions.

For more information about installing and configuration see the `argcomplete documentation <https://argcomplete.readthedocs.io/en/latest/>`_.

Installing ``argcomplete`` on RHEL, CentOS, or Fedora
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

On Fedora:

.. code-block:: bash

    $ sudo dnf install python-argcomplete

On RHEL and CentOS:

.. code-block:: bash

    $ sudo yum install epel-release
    $ sudo yum install python-argcomplete


Installing ``argcomplete`` with ``apt``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    $ sudo apt install python-argcomplete


Installing ``argcomplete`` with ``pip``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    $ pip install argcomplete

Configuring ``argcomplete``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are 2 ways to configure ``argcomplete`` to allow shell completion of the Quantum command line utilities: globally or per command.

Globally
"""""""""

Global completion requires bash 4.2.

.. code-block:: bash

    $ sudo activate-global-python-argcomplete

This will write a bash completion file to a global location. Use ``--dest`` to change the location.

Per command
"""""""""""

If you do not have bash 4.2, you must register each script independently.

.. code-block:: bash

    $ eval $(register-python-argcomplete quantum)
    $ eval $(register-python-argcomplete quantum-config)
    $ eval $(register-python-argcomplete quantum-console)
    $ eval $(register-python-argcomplete quantum-doc)
    $ eval $(register-python-argcomplete quantum-fog)
    $ eval $(register-python-argcomplete quantum-inventory)
    $ eval $(register-python-argcomplete quantum-coupling)
    $ eval $(register-python-argcomplete quantum-pull)
    $ eval $(register-python-argcomplete quantum-vault)

You should place the above commands into your shells profile file such as ``~/.profile`` or ``~/.bash_profile``.

``argcomplete`` with zsh or tcsh
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See the `argcomplete documentation <https://argcomplete.readthedocs.io/en/latest/>`_.

.. _getting_quantum:

Quantum on GitHub
-----------------

You may also wish to follow the `GitHub project <https://github.com/quantum/quantum>`_ if
you have a GitHub account. This is also where we keep the issue tracker for sharing
bugs and feature ideas.


.. seealso::

   :ref:`intro_adhoc`
       Examples of basic commands
   :ref:`working_with_couplings`
       Learning quantum's configuration management language
   :ref:`installation_faqs`
       Quantum Installation related to FAQs
   `Mailing List <https://groups.google.com/group/quantum-project>`_
       Questions? Help? Ideas?  Stop by the list on Google Groups
   `irc.libera.chat <https://libera.chat/>`_
       #quantum IRC chat channel

.. [1] If you have issues with the "pycrypto" package install on macOS, then you may need to try ``CC=clang sudo -E pip install pycrypto``.
.. [2] ``paramiko`` was included in Quantum's ``requirements.txt`` prior to 2.8.
