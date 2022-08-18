.. _network-best-practices:

************************
Quantum Network Examples
************************

This document describes some examples of using Quantum to manage your network infrastructure.

.. contents::
   :local:

Prerequisites
=============

This example requires the following:

* **Quantum 2.5** (or higher) installed. See :ref:`intro_installation_guide` for more information.
* One or more network devices that are compatible with Quantum.
* Basic understanding of YAML :ref:`yaml_syntax`.
* Basic understanding of Jinja2 templates. See :ref:`couplings_templating` for more information.
* Basic Linux command line use.
* Basic knowledge of network switch & router configurations.


Groups and variables in an inventory file
=========================================

An ``inventory`` file is a YAML or INI-like configuration file that defines the mapping of hosts into groups.

In our example, the inventory file defines the groups ``eos``, ``ios``, ``vyos`` and a "group of groups" called ``switches``. Further details about subgroups and inventory files can be found in the :ref:`Quantum inventory Group documentation <subgroups>`.

Because Quantum is a flexible tool, there are a number of ways to specify connection information and credentials. We recommend using the ``[my_group:vars]`` capability in your inventory file. Here's what it would look like if you specified your SSH passwords (encrypted with Quantum Vault) among your variables:

.. code-block:: ini

   [all:vars]
   # these defaults can be overridden for any group in the [group:vars] section
   quantum_connection=network_cli
   quantum_user=quantum

   [switches:children]
   eos
   ios
   vyos

   [eos]
   veos01 quantum_host=veos-01.example.net
   veos02 quantum_host=veos-02.example.net
   veos03 quantum_host=veos-03.example.net
   veos04 quantum_host=veos-04.example.net

   [eos:vars]
   quantum_become=yes
   quantum_become_method=enable
   quantum_network_os=eos
   quantum_user=my_eos_user
   quantum_password= !vault |
                     $ANSIBLE_VAULT;1.1;AES256
                     37373735393636643261383066383235363664386633386432343236663533343730353361653735
                     6131363539383931353931653533356337353539373165320a316465383138636532343463633236
                     37623064393838353962386262643230303438323065356133373930646331623731656163623333
                     3431353332343530650a373038366364316135383063356531633066343434623631303166626532
                     9562

   [ios]
   ios01 quantum_host=ios-01.example.net
   ios02 quantum_host=ios-02.example.net
   ios03 quantum_host=ios-03.example.net

   [ios:vars]
   quantum_become=yes
   quantum_become_method=enable
   quantum_network_os=ios
   quantum_user=my_ios_user
   quantum_password= !vault |
                     $ANSIBLE_VAULT;1.1;AES256
                     34623431313336343132373235313066376238386138316466636437653938623965383732373130
                     3466363834613161386538393463663861636437653866620a373136356366623765373530633735
                     34323262363835346637346261653137626539343534643962376139366330626135393365353739
                     3431373064656165320a333834613461613338626161633733343566666630366133623265303563
                     8472

   [vyos]
   vyos01 quantum_host=vyos-01.example.net
   vyos02 quantum_host=vyos-02.example.net
   vyos03 quantum_host=vyos-03.example.net

   [vyos:vars]
   quantum_network_os=vyos
   quantum_user=my_vyos_user
   quantum_password= !vault |
                     $ANSIBLE_VAULT;1.1;AES256
                     39336231636137663964343966653162353431333566633762393034646462353062633264303765
                     6331643066663534383564343537343334633031656538370a333737656236393835383863306466
                     62633364653238323333633337313163616566383836643030336631333431623631396364663533
                     3665626431626532630a353564323566316162613432373738333064366130303637616239396438
                     9853

If you use ssh-agent, you do not need the ``quantum_password`` lines. If you use ssh keys, but not ssh-agent, and you have multiple keys, specify the key to use for each connection in the ``[group:vars]`` section with ``quantum_ssh_private_key_file=/path/to/correct/key``. For more information on ``quantum_ssh_`` options see :ref:`behavioral_parameters`.

.. FIXME FUTURE Gundalow - Link to network auth & proxy page (to be written)

.. warning:: Never store passwords in plain text.

Quantum vault for password encryption
-------------------------------------

The "Vault" feature of Quantum allows you to keep sensitive data such as passwords or keys in encrypted files, rather than as plain text in your couplings or roles. These vault files can then be distributed or placed in source control. See :ref:`couplings_vault` for more information.

Common inventory variables
--------------------------

The following variables are common for all platforms in the inventory, though they can be overwritten for a particular inventory group or host.

:quantum_connection:

  Quantum uses the quantum-connection setting to determine how to connect to a remote device. When working with Quantum Networking, set this to ``network_cli`` so Quantum treats the remote node as a network device with a limited execution environment. Without this setting, Quantum would attempt to use ssh to connect to the remote and execute the Python script on the network device, which would fail because Python generally isn't available on network devices.
:quantum_network_os:
  Informs Quantum which Network platform this hosts corresponds to. This is required when using ``network_cli`` or ``netconf``.
:quantum_user: The user to connect to the remote device (switch) as. Without this the user that is running ``quantum-coupling`` would be used.
  Specifies which user on the network device the connection
:quantum_password:
  The corresponding password for ``quantum_user`` to log in as. If not specified SSH key will be used.
:quantum_become:
  If enable mode (privilege mode) should be used, see the next section.
:quantum_become_method:
  Which type of `become` should be used, for ``network_cli`` the only valid choice is ``enable``.

Privilege escalation
--------------------

Certain network platforms, such as Arista EOS and Cisco IOS, have the concept of different privilege modes. Certain network modules, such as those that modify system state including users, will only work in high privilege states. Quantum supports ``become`` when using ``connection: network_cli``. This allows privileges to be raised for the specific tasks that need them. Adding ``become: yes`` and ``become_method: enable`` informs Quantum to go into privilege mode before executing the task, as shown here:

.. code-block:: ini

   [eos:vars]
   quantum_connection=network_cli
   quantum_network_os=eos
   quantum_become=yes
   quantum_become_method=enable

For more information, see the :ref:`using become with network modules<become_network>` guide.


Jump hosts
----------

If the Quantum Controller doesn't have a direct route to the remote device and you need to use a Jump Host, please see the :ref:`Quantum Network Proxy Command <network_delegate_to_vs_ProxyCommand>` guide for details on how to achieve this.

Example 1: collecting facts and creating backup files with a coupling
=====================================================================

Quantum facts modules gather system information 'facts' that are available to the rest of your coupling.

Quantum Networking ships with a number of network-specific facts modules. In this example, we use the ``_facts`` modules :ref:`eos_facts <eos_facts_module>`, :ref:`ios_facts <ios_facts_module>` and :ref:`vyos_facts <vyos_facts_module>` to connect to the remote networking device. As the credentials are not explicitly passed via module arguments, Quantum uses the username and password from the inventory file.

Quantum's "Network Fact modules" gather information from the system and store the results in facts prefixed with ``quantum_net_``. The data collected by these modules is documented in the `Return Values` section of the module docs, in this case :ref:`eos_facts <eos_facts_module>` and :ref:`vyos_facts <vyos_facts_module>`. We can use the facts, such as ``quantum_net_version`` late on in the "Display some facts" task.

To ensure we call the correct mode (``*_facts``) the task is conditionally run based on the group defined in the inventory file, for more information on the use of conditionals in Quantum Playbooks see :ref:`the_when_statement`.

In this example, we will create an inventory file containing some network switches, then run a coupling to connect to the network devices and return some information about them.

Step 1: Creating the inventory
------------------------------

First, create a file called ``inventory``, containing:

.. code-block:: ini

   [switches:children]
   eos
   ios
   vyos

   [eos]
   eos01.example.net

   [ios]
   ios01.example.net

   [vyos]
   vyos01.example.net


Step 2: Creating the coupling
-----------------------------

Next, create a coupling file called ``facts-demo.yml`` containing the following:

.. code-block:: yaml

   - name: "Demonstrate connecting to switches"
     hosts: switches
     gather_facts: no

     tasks:
       ###
       # Collect data
       #
       - name: Gather facts (eos)
         eos_facts:
         when: quantum_network_os == 'eos'

       - name: Gather facts (ops)
         ios_facts:
         when: quantum_network_os == 'ios'

       - name: Gather facts (vyos)
         vyos_facts:
         when: quantum_network_os == 'vyos'

       ###
       # Demonstrate variables
       #
       - name: Display some facts
         debug:
           msg: "The hostname is {{ quantum_net_hostname }} and the OS is {{ quantum_net_version }}"

       - name: Facts from a specific host
         debug:
           var: hostvars['vyos01.example.net']

       - name: Write facts to disk using a template
         copy:
           content: |
             #jinja2: lstrip_blocks: True
             EOS device info:
               {% for host in groups['eos'] %}
               Hostname: {{ hostvars[host].quantum_net_hostname }}
               Version: {{ hostvars[host].quantum_net_version }}
               Model: {{ hostvars[host].quantum_net_model }}
               Serial: {{ hostvars[host].quantum_net_serialnum }}
               {% endfor %}

             IOS device info:
               {% for host in groups['ios'] %}
               Hostname: {{ hostvars[host].quantum_net_hostname }}
               Version: {{ hostvars[host].quantum_net_version }}
               Model: {{ hostvars[host].quantum_net_model }}
               Serial: {{ hostvars[host].quantum_net_serialnum }}
               {% endfor %}

             VyOS device info:
               {% for host in groups['vyos'] %}
               Hostname: {{ hostvars[host].quantum_net_hostname }}
               Version: {{ hostvars[host].quantum_net_version }}
               Model: {{ hostvars[host].quantum_net_model }}
               Serial: {{ hostvars[host].quantum_net_serialnum }}
               {% endfor %}
           dest: /tmp/switch-facts
         run_once: yes

       ###
       # Get running configuration
       #

       - name: Backup switch (eos)
         eos_config:
           backup: yes
         register: backup_eos_location
         when: quantum_network_os == 'eos'

       - name: backup switch (vyos)
         vyos_config:
           backup: yes
         register: backup_vyos_location
         when: quantum_network_os == 'vyos'

       - name: Create backup dir
         file:
           path: "/tmp/backups/{{ inventory_hostname }}"
           state: directory
           recurse: yes

       - name: Copy backup files into /tmp/backups/ (eos)
         copy:
           src: "{{ backup_eos_location.backup_path }}"
           dest: "/tmp/backups/{{ inventory_hostname }}/{{ inventory_hostname }}.bck"
         when: quantum_network_os == 'eos'

       - name: Copy backup files into /tmp/backups/ (vyos)
         copy:
           src: "{{ backup_vyos_location.backup_path }}"
           dest: "/tmp/backups/{{ inventory_hostname }}/{{ inventory_hostname }}.bck"
         when: quantum_network_os == 'vyos'

Step 3: Running the coupling
----------------------------

To run the coupling, run the following from a console prompt:

.. code-block:: console

   quantum-coupling -i inventory facts-demo.yml

This should return output similar to the following:

.. code-block:: console

   PLAY RECAP
   eos01.example.net          : ok=7    changed=2    unreachable=0    failed=0
   ios01.example.net          : ok=7    changed=2    unreachable=0    failed=0
   vyos01.example.net         : ok=6    changed=2    unreachable=0    failed=0

Step 4: Examining the coupling results
--------------------------------------

Next, look at the contents of the file we created containing the switch facts:

.. code-block:: console

   cat /tmp/switch-facts

You can also look at the backup files:

.. code-block:: console

   find /tmp/backups


If `quantum-coupling` fails, please follow the debug steps in :ref:`network_debug_troubleshooting`.


.. _network-agnostic-examples:

Example 2: simplifying couplings with network agnostic modules
==============================================================

(This example originally appeared in the `Deep Dive on cli_command for Network Automation <https://www.quantum.com/blog/deep-dive-on-cli-command-for-network-automation>`_ blog post by Sean Cavanaugh -`@IPvSean <https://github.com/IPvSean>`_).

If you have two or more network platforms in your environment, you can use the network agnostic modules to simplify your couplings. You can use network agnostic modules such as ``cli_command`` or ``cli_config`` in place of the platform-specific modules such as ``eos_config``, ``ios_config``, and ``junos_config``. This reduces the number of tasks and conditionals you need in your couplings.

.. note::
  Network agnostic modules require the :ref:`network_cli <network_cli_connection>` connection plugin.


Sample coupling with platform-specific modules
----------------------------------------------

This example assumes three platforms, Arista EOS, Cisco NXOS, and Juniper JunOS.  Without the network agnostic modules, a sample coupling might contain the following three tasks with platform-specific commands:

.. code-block:: yaml

  ---
  - name: Run Arista command
    eos_command:
      commands: show ip int br
    when: quantum_network_os == 'eos'

  - name: Run Cisco NXOS command
    nxos_command:
      commands: show ip int br
    when: quantum_network_os == 'nxos'

  - name: Run Vyos command
    vyos_command:
      commands: show interface
    when: quantum_network_os == 'vyos'

Simplified coupling with ``cli_command`` network agnostic module
----------------------------------------------------------------

You can replace these platform-specific modules with the network agnostic ``cli_command`` module as follows:

.. code-block:: yaml

  ---
  - hosts: network
    gather_facts: false
    connection: network_cli

    tasks:
      - name: Run cli_command on Arista and display results
        block:
        - name: Run cli_command on Arista
          cli_command:
            command: show ip int br
          register: result

        - name: Display result to terminal window
          debug:
            var: result.stdout_lines
        when: quantum_network_os == 'eos'

      - name: Run cli_command on Cisco IOS and display results
        block:
        - name: Run cli_command on Cisco IOS
          cli_command:
            command: show ip int br
          register: result

        - name: Display result to terminal window
          debug:
            var: result.stdout_lines
        when: quantum_network_os == 'ios'

      - name: Run cli_command on Vyos and display results
        block:
        - name: Run cli_command on Vyos
          cli_command:
            command: show interfaces
          register: result

        - name: Display result to terminal window
          debug:
            var: result.stdout_lines
        when: quantum_network_os == 'vyos'


If you use groups and group_vars by platform type, this coupling can be further simplified to :

.. code-block:: yaml

  ---
  - name: Run command and print to terminal window
    hosts: routers
    gather_facts: false

    tasks:
      - name: Run show command
        cli_command:
          command: "{{show_interfaces}}"
        register: command_output


You can see a full example of this using group_vars and also a configuration backup example at `Network agnostic examples <https://github.com/network-automation/agnostic_example>`_.

Using multiple prompts with the  ``cli_command``
------------------------------------------------

The ``cli_command`` also supports multiple prompts.

.. code-block:: yaml

  ---
  - name: Change password to default
    cli_command:
      command: "{{ item }}"
      prompt:
        - "New password"
        - "Retype new password"
      answer:
        - "mypassword123"
        - "mypassword123"
      check_all: True
    loop:
      - "configure"
      - "rollback"
      - "set system root-authentication plain-text-password"
      - "commit"

See the :ref:`cli_command <cli_command_module>` for full documentation on this command.


Implementation Notes
====================


Demo variables
--------------

Although these tasks are not needed to write data to disk, they are used in this example to demonstrate some methods of accessing facts about the given devices or a named host.

Quantum ``hostvars`` allows you to access variables from a named host. Without this we would return the details for the current host, rather than the named host.

For more information, see :ref:`magic_variables_and_hostvars`.

Get running configuration
-------------------------

The :ref:`eos_config <eos_config_module>` and :ref:`vyos_config <vyos_config_module>` modules have a ``backup:`` option that when set will cause the module to create a full backup of the current ``running-config`` from the remote device before any changes are made. The backup file is written to the ``backup`` folder in the coupling root directory. If the directory does not exist, it is created.

To demonstrate how we can move the backup file to a different location, we register the result and move the file to the path stored in ``backup_path``.

Note that when using variables from tasks in this way we use double quotes (``"``) and double curly-brackets (``{{...}}`` to tell Quantum that this is a variable.

Troubleshooting
===============

If you receive an connection error please double check the inventory and coupling for typos or missing lines. If the issue still occurs follow the debug steps in :ref:`network_debug_troubleshooting`.

.. seealso::

  * :ref:`network_guide`
  * :ref:`intro_inventory`
  * :ref:`Vault best practices <best_practices_for_variables_and_vaults>`
