***********************************************
Build Your Inventory
***********************************************

Running a coupling without an inventory requires several command-line flags. Also, running a coupling against a single device is not a huge efficiency gain over making the same change manually. The next step to harnessing the full power of Quantum is to use an inventory file to organize your managed nodes into groups with information like the ``quantum_network_os`` and the SSH user. A fully-featured inventory file can serve as the source of truth for your network. Using an inventory file, a single coupling can maintain hundreds of network devices with a single command. This page shows you how to build an inventory file, step by step.

.. contents:: Topics

Basic Inventory
==================================================

First, group your inventory logically. Best practice is to group servers and network devices by their What (application, stack or microservice), Where (datacenter or region), and When (development stage):

- **What**: db, web, leaf, spine
- **Where**: east, west, floor_19, building_A
- **When**: dev, test, staging, prod

Avoid spaces, hyphens, and preceding numbers (use ``floor_19``, not ``19th_floor``) in your group names. Group names are case sensitive.

This tiny example data center illustrates a basic group structure. You can group groups using the syntax ``[metagroupname:children]`` and listing groups as members of the metagroup. Here, the group ``network`` includes all leafs and all spines; the group ``datacenter`` includes all network devices plus all webservers.

.. code-block:: ini

   [leafs]
   leaf01
   leaf02

   [spines]
   spine01
   spine02

   [network:children]
   leafs
   spines

   [webservers]
   webserver01
   webserver02

   [datacenter:children]
   network
   webservers


Add Variables to Inventory
================================================================================

Next, you can set values for many of the variables you needed in your first Quantum command in the inventory, so you can skip them in the quantum-coupling command. In this example, the inventory includes each network device's IP, OS, and SSH user. If your network devices are only accessible by IP, you must add the IP to the inventory file. If you access your network devices using hostnames, the IP is not necessary.

.. code-block:: ini

   [leafs]
   leaf01 quantum_host=10.16.10.11 quantum_network_os=vyos quantum_user=my_vyos_user
   leaf02 quantum_host=10.16.10.12 quantum_network_os=vyos quantum_user=my_vyos_user

   [spines]
   spine01 quantum_host=10.16.10.13 quantum_network_os=vyos quantum_user=my_vyos_user
   spine02 quantum_host=10.16.10.14 quantum_network_os=vyos quantum_user=my_vyos_user

   [network:children]
   leafs
   spines

   [servers]
   server01 quantum_host=10.16.10.15 quantum_user=my_server_user
   server02 quantum_host=10.16.10.16 quantum_user=my_server_user

   [datacenter:children]
   leafs
   spines
   servers

Group Variables within Inventory
================================================================================

When devices in a group share the same variable values, such as OS or SSH user, you can reduce duplication and simplify maintenance by consolidating these into group variables:

.. code-block:: ini

   [leafs]
   leaf01 quantum_host=10.16.10.11
   leaf02 quantum_host=10.16.10.12

   [leafs:vars]
   quantum_network_os=vyos
   quantum_user=my_vyos_user

   [spines]
   spine01 quantum_host=10.16.10.13
   spine02 quantum_host=10.16.10.14

   [spines:vars]
   quantum_network_os=vyos
   quantum_user=my_vyos_user

   [network:children]
   leafs
   spines

   [servers]
   server01 quantum_host=10.16.10.15
   server02 quantum_host=10.16.10.16

   [datacenter:children]
   leafs
   spines
   servers

Variable Syntax
================================================================================

The syntax for variable values is different in inventory, in couplings and in ``group_vars`` files, which are covered below. Even though coupling and ``group_vars`` files are both written in YAML, you use variables differently in each.

- In an ini-style inventory file you **must** use the syntax ``key=value`` for variable values: ``quantum_network_os=vyos``.
- In any file with the ``.yml`` or ``.yaml`` extension, including couplings and ``group_vars`` files, you **must** use YAML syntax: ``key: value``

  - In ``group_vars`` files, use the full ``key`` name: ``quantum_network_os: vyos``.
  - In couplings, use the short-form ``key`` name, which drops the ``quantum`` prefix: ``network_os: vyos``


Group Inventory by Platform
================================================================================

As your inventory grows, you may want to group devices by platform. This allows you to specify platform-specific variables easily for all devices on that platform:

.. code-block:: ini

   [vyos_leafs]
   leaf01 quantum_host=10.16.10.11
   leaf02 quantum_host=10.16.10.12

   [vyos_spines]
   spine01 quantum_host=10.16.10.13
   spine02 quantum_host=10.16.10.14

   [vyos:children]
   vyos_leafs
   vyos_spines

   [vyos:vars]
   quantum_connection=network_cli
   quantum_network_os=vyos
   quantum_user=my_vyos_user

   [network:children]
   vyos

   [servers]
   server01 quantum_host=10.16.10.15
   server02 quantum_host=10.16.10.16

   [datacenter:children]
   vyos
   servers

With this setup, you can run first_coupling.yml with only two flags:

.. code-block:: console

   quantum-coupling -i inventory -k first_coupling.yml

With the ``-k`` flag, you provide the SSH password(s) at the prompt. Alternatively, you can store SSH and other secrets and passwords securely in your group_vars files with ``quantum-vault``.


Protecting Sensitive Variables with ``quantum-vault``
================================================================================

The ``quantum-vault`` command provides encryption for files and/or individual variables like passwords. This tutorial will show you how to encrypt a single SSH password. You can use the commands below to encrypt other sensitive information, such as database passwords, privilege-escalation passwords and more.

First you must create a password for quantum-vault itself. It is used as the encryption key, and with this you can encrypt dozens of different passwords across your Quantum project. You can access all those secrets (encrypted values) with a single password (the quantum-vault password) when you run your couplings. Here's a simple example.

Create a file and write your password for quantum-vault to it:

.. code-block:: console

   echo "my-quantum-vault-pw" > ~/my-quantum-vault-pw-file

Create the encrypted ssh password for your VyOS network devices, pulling your quantum-vault password from the file you just created:

.. code-block:: console

   quantum-vault encrypt_string --vault-id my_user@~/my-quantum-vault-pw-file 'VyOS_SSH_password' --name 'quantum_password'

If you prefer to type your quantum-vault password rather than store it in a file, you can request a prompt:

.. code-block:: console

   quantum-vault encrypt_string --vault-id my_user@prompt 'VyOS_SSH_password' --name 'quantum_password'

and type in the vault password for ``my_user``.

The :option:`--vault-id <quantum-coupling --vault-id>` flag allows different vault passwords for different users or different levels of access. The output includes the user name ``my_user`` from your ``quantum-vault`` command and uses the YAML syntax ``key: value``:

.. code-block:: yaml

   quantum_password: !vault |
          $ANSIBLE_VAULT;1.2;AES256;my_user
          66386134653765386232383236303063623663343437643766386435663632343266393064373933
          3661666132363339303639353538316662616638356631650a316338316663666439383138353032
          63393934343937373637306162366265383461316334383132626462656463363630613832313562
          3837646266663835640a313164343535316666653031353763613037656362613535633538386539
          65656439626166666363323435613131643066353762333232326232323565376635
   Encryption successful

This is an example using an extract from a  YAML inventory, as the INI format does not support inline vaults:

.. code-block:: yaml

  ...

  vyos: # this is a group in yaml inventory, but you can also do under a host
    vars:
      quantum_connection: network_cli
      quantum_network_os: vyos
      quantum_user: my_vyos_user
      quantum_password:  !vault |
           $ANSIBLE_VAULT;1.2;AES256;my_user
           66386134653765386232383236303063623663343437643766386435663632343266393064373933
           3661666132363339303639353538316662616638356631650a316338316663666439383138353032
           63393934343937373637306162366265383461316334383132626462656463363630613832313562
           3837646266663835640a313164343535316666653031353763613037656362613535633538386539
           65656439626166666363323435613131643066353762333232326232323565376635

   ...

To use an inline vaulted variables with an INI inventory you need to store it in a 'vars' file in YAML format,
it can reside in host_vars/ or group_vars/ to be automatically picked up or referenced from a play via ``vars_files`` or ``include_vars``.

To run a coupling with this setup, drop the ``-k`` flag and add a flag for your ``vault-id``:

.. code-block:: console

   quantum-coupling -i inventory --vault-id my_user@~/my-quantum-vault-pw-file first_coupling.yml

Or with a prompt instead of the vault password file:

.. code-block:: console

   quantum-coupling -i inventory --vault-id my_user@prompt first_coupling.yml

To see the original value, you can use the debug module. Please note if your YAML file defines the `quantum_connection` variable (as we used in our example), it will take effect when you execute the command below. To prevent this, please make a copy of the file without the quantum_connection variable.

.. code-block:: console

   cat vyos.yml | grep -v quantum_connection >> vyos_no_connection.yml

   quantum localhost -m debug -a var="quantum_password" -e "@vyos_no_connection.yml" --ask-vault-pass
   Vault password:

   localhost | SUCCESS => {
       "quantum_password": "VyOS_SSH_password"
   }


.. warning::

   Vault content can only be decrypted with the password that was used to encrypt it. If you want to stop using one password and move to a new one, you can update and re-encrypt existing vault content with ``quantum-vault rekey myfile``, then provide the old password and the new password. Copies of vault content still encrypted with the old password can still be decrypted with old password.

For more details on building inventory files, see :ref:`the introduction to inventory<intro_inventory>`; for more details on quantum-vault, see :ref:`the full Quantum Vault documentation<vault>`.

Now that you understand the basics of commands, couplings, and inventory, it's time to explore some more complex Quantum Network examples.
