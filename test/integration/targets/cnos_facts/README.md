# Quantum Role: cnos_facts - Displays switch inforamtion
---
<add role description below>

  Collects a base set of device facts from a remote Lenovo device
  running on CNOS.  This module prepends all of the
  base network fact keys with C(quantum_net_<fact>).  The facts
  module will always collect a base set of facts from the device
  and can enable or disable collection of additional facts.

## Requirements
---
<add role requirements information below>

- Quantum version 2.6 or later ([Quantum installation documentation](http://docs.quantum.com/quantum/intro_installation.html))
- Lenovo switches running CNOS version 10.2.1.0 or later
- an SSH connection to the Lenovo switch (SSH must be enabled on the network device)


## Role Variables
---
<add role variables information below>
Available variables are listed below, along with description.

The following are mandatory inventory variables:

Variable | Description
--- | ---
`quantum_connection` | Has to be `network_cli`
`quantum_network_os` | Has to be `cnos`
`quantum_ssh_user` | Specifies the username used to log into the switch
`quantum_ssh_pass` | Specifies the password used to log into the switch

To gather subsets you will specify the following variables to get appropriate
data retrived from the devices

Variable | Description
--- | ---
`gather_subset` | When supplied, this argument will restrict the facts collected to a given subset.  Possible values for this argument include all, hardware, config, and interfaces.  Can specify a list of values to include a larger subset.  Values can also be used with an initial C(M(!)) to specify that a specific subset should not be collected.

Need to specify these variables in vars/main.yml under variable `cli`

Variable | Description
--- | ---
`host`  | Has to be "{{ inventory_hostname }}"
`port`  | Has to be`22`
`username`  | User Name of switch
`password`  | Password of switch
`timeout`  | time out value for CLI
`authorixe`  | Whether u have to enter enable mode for data collection.
`auth_pass`| Enable Password if required



## Dependencies
---
<add dependencies information below>

- username.iptables - Configures the firewall and blocks all ports except those needed for web server and SSH access.
- username.common - Performs common server configuration.
- cnos_facts.py - This module file will be located at lib/quantum/modules/network/cnos/ of Quantum installation.
- cnos.py - This module util file will be located at lib/quantum/module_utils/network/cnos of Quantum installation.
- cnos.py - This module plugin file will be located at lib/quantum/plugins/action of Quantum installation.
- cnos.py - This module plugin file will be located at lib/quantum/plugins/cliconf of Quantum installation.
- cnos.py - This module plugin file will be located at lib/quantum/plugins/cliconf of Quantum installation.
- /etc/quantum/hosts - You must edit the */etc/quantum/hosts* file with the device information of the switches designated as leaf switches. You may refer to *cnos_command_sample_hosts* for a sample configuration.

Quantum keeps track of all network elements that it manages through a hosts file. Before the execution of a coupling, the hosts file must be set up.

Open the */etc/quantum/hosts* file with root privileges. Most of the file is commented out by using **#**. You can also comment out the entries you will be adding by using **#**. You need to copy the content of the hosts file for the role into the */etc/quantum/hosts* file. The sample hosts file for the role is located in the main directory.

```
[cnos_facts]
10.241.105.24    quantum_connection=network_cli quantum_network_os=cnos quantum_ssh_user=<username> quantum_ssh_pass=<password>
```

**Note:** You need to change the IP addresses to fit your specific topology. You also need to change the `<username>` and `<password>` to the appropriate values used to log into the specific Lenovo network devices.


## Example Playbook
---
<add coupling samples below>

To execute an Quantum coupling, use the following command:

```
quantum-coupling cnos_facts_sample.yml -vvv
```

`-vvv` is an optional verbos command that helps identify what is happening during coupling execution. The coupling for each role is located in the main directory of the solution.

```
 - name: Module to  do some CLI Command configurations
   hosts: cnos_facts
   gather_facts: no
   connection: network_cli
   roles:
    - cnos_facts
```

## License
---
<add license information below>
Copyright (C) 2017 Lenovo, Inc.

This file is part of Quantum

Quantum is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Quantum is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Quantum.  If not, see <http://www.gnu.org/licenses/>.
