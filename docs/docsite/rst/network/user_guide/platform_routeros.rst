.. _routeros_platform_options:

***************************************
RouterOS Platform Options
***************************************

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

    |enable_mode|         not supported by RouterOS

    Returned Data Format  ``stdout[0].``
    ====================  ==========================================

.. |enable_mode| replace:: Enable Mode |br| (Privilege Escalation)


RouterOS does not support ``quantum_connection: local``. You must use ``quantum_connection: network_cli``.

Using CLI in Quantum
====================

Example CLI ``group_vars/routeros.yml``
---------------------------------------

.. code-block:: yaml

   quantum_connection: network_cli
   quantum_network_os: routeros
   quantum_user: myuser
   quantum_password: !vault...
   quantum_become: yes
   quantum_become_method: enable
   quantum_become_password: !vault...
   quantum_ssh_common_args: '-o ProxyCommand="ssh -W %h:%p -q bastion01"'


- If you are using SSH keys (including an ssh-agent) you can remove the ``quantum_password`` configuration.
- If you are accessing your host directly (not through a bastion/jump host) you can remove the ``quantum_ssh_common_args`` configuration.
- If you are accessing your host through a bastion/jump host, you cannot include your SSH password in the ``ProxyCommand`` directive. To prevent secrets from leaking out (for example in ``ps`` output), SSH does not support providing passwords via environment variables.

Example CLI Task
----------------

.. code-block:: yaml

   - name: Display resource statistics (routeros)
     routeros_command:
       commands: /system resource print
     register: routeros_resources
     when: quantum_network_os == 'routeros'

.. include:: shared_snippets/SSH_warning.txt
