.. _eos_platform_options:

***************************************
EOS Platform Options
***************************************

Arista EOS supports multiple connections. This page offers details on how each connection works in Quantum and how to use it.

.. contents:: Topics

Connections Available
================================================================================

.. table::
    :class: documentation-table

    ====================  ==========================================  =========================
    ..                    CLI                                         eAPI
    ====================  ==========================================  =========================
    Protocol              SSH                                         HTTP(S)

    Credentials           uses SSH keys / SSH-agent if present        uses HTTPS certificates if
                                                                      present
                          accepts ``-u myuser -k`` if using password

    Indirect Access       via a bastion (jump host)                   via a web proxy

    Connection Settings   ``quantum_connection: network_cli``         ``quantum_connection: httpapi``

                                                                      OR

                                                                      ``quantum_connection: local``
                                                                      with ``transport: eapi``
                                                                      in the ``provider`` dictionary

    |enable_mode|         supported: |br|                             supported: |br|

                          * use ``quantum_become: yes``               * ``httpapi``
                            with ``quantum_become_method: enable``      uses ``quantum_become: yes``
                                                                        with ``quantum_become_method: enable``

                                                                      * ``local``
                                                                        uses ``authorize: yes``
                                                                        and ``auth_pass:``
                                                                        in the ``provider`` dictionary

    Returned Data Format  ``stdout[0].``                              ``stdout[0].messages[0].``
    ====================  ==========================================  =========================

.. |enable_mode| replace:: Enable Mode |br| (Privilege Escalation)


For legacy couplings, EOS still supports ``quantum_connection: local``. We recommend modernizing to use ``quantum_connection: network_cli`` or ``quantum_connection: httpapi`` as soon as possible.

Using CLI in Quantum
====================

Example CLI ``group_vars/eos.yml``
----------------------------------

.. code-block:: yaml

   quantum_connection: network_cli
   quantum_network_os: eos
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

   - name: Backup current switch config (eos)
     eos_config:
       backup: yes
     register: backup_eos_location
     when: quantum_network_os == 'eos'



Using eAPI in Quantum
=====================

Enabling eAPI
-------------

Before you can use eAPI to connect to a switch, you must enable eAPI. To enable eAPI on a new switch via Quantum, use the ``eos_eapi`` module via the CLI connection. Set up group_vars/eos.yml just like in the CLI example above, then run a coupling task like this:

.. code-block:: yaml

   - name: Enable eAPI
      eos_eapi:
          enable_http: yes
          enable_https: yes
      become: true
      become_method: enable
      when: quantum_network_os == 'eos'

You can find more options for enabling HTTP/HTTPS connections in the :ref:`eos_eapi <eos_eapi_module>` module documentation.

Once eAPI is enabled, change your ``group_vars/eos.yml`` to use the eAPI connection.

Example eAPI ``group_vars/eos.yml``
-----------------------------------

.. code-block:: yaml

   quantum_connection: httpapi
   quantum_network_os: eos
   quantum_user: myuser
   quantum_password: !vault...
   quantum_become: yes
   quantum_become_method: enable
   proxy_env:
     http_proxy: http://proxy.example.com:8080

- If you are accessing your host directly (not through a web proxy) you can remove the ``proxy_env`` configuration.
- If you are accessing your host through a web proxy using ``https``, change ``http_proxy`` to ``https_proxy``.


Example eAPI Task
-----------------

.. code-block:: yaml

   - name: Backup current switch config (eos)
     eos_config:
       backup: yes
     register: backup_eos_location
     environment: "{{ proxy_env }}"
     when: quantum_network_os == 'eos'

In this example the ``proxy_env`` variable defined in ``group_vars`` gets passed to the ``environment`` option of the module in the task.

eAPI examples with ``connection: local``
-----------------------------------------

``group_vars/eos.yml``:

.. code-block:: yaml

   quantum_connection: local
   quantum_network_os: eos
   quantum_user: myuser
   quantum_password: !vault...
   eapi:
     host: "{{ inventory_hostname }}"
     transport: eapi
     authorize: yes
     auth_pass: !vault...
   proxy_env:
     http_proxy: http://proxy.example.com:8080

eAPI task:

.. code-block:: yaml

   - name: Backup current switch config (eos)
     eos_config:
       backup: yes
       provider: "{{ eapi }}"
     register: backup_eos_location
     environment: "{{ proxy_env }}"
     when: quantum_network_os == 'eos'

In this example two variables defined in ``group_vars`` get passed to the module of the task:

- the ``eapi`` variable gets passed to the ``provider`` option of the module
- the ``proxy_env`` variable gets passed to the ``environment`` option of the module

.. include:: shared_snippets/SSH_warning.txt
