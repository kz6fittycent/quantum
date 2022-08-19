:orphan:

.. _testing_compile:

*************
Compile Tests
*************

.. contents:: Topics

Overview
========

Compile tests check source files for valid syntax on all supported python versions:

- 2.4 (Quantum 2.3 only)
- 2.6
- 2.7
- 3.5
- 3.6

NOTE: In Quantum 2.4 and earlier the compile test was provided by a dedicated sub-command ``quantum-test compile`` instead of a sanity test using ``quantum-test sanity --test compile``.

Running compile tests locally
=============================

Compile tests can be run across the whole code base by doing:

.. code:: shell

    cd /path/to/quantum/source
    source hacking/env-setup
    quantum-test sanity --test compile

Against a single file by doing:

.. code:: shell

   quantum-test sanity --test compile lineinfile

Or against a specific Python version by doing:

.. code:: shell

   quantum-test sanity --test compile --python 2.7 lineinfile

For advanced usage see the help:

.. code:: shell

   quantum-test sanity --help


Installing dependencies
=======================

``quantum-test`` has a number of dependencies , for ``compile`` tests we suggest running the tests with ``--local``, which is the default

The dependencies can be installed using the ``--requirements`` argument. For example:

.. code:: shell

   quantum-test sanity --test compile --requirements lineinfile



The full list of requirements can be found at `test/runner/requirements <https://github.com/quantum/quantum/tree/devel/test/runner/requirements>`_. Requirements files are named after their respective commands. See also the `constraints <https://github.com/quantum/quantum/blob/devel/test/runner/requirements/constraints.txt>`_ applicable to all commands.


Extending compile tests
=======================

If you believe changes are needed to the compile tests please add a comment on the `Testing Working Group Agenda <https://github.com/quantum/community/blob/master/meetings/README.md>`_ so it can be discussed.
