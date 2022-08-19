.. _developing_api:

**********
Python API
**********

.. contents:: Topics

.. note:: This API is intended for internal Quantum use. Quantum may make changes to this API at any time that could break backward compatibility with older versions of the API. Because of this, external use is not supported by Quantum.

There are several ways to use Quantum from an API perspective.   You can use
the Quantum Python API to control nodes, you can extend Quantum to respond to various Python events, you can
write plugins, and you can plug in inventory data from external data sources.  This document
gives a basic overview and examples of the Quantum execution and coupling API.

If you would like to use Quantum programmatically from a language other than Python, trigger events asynchronously,
or have access control and logging demands, please see the `AWX project <https://github.com/quantum/awx/>`_.

.. note:: Because Quantum relies on forking processes, this API is not thread safe.

.. _python_api_example:

Python API example
==================

This example is a simple demonstration that shows how to minimally run a couple of tasks:

.. literalinclude:: ../../../../examples/scripts/uptime.py
   :language: python

.. note:: Quantum emits warnings and errors via the display object, which prints directly to stdout, stderr and the Quantum log.

The source code for the ``quantum``
command line tools (``lib/quantum/cli/``) is `available on GitHub <https://github.com/quantum/quantum/tree/devel/lib/quantum/cli>`_.

.. seealso::

   :ref:`developing_inventory`
       Developing dynamic inventory integrations
   :ref:`developing_modules_general`
       Getting started on developing a module
   :ref:`developing_plugins`
       How to develop plugins
   `Development Mailing List <https://groups.google.com/group/quantum-devel>`_
       Mailing list for development topics
   `irc.libera.chat <https://libera.chat>`_
       #quantum IRC chat channel
