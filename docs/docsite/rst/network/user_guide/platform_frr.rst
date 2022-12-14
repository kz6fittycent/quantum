.. _frr_platform_options:

***************************************
FRR Platform Options
***************************************

This page offers details on connection options to manage FRR using Quantum.

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

    |enable_mode|         not supported

    Returned Data Format  ``stdout[0].``
    ====================  ==========================================

.. |enable_mode| replace:: Enable Mode |br| (Privilege Escalation)


Using CLI in Quantum
====================

Example CLI ``group_vars/frr.yml``
----------------------------------

.. code-block:: yaml

   quantum_connection: network_cli
   quantum_network_os: frr
   quantum_user: frruser
   quantum_password: !vault...
   quantum_ssh_common_args: '-o ProxyCommand="ssh -W %h:%p -q bastion01"'

- The `quantum_user` should be a part of the `frrvty` group and should have the default shell set to `/bin/vtysh`.
- If you are using SSH keys (including an ssh-agent) you can remove the ``quantum_password`` configuration.
- If you are accessing your host directly (not through a bastion/jump host) you can remove the ``quantum_ssh_common_args`` configuration.
- If you are accessing your host through a bastion/jump host, you cannot include your SSH password in the ``ProxyCommand`` directive. To prevent secrets from leaking out (for example in ``ps`` output), SSH does not support providing passwords via environment variables.

Example CLI Task
----------------

.. code-block:: yaml

   - name: Gather FRR facts
     frr_facts:
       gather_subset:
        - config
        - hardware

.. include:: shared_snippets/SSH_warning.txt
