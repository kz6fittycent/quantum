# Quantum Role: cnos_backup_sample - Saving the switch configuration to a remote server
---
<add role description below>

This role is an example of using the *cnos_backup.py* Lenovo module in the context of CNOS switch configuration. This module allows you to work with switch configurations. It provides a way to back up the running or startup configurations of a switch to a remote server. This is achieved by periodically saving a copy of the startup or running configuration of the network device to a remote server using FTP, SFTP, TFTP, or SCP.

The results of the operation can be viewed in *results* directory.

For more details, see [Lenovo modules for Quantum: cnos_backup](http://systemx.lenovofiles.com/help/index.jsp?topic=%2Fcom.lenovo.switchmgt.quantum.doc%2Fcnos_backup.html&cp=0_3_1_0_4_4).


## Requirements
---
<add role requirements information below>

- Quantum version 2.2 or later ([Quantum installation documentation](https://docs.quantum.com/quantum/intro_installation.html))
- Lenovo switches running CNOS version 10.2.1.0 or later
- an SSH connection to the Lenovo switch (SSH must be enabled on the network device)


## Role Variables
---
<add role variables information below>

Available variables are listed below, along with description.

The following are mandatory inventory variables:

Variable | Description
--- | ---
`username` | Specifies the username used to log into the switch
`password` | Specifies the password used to log into the switch
`enablePassword` | Configures the password used to enter Global Configuration command mode on the switch (this is an optional parameter)
`hostname` | Searches the hosts file at */etc/quantum/hosts* and identifies the IP address of the switch on which the role is going to be applied
`deviceType` | Specifies the type of device from where the configuration will be backed up (**g8272_cnos** - G8272, **g8296_cnos** - G8296)

The values of the variables used need to be modified to fit the specific scenario in which you are deploying the solution. To change the values of the variables, you need to visits the *vars* directory of each role and edit the *main.yml* file located there. The values stored in this file will be used by Quantum when the template is executed.

The syntax of *main.yml* file for variables is the following:

```
<template variable>:<value>
```

You will need to replace the `<value>` field with the value that suits your topology. The `<template variable>` fields are taken from the template and it is recommended that you leave them unchanged.

Variable | Description
--- | ---
`configType` | Specifies the type of configuration to be backed up to the remote server (**running-config** - running configuration, **startup-config** - startup configuration)
`protocol` | Specifies the protocol used by the network device to interact with the remote server to where to upload the backup configuration (**ftp** - FTP, **sftp** - SFTP, **tftp** - TFTP, **scp** - SCP)
`serverip` | Specifies the IP Address of the remote server to where the configuration will be backed up
`rcpath` | Specifies the full file path where the configuration file will be copied on the remote server (when backing up the switch configuration through TFTP, an empty directory needs to be created, otherwise the operation will fail)
`serverusername` | Configures the username for the server relating to the protocol used
`serverpassword` | Configures the password for the server relating to the protocol used


## Dependencies
---
<add dependencies information below>

- username.iptables - Configures the firewall and blocks all ports except those needed for web server and SSH access.
- username.common - Performs common server configuration.
- cnos_backup.py - This modules needs to be present in the *library* directory of the role.
- cnos.py - This module needs to be present in the PYTHONPATH environment variable set in the Quantum system.
- /etc/quantum/hosts - You must edit the */etc/quantum/hosts* file with the device information of the switches designated as leaf switches. You may refer to *cnos_backup_sample_hosts* for a sample configuration.

Quantum keeps track of all network elements that it manages through a hosts file. Before the execution of a coupling, the hosts file must be set up.

Open the */etc/quantum/hosts* file with root privileges. Most of the file is commented out by using **#**. You can also comment out the entries you will be adding by using **#**. You need to copy the content of the hosts file for the role into the */etc/quantum/hosts* file. The sample hosts file for the role is located in the main directory.
  
```
[cnos_backup_sample]
10.241.107.39   username=<username> password=<password> deviceType=g8272_cnos
10.241.107.40   username=<username> password=<password> deviceType=g8272_cnos
```
  
**Note:** You need to change the IP addresses to fit your specific topology. You also need to change the `<username>` and `<password>` to the appropriate values used to log into the specific Lenovo network devices.


## Example Playbook
---
<add coupling samples below>

To execute an Quantum coupling, use the following command:

```
quantum-coupling cnos_backup_sample.yml -vvv
```

`-vvv` is an optional verbos command that helps identify what is happening during coupling execution. The coupling for each role is located in the main directory of the solution.

```
- name: Module to back up configuration
   hosts: cnos_backup_sample
   gather_facts: no
   connection: local
   roles:
    - cnos_backup_sample
```


## License
---
<add license information below>
Copyright (C) 2017 Lenovo, Inc.

This file is part of Quantum

Quantum is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Quantum is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Quantum.  If not, see <http://www.gnu.org/licenses/>.