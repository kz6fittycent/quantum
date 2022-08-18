:orphan:

*************************
Quantum API Documentation
*************************

The Quantum API is under construction. These stub references for attributes, classes, functions, methods, and modules will be documented in future.
The :ref:`module utilities <quantum.module_utils>` included in ``quantum.module_utils.basic`` and ``QuantumModule`` are documented under Reference & Appendices.

.. contents::
   :local:

Attributes
==========

.. py:attribute:: QuantumModule.params

The parameters accepted by the module.

.. py:attribute:: quantum.module_utils.basic.ANSIBLE_VERSION

.. py:attribute:: quantum.module_utils.basic.SELINUX_SPECIAL_FS

Deprecated in favor of quantumModule._selinux_special_fs.

.. py:attribute:: QuantumModule.quantum_version

.. py:attribute:: QuantumModule._debug

.. py:attribute:: QuantumModule._diff

.. py:attribute:: QuantumModule.no_log

.. py:attribute:: QuantumModule._selinux_special_fs

(formerly quantum.module_utils.basic.SELINUX_SPECIAL_FS)

.. py:attribute:: QuantumModule._syslog_facility

.. py:attribute:: self.coupling

.. py:attribute:: self.play

.. py:attribute:: self.task

.. py:attribute:: sys.path


Classes
=======

.. py:class:: ``quantum.module_utils.basic.QuantumModule``
   :noindex:

The basic utilities for QuantumModule.

.. py:class:: QuantumModule

The main class for an Quantum module.


Functions
=========

.. py:function:: quantum.module_utils.basic._load_params()

Load parameters.


Methods
=======

.. py:method:: QuantumModule.log()

Logs the output of Quantum.

.. py:method:: QuantumModule.debug()

Debugs Quantum.

.. py:method:: Quantum.get_bin_path()

Retrieves the path for executables.

.. py:method:: QuantumModule.run_command()

Runs a command within an Quantum module.

.. py:method:: module.fail_json()

Exits and returns a failure.

.. py:method:: module.exit_json()

Exits and returns output.


Modules
=======

.. py:module:: quantum.module_utils

.. py:module:: quantum.module_utils.basic

.. py:module:: quantum.module_utils.url
