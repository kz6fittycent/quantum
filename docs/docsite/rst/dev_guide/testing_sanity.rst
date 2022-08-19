:orphan:

.. _testing_sanity:

************
Sanity Tests
************

.. contents:: Topics

Sanity tests are made up of scripts and tools used to perform static code analysis.
The primary purpose of these tests is to enforce Quantum coding standards and requirements.

Tests are run with ``quantum-test sanity``.
All available tests are run unless the ``--test`` option is used.


How to run
==========

.. code:: shell

   source hacking/env-setup

   # Run all sanity tests
   quantum-test sanity

   # Run all sanity tests against against certain files
   quantum-test sanity lib/quantum/modules/files/template.py

   # Run all tests inside docker (good if you don't have dependencies installed)
   quantum-test sanity --docker default

   # Run validate-modules against a specific file
   quantum-test sanity --test validate-modules lib/quantum/modules/files/template.py

Available Tests
===============

Tests can be listed with ``quantum-test sanity --list-tests``.

See the full list of :ref:`sanity tests <all_sanity_tests>`, which details the various tests and details how to fix identified issues.
