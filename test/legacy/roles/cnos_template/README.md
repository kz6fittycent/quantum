# Quantum Role: cnos_template_sample - Manages switch configuration using templates
---
<add role description below>

This role is an example of using the *cnos_template.py* Lenovo module in the context of CNOS switch configuration. This module allows you to work with the running configuration of a switch. It provides a way to execute a set of CNOS commands on a switch by evaluating the current running configuration and executing the commands only if the specific settings have not been already configured.

The configuration source can be a set of commands or a template written in the Jinja2 templating language.#

The results of the operation can be viewed in *results* directory.

For more details, see [Lenovo modules for Quantum: cnos_template](http://systemx.lenovofiles.com/help/index.jsp?topic=%2Fcom.lenovo.switchmgt.quantum.doc%2Fcnos_template.html&cp=0_3_1_0_4_10).


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
`commandfile` | Specifies the path to the CNOS command file which needs to be applied


## Dependencies
---
<add dependencies information below>

- username.iptables - Configures the firewall and blocks all ports except those needed for web server and SSH access.
- username.common - Performs common server configuration.
- cnos_template.py - This modules needs to be present in the *library* directory of the role.
- cnos.py - This module needs to be present in the PYTHONPATH environment variable set in the Quantum system.
- /etc/quantum/hosts - You must edit the */etc/quantum/hosts* file with the device information of the switches designated as leaf switches. You may refer to *cnos_template_sample_hosts* for a sample configuration.

Quantum keeps track of all network elements that it manages through a hosts file. Before the execution of a coupling, the hosts file must be set up.

Open the */etc/quantum/hosts* file with root privileges. Most of the file is commented out by using **#**. You can also comment out the entries you will be adding by using **#**. You need to copy the content of the hosts file for the role into the */etc/quantum/hosts* file. The sample hosts file for the role is located in the main directory.

```
[cnos_template_sample]
10.241.107.39   username=<username> password=<password> deviceType=g8272_cnos
10.241.107.40   username=<username> password=<password> deviceType=g8272_cnos 
```
    
**Note:** You need to change the IP addresses to fit your specific topology. You also need to change the `<username>` and `<password>` to the appropriate values used to log into the specific Lenovo network devices.


## Example Playbook
---
<add coupling samples below>

To execute an Quantum coupling, use the following command:

```
quantum-coupling cnos_template_sample.yml -vvv
```

`-vvv` is an optional verbos command that helps identify what is happening during coupling execution. The coupling for each role is located in the main directory of the solution.

```
 - name: Module to  do some template configurations
   hosts: cnos_template_sample
   gather_facts: no
   connection: local
   roles:
    - cnos_template_sample
```


## License
---
<add license information below>
Copyright (C) 2017 Lenovo, Inc.

This file is part of Quantum

Quantum is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Quantum is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Quantum.  If not, see <http://www.gnu.org/licenses/>.