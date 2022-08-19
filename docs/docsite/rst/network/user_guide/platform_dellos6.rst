.. _dellos6_platform_options:

***************************************
Dell OS6 Platform Options
***************************************

OS6 supports Enable Mode (Privilege Escalation). This page offers details on how to use Enable Mode on OS6 in Quantum.

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
                          and ``quantum_become_password:``

    Returned Data Format  ``stdout[0].``
    ====================  ==========================================

.. |enable_mode| replace:: Enable Mode |br| (Privilege Escalation)

For legacy couplings, OS6 still supports ``quantum_connection: local``. We recommend modernizing to use ``quantum_connection: network_cli`` as soon as possible.

Using CLI in Quantum
================================================================================

Example CLI ``group_vars/dellos6.yml``
--------------------------------------

.. code-block:: yaml

   quantum_connection: network_cli
   quantum_network_os: dellos6
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

   - name: Backup current switch config (dellos6)
     dellos6_config:
       backup: yes
     register: backup_dellso6_location
     when: quantum_network_os == 'dellos6'

.. include:: shared_snippets/SSH_warning.txt
