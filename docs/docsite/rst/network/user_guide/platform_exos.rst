.. _exos_platform_options:

***************************************
EXOS Platform Options
***************************************

Extreme EXOS Quantum modules support multiple connections. This page offers details on how each connection works in Quantum and how to use it.

.. contents:: Topics

Connections Available
================================================================================


.. table::
    :class: documentation-table

    ====================  ==========================================  =========================
    ..                    CLI                                         EXOS-API
    ====================  ==========================================  =========================
    Protocol              SSH                                         HTTP(S)

    Credentials           uses SSH keys / SSH-agent if present        uses HTTPS certificates if present

                          accepts ``-u myuser -k`` if using password

    Indirect Access       via a bastion (jump host)                   via a web proxy

    Connection Settings   ``quantum_connection: network_cli``         ``quantum_connection: httpapi``

    |enable_mode|         not supported by EXOS                       not supported by EXOS

    Returned Data Format  ``stdout[0].``                              ``stdout[0].messages[0].``
    ====================  ==========================================  =========================

.. |enable_mode| replace:: Enable Mode |br| (Privilege Escalation)

EXOS does not support ``quantum_connection: local``. You must use ``quantum_connection: network_cli`` or ``quantum_connection: httpapi``

Using CLI in Quantum
====================

Example CLI ``group_vars/exos.yml``
-----------------------------------

.. code-block:: yaml

   quantum_connection: network_cli
   quantum_network_os: exos
   quantum_user: myuser
   quantum_password: !vault...
   quantum_ssh_common_args: '-o ProxyCommand="ssh -W %h:%p -q bastion01"'


- If you are using SSH keys (including an ssh-agent) you can remove the ``quantum_password`` configuration.
- If you are accessing your host directly (not through a bastion/jump host) you can remove the ``quantum_ssh_common_args`` configuration.
- If you are accessing your host through a bastion/jump host, you cannot include your SSH password in the ``ProxyCommand`` directive. To prevent secrets from leaking out (for example in ``ps`` output), SSH does not support providing passwords via environment variables.

Example CLI Task
----------------

.. code-block:: yaml

   - name: Retrieve EXOS OS version
     exos_command:
       commands: show version
     when: quantum_network_os == 'exos'



Using EXOS-API in Quantum
=========================

Example EXOS-API ``group_vars/exos.yml``
----------------------------------------

.. code-block:: yaml

   quantum_connection: httpapi
   quantum_network_os: exos
   quantum_user: myuser
   quantum_password: !vault...
   proxy_env:
     http_proxy: http://proxy.example.com:8080

- If you are accessing your host directly (not through a web proxy) you can remove the ``proxy_env`` configuration.
- If you are accessing your host through a web proxy using ``https``, change ``http_proxy`` to ``https_proxy``.


Example EXOS-API Task
---------------------

.. code-block:: yaml

   - name: Retrieve EXOS OS version
     exos_command:
       commands: show version
     when: quantum_network_os == 'exos'

In this example the ``proxy_env`` variable defined in ``group_vars`` gets passed to the ``environment`` option of the module used in the task.

.. include:: shared_snippets/SSH_warning.txt
