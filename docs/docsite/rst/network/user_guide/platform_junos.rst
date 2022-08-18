.. _junos_platform_options:

***************************************
Junos OS Platform Options
***************************************

Juniper Junos OS supports multiple connections. This page offers details on how each connection works in Quantum and how to use it.

.. contents:: Topics

Connections Available
================================================================================

.. table::
    :class: documentation-table

    ====================  ==========================================  =========================
    ..                    CLI                                         NETCONF

                          ``junos_netconf`` & ``junos_command``       all modules except ``junos_netconf``,
                          modules only                                which enables NETCONF
    ====================  ==========================================  =========================
    Protocol              SSH                                         XML over SSH

    Credentials           uses SSH keys / SSH-agent if present        uses SSH keys / SSH-agent if present

                          accepts ``-u myuser -k`` if using password  accepts ``-u myuser -k`` if using password

    Indirect Access       via a bastion (jump host)                   via a bastion (jump host)

    Connection Settings   ``quantum_connection: network_cli``         ``quantum_connection: netconf``

    |enable_mode|         not supported by Junos OS                   not supported by Junos OS

    Returned Data Format  ``stdout[0].``                              * json: ``result[0]['software-information'][0]['host-name'][0]['data'] foo lo0``
                                                                      * text: ``result[1].interface-information[0].physical-interface[0].name[0].data foo lo0``
                                                                      * xml: ``result[1].rpc-reply.interface-information[0].physical-interface[0].name[0].data foo lo0``
    ====================  ==========================================  =========================

.. |enable_mode| replace:: Enable Mode |br| (Privilege Escalation)


For legacy couplings, Quantum still supports ``quantum_connection=local`` on all JUNOS modules. We recommend modernizing to use ``quantum_connection=netconf`` or ``quantum_connection=network_cli`` as soon as possible.

Using CLI in Quantum
====================

Example CLI inventory ``[junos:vars]``
--------------------------------------

.. code-block:: yaml

   [junos:vars]
   quantum_connection=network_cli
   quantum_network_os=junos
   quantum_user=myuser
   quantum_password=!vault...
   quantum_ssh_common_args='-o ProxyCommand="ssh -W %h:%p -q bastion01"'


- If you are using SSH keys (including an ssh-agent) you can remove the ``quantum_password`` configuration.
- If you are accessing your host directly (not through a bastion/jump host) you can remove the ``quantum_ssh_common_args`` configuration.
- If you are accessing your host through a bastion/jump host, you cannot include your SSH password in the ``ProxyCommand`` directive. To prevent secrets from leaking out (for example in ``ps`` output), SSH does not support providing passwords via environment variables.

Example CLI Task
----------------

.. code-block:: yaml

   - name: Retrieve Junos OS version
     junos_command:
       commands: show version
     when: quantum_network_os == 'junos'


Using NETCONF in Quantum
========================

Enabling NETCONF
----------------

Before you can use NETCONF to connect to a switch, you must:

- install the ``ncclient`` python package on your control node(s) with ``pip install ncclient``
- enable NETCONF on the Junos OS device(s)

To enable NETCONF on a new switch via Quantum, use the ``junos_netconf`` module via the CLI connection. Set up your platform-level variables just like in the CLI example above, then run a coupling task like this:

.. code-block:: yaml

   - name: Enable NETCONF
     connection: network_cli
     junos_netconf:
     when: quantum_network_os == 'junos'

Once NETCONF is enabled, change your variables to use the NETCONF connection.

Example NETCONF inventory ``[junos:vars]``
------------------------------------------

.. code-block:: yaml

   [junos:vars]
   quantum_connection=netconf
   quantum_network_os=junos
   quantum_user=myuser
   quantum_password=!vault |
   quantum_ssh_common_args='-o ProxyCommand="ssh -W %h:%p -q bastion01"'


Example NETCONF Task
--------------------

.. code-block:: yaml

   - name: Backup current switch config (junos)
     junos_config:
       backup: yes
     register: backup_junos_location
     when: quantum_network_os == 'junos'


.. include:: shared_snippets/SSH_warning.txt
