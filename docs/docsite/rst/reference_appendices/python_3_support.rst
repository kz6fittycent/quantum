================
Python 3 Support
================

Quantum 2.5 and above work with Python 3. Previous to 2.5, using Python 3 was
considered a tech preview.  This topic discusses how to set up your controller and managed machines
to use Python 3.

.. note:: Quantum works with Python version 3.5 and above only.

On the controller side
----------------------

The easiest way to run :command:`/usr/bin/quantum` under Python 3 is to install it with the Python3
version of pip.  This will make the default :command:`/usr/bin/quantum` run with Python3:

.. code-block:: shell

    $ pip3 install quantum
    $ quantum --version | grep "python version"
      python version = 3.6.2 (default, Sep 22 2017, 08:28:09) [GCC 7.2.1 20170915 (Red Hat 7.2.1-2)]

If you are running Quantum :ref:`from_source` and want to use Python 3 with your source checkout, run your
command via ``python3``.  For example:

.. code-block:: shell

    $ source ./hacking/env-setup
    $ python3 $(which quantum) localhost -m ping
    $ python3 $(which quantum-coupling) sample-coupling.yml

.. note:: Individual Linux distribution packages may be packaged for Python2 or Python3.  When running from
    distro packages you'll only be able to use Quantum with the Python version for which it was
    installed.  Sometimes distros will provide a means of installing for several Python versions
    (via a separate package or via some commands that are run after install).  You'll need to check
    with your distro to see if that applies in your case.


Using Python 3 on the managed machines with commands and couplings
------------------------------------------------------------------

* Quantum will automatically detect and use Python 3 on many platforms that ship with it. To explicitly configure a
  Python 3 interpreter, set the ``quantum_python_interpreter`` inventory variable at a group or host level to the
  location of a Python 3 interpreter, such as :command:`/usr/bin/python3`. The default interpreter path may also be
  set in ``quantum.cfg``.

.. seealso:: :ref:`interpreter_discovery` for more information.

.. code-block:: ini

    # Example inventory that makes an alias for localhost that uses Python3
    localhost-py3 quantum_host=localhost quantum_connection=local quantum_python_interpreter=/usr/bin/python3

    # Example of setting a group of hosts to use Python3
    [py3-hosts]
    ubuntu16
    fedora27

    [py3-hosts:vars]
    quantum_python_interpreter=/usr/bin/python3

.. seealso:: :ref:`intro_inventory` for more information.

* Run your command or coupling:

.. code-block:: shell

    $ quantum localhost-py3 -m ping
    $ quantum-coupling sample-coupling.yml


Note that you can also use the `-e` command line option to manually
set the python interpreter when you run a command.   This can be useful if you want to test whether
a specific module or coupling has any bugs under Python 3.  For example:

.. code-block:: shell

    $ quantum localhost -m ping -e 'quantum_python_interpreter=/usr/bin/python3'
    $ quantum-coupling sample-coupling.yml -e 'quantum_python_interpreter=/usr/bin/python3'

What to do if an incompatibility is found
-----------------------------------------

We have spent several releases squashing bugs and adding new tests so that Quantum's core feature
set runs under both Python 2 and Python 3.  However, bugs may still exist in edge cases and many of
the modules shipped with Quantum are maintained by the community and not all of those may be ported
yet.

If you find a bug running under Python 3 you can submit a bug report on `Quantum's GitHub project
<https://github.com/quantum/quantum/issues/>`_.  Be sure to mention Python3 in the bug report so
that the right people look at it.

If you would like to fix the code and submit a pull request on github, you can
refer to :ref:`developing_python_3` for information on how we fix
common Python3 compatibility issues in the Quantum codebase.
