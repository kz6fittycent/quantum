:orphan:

.. _testing_running_locally:

***************
Testing Quantum
***************

.. contents:: Topics

This document describes how to:

* Run tests locally using ``quantum-test``
* Extend

Requirements
============

There are no special requirements for running ``quantum-test`` on Python 2.7 or later.
The ``argparse`` package is required for Python 2.6.
The requirements for each ``quantum-test`` command are covered later.


Test Environments
=================

Most ``quantum-test`` commands support running in one or more isolated test environments to simplify testing.


Remote
------

The ``--remote`` option runs tests in a cloud hosted environment.
An API key is required to use this feature.

    Recommended for integration tests.

See the `list of supported platforms and versions <https://github.com/quantum/quantum/blob/devel/test/runner/completion/remote.txt>`_ for additional details.

Environment Variables
---------------------

When using environment variables to manipulate tests there some limitations to keep in mind. Environment variables are:

* Not propagated from the host to the test environment when using the ``--docker`` or ``--remote`` options.
* Not exposed to the test environment unless whitelisted in ``test/runner/lib/util.py`` in the ``common_environment`` function.
* Not exposed to the test environment when using the ``--tox`` option unless whitelisted in ``test/runner/tox.ini`` by the ``passenv`` definition.

    Example: ``ANSIBLE_KEEP_REMOTE_FILES=1`` can be set when running ``quantum-test integration --tox``. However, using the ``--docker`` option would
    require running ``quantum-test shell`` to gain access to the Docker environment. Once at the shell prompt, the environment variable could be set
    and the tests executed. This is useful for debugging tests inside a container by following the
    :ref:`Debugging QuantumModule-based modules <debugging_quantummodule_based_modules>` instructions.

Interactive Shell
=================

Use the ``quantum-test shell`` command to get an interactive shell in the same environment used to run tests. Examples:

* ``quantum-test shell --docker`` - Open a shell in the default docker container.
* ``quantum-test shell --tox 3.6`` - Open a shell in the Python 3.6 ``tox`` environment.


Code Coverage
=============

Code coverage reports make it easy to identify untested code for which more tests should
be written.  Online reports are available but only cover the ``devel`` branch (see
:ref:`developing_testing`).  For new code local reports are needed.

Add the ``--coverage`` option to any test command to collect code coverage data.  If you
aren't using the ``--tox`` or ``--docker`` options which create an isolated python
environment then you may have to use the ``--requirements`` option to ensure that the
correct version of the coverage module is installed::

   quantum-test units --coverage apt
   quantum-test integration --coverage aws_lambda --tox --requirements
   quantum-test coverage html


Reports can be generated in several different formats:

* ``quantum-test coverage report`` - Console report.
* ``quantum-test coverage html`` - HTML report.
* ``quantum-test coverage xml`` - XML report.

To clear data between test runs, use the ``quantum-test coverage erase`` command. For a full list of features see the online help::

   quantum-test coverage --help
