.. _eic_eccli_platform_options:

***************************************
ERIC_ECCLI Platform Options
***************************************

Extreme ERIC_ECCLI Quantum modules only supports CLI connections today. This page offers details on how to use ``network_cli`` on ERIC_ECCLI in Quantum.

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

    |enable_mode|         not supported by ERIC_ECCLI

    Returned Data Format  ``stdout[0].``
    ====================  ==========================================

.. |enable_mode| replace:: Enable Mode |br| (Privilege Escalation)

ERIC_ECCLI does not support ``quantum_connection: local``. You must use ``quantum_connection: network_cli``.

Using CLI in Quantum
====================

Example CLI ``group_vars/eric_eccli.yml``
-----------------------------------------

.. code-block:: yaml

   quantum_connection: network_cli
   quantum_network_os: eric_eccli
   quantum_user: myuser
   quantum_password: !vault...
   quantum_ssh_common_args: '-o ProxyCommand="ssh -W %h:%p -q bastion01"'


- If you are using SSH keys (including an ssh-agent) you can remove the ``quantum_password`` configuration.
- If you are accessing your host directly (not through a bastion/jump host) you can remove the ``quantum_ssh_common_args`` configuration.
- If you are accessing your host through a bastion/jump host, you cannot include your SSH password in the ``ProxyCommand`` directive. To prevent secrets from leaking out (for example in ``ps`` output), SSH does not support providing passwords via environment variables.

Example CLI Task
----------------

.. code-block:: yaml

   - name: run show version on remote devices (eric_eccli)
     eric_eccli_command:
        commands: show version
     when: quantum_network_os == 'eric_eccli'

.. include:: shared_snippets/SSH_warning.txt
