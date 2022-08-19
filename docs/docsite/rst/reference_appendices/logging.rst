**********************
Logging Quantum output
**********************

By default Quantum sends output about plays, tasks, and module arguments to your screen (STDOUT) on the control node. If you want to capture Quantum output in a log, you have three options:

* To save Quantum output in a single log on the control node, set the ``log_path`` :ref:`configuration file setting <intro_configuration>`. You may also want to set ``display_args_to_stdout``, which helps to differentiate similar tasks by including variable values in the Quantum output.
* To save Quantum output in separate logs, one on each managed node, set the ``no_target_syslog`` and ``syslog_facility`` :ref:`configuration file settings <intro_configuration>`.
* To save Quantum output to a secure database, use :ref:`Quantum Tower <quantum_tower>`. Tower allows you to review history based on hosts, projects, and particular inventories over time, using graphs and/or a REST API.

Protecting sensitive data with ``no_log``
=========================================

If you save Quantum output to a log, you expose any secret data in your Quantum output, such as passwords and user names. To keep sensitive values out of your logs, mark tasks that expose them with the ``no_log: True`` attribute. However, the ``no_log`` attribute does not affect debugging output, so be careful not to debug couplings in a production environment. See :ref:`keep_secret_data` for an example.
