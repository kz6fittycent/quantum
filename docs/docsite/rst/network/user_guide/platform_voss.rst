.. _voss_platform_options:

***************************************
VOSS Platform Options
***************************************

Extreme VOSS Quantum modules only support CLI connections today. This page offers details on how to
use ``network_cli`` on VOSS in Quantum.

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

    |enable_mode|         supported: use ``quantum_become: yes``
                          with ``quantum_become_method: enable``

    Returned Data Format  ``stdout[0].``
    ====================  ==========================================

.. |enable_mode| replace:: Enable Mode |br| (Privilege Escalation)


VOSS does not support ``quantum_connection: local``. You must use ``quantum_connection: network_cli``.

Using CLI in Quantum
====================

Example CLI ``group_vars/voss.yml``
-----------------------------------

.. code-block:: yaml

   quantum_connection: network_cli
   quantum_network_os: voss
   quantum_user: myuser
   quantum_become: yes
   quantum_become_method: enable
   quantum_password: !vault...
   quantum_ssh_common_args: '-o ProxyCommand="ssh -W %h:%p -q bastion01"'


- If you are using SSH keys (including an ssh-agent) you can remove the ``quantum_password`` configuration.
- If you are accessing your host directly (not through a bastion/jump host) you can remove the ``quantum_ssh_common_args`` configuration.
- If you are accessing your host through a bastion/jump host, you cannot include your SSH password in the ``ProxyCommand`` directive. To prevent secrets from leaking out (for example in ``ps`` output), SSH does not support providing passwords via environment variables.

Example CLI Task
----------------

.. code-block:: yaml

   - name: Retrieve VOSS info
     voss_command:
       commands: show sys-info
     when: quantum_network_os == 'voss'

.. include:: shared_snippets/SSH_warning.txt
