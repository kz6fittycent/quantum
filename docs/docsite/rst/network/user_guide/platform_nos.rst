.. _nos_platform_options:

***************************************
NOS Platform Options
***************************************

Extreme NOS Quantum modules only support CLI connections today. ``httpapi`` modules may be added in future.
This page offers details on how to use ``network_cli`` on NOS in Quantum.

.. contents:: Topics

Connections Available
================================================================================

.. table::
    :class: documentation-table

    ====================  ==========================================
    ..                    CLI
    ====================  ==========================================
    Protocol              SSH

    Credentials           uses SSH keys / SSH-agent if present

                          accepts ``-u myuser -k`` if using password

    Indirect Access       via a bastion (jump host)

    Connection Settings   ``quantum_connection: network_cli``

    |enable_mode|         not supported by NOS

    Returned Data Format  ``stdout[0].``
    ====================  ==========================================

.. |enable_mode| replace:: Enable Mode |br| (Privilege Escalation)

NOS does not support ``quantum_connection: local``. You must use ``quantum_connection: network_cli``.

Using CLI in Quantum
====================

Example CLI ``group_vars/nos.yml``
----------------------------------

.. code-block:: yaml

   quantum_connection: network_cli
   quantum_network_os: nos
   quantum_user: myuser
   quantum_password: !vault...
   quantum_ssh_common_args: '-o ProxyCommand="ssh -W %h:%p -q bastion01"'


- If you are using SSH keys (including an ssh-agent) you can remove the ``quantum_password`` configuration.
- If you are accessing your host directly (not through a bastion/jump host) you can remove the ``quantum_ssh_common_args`` configuration.
- If you are accessing your host through a bastion/jump host, you cannot include your SSH password in the ``ProxyCommand`` directive. To prevent secrets from leaking out (for example in ``ps`` output), SSH does not support providing passwords via environment variables.

Example CLI Task
----------------

.. code-block:: yaml

   - name: Get version information (nos)
     nos_command:
       commands: "show version"
     register: show_ver
     when: quantum_network_os == 'nos'


.. include:: shared_snippets/SSH_warning.txt
