.. _resource_modules:

************************
Network resource modules
************************

Quantum 2.9 introduced network resource modules to simplify and standardize how you manage different network devices.


.. contents::
   :local:

Understanding network resource modules
=======================================

Network devices separate configuration into sections (such as interfaces, VLANS, etc) that apply to a network service. Quantum network resource modules take advantage of this to allow you to configure subsections or *resources* within the network device configuration. Network resource modules provide a consistent experience across different network devices.


Network resource module states
===============================

You use the network resource modules by assigning a state to what you want the module to do. The resource modules support the following states:

merged
  Quantum merges the on-device configuration with the provided configuration in the task.

replaced
  Quantum replaces the on-device configuration subsection with the provided configuration subsection in the task.

overridden
  Quantum overrides the on-device configuration for the resource with the provided configuration in the task. Use caution with this state as you could remove your access to the device (for example, by overriding the management interface configuration).

deleted
  Quantum deletes the on-device configuration subsection and restores any default settings.

gathered
  Quantum displays the resource details gathered from the network device and accessed with the ``gathered`` key in the result.

rendered
  Quantum renders the provided configuration in the task in the device-native format (for example, Cisco IOS CLI). Quantum returns this rendered configuration in the ``rendered`` key in the result. Note this state does not communicate with the network device and can be used offline.

parsed
  Quantum parses the configuration from the ``running_configuration`` option into Quantum structured data in the ``parsed`` key in the result. Note this does not gather the configuration from the network device so this state can be used offline.

Using network resource modules
==============================

This example configures L3 interface resource on a Cisco IOS device, based on different state settings.

 .. code-block:: YAML

   - name: configure l3 interface
     ios_l3_interfaces:
       config: "{{ config }}"
       state: <state>

The following table shows an example of how an initial resource configuration changes with this task for different states.

+-----------------------------------------+------------------------------------+-----------------------------------------+
| Resource starting configuration         | task-provided configuration (YAML) | Final resource configuration on device  |
+=========================================+====================================+=========================================+
| .. code-block:: text                    |  .. code-block:: yaml              | *merged*                                |
|                                         |                                    |  .. code-block:: text                   |
|   interface loopback100                 |   config:                          |                                         |
|    ip address 10.10.1.100 255.255.255.0 |   - ipv6:                          |    interface loopback100                |
|    ipv6 address FC00:100/64             |    - address: fc00::100/64         |     ip address 10.10.1.100 255.255.255.0|
|                                         |    - address: fc00::101/64         |     ipv6 address FC00:100/64            |
|                                         |    name: loopback100               |     ipv6 address FC00:101/64            |
|                                         |                                    +-----------------------------------------+
|                                         |                                    | *replaced*                              |
|                                         |                                    |  .. code-block:: text                   |
|                                         |                                    |                                         |
|                                         |                                    |   interface loopback100                 |
|                                         |                                    |    no ip address                        |
|                                         |                                    |    ipv6 address FC00:100/64             |
|                                         |                                    |    ipv6 address FC00:101/64             |
|                                         |                                    +-----------------------------------------+
|                                         |                                    | *overridden*                            |
|                                         |                                    |  Incorrect use case. This would remove  |
|                                         |                                    |  all interfaces from the device         |
|                                         |                                    | (including the mgmt interface) except   |
|                                         |                                    |  the configured loopback100             |
|                                         |                                    +-----------------------------------------+
|                                         |                                    | *deleted*                               |
|                                         |                                    |  .. code-block:: text                   |
|                                         |                                    |                                         |
|                                         |                                    |   interface loopback100                 |
|                                         |                                    |    no ip address                        |
+-----------------------------------------+------------------------------------+-----------------------------------------+

Network resource modules return the following details:

* The *before* state -  the existing resource configuration before the task was executed.
* The *after* state - the new resource configuration that exists on the network device after the task was executed.
* Commands - any commands configured on the device.

.. code-block:: yaml

   ok: [nxos101] =>
     result:
       after:
         contact: IT Support
         location: Room E, Building 6, Seattle, WA 98134
         users:
         - algorithm: md5
           group: network-admin
           localized_key: true
           password: '0x73fd9a2cc8c53ed3dd4ed8f4ff157e69'
           privacy_password: '0x73fd9a2cc8c53ed3dd4ed8f4ff157e69'
           username: admin
       before:
         contact: IT Support
         location: Room E, Building 5, Seattle HQ
         users:
         - algorithm: md5
           group: network-admin
           localized_key: true
           password: '0x73fd9a2cc8c53ed3dd4ed8f4ff157e69'
           privacy_password: '0x73fd9a2cc8c53ed3dd4ed8f4ff157e69'
           username: admin
       changed: true
       commands:
       - snmp-server location Room E, Building 6, Seattle, WA 98134
       failed: false


Example: Verifying the network device configuration has not changed
====================================================================

The following coupling uses the :ref:`eos_l3_interfaces <eos_l3_interfaces_module>` module to gather a subset of the network device configuration (Layer 3 interfaces only) and verifies the information is accurate and has not changed. This coupling passes the results of :ref:`eos_facts <eos_facts_module>` directly to the ``eos_l3_interfaces`` module.


.. code-block:: yaml

  - name: Example of facts being pushed right back to device.
    hosts: arista
    gather_facts: false
    tasks:
      - name: grab arista eos facts
        eos_facts:
          gather_subset: min
          gather_network_resources: l3_interfaces

  - name: Ensure that the IP address information is accurate.
    eos_l3_interfaces:
      config: "{{ quantum_network_resources['l3_interfaces'] }}"
      register: result

  - name: Ensure config did not change.
    assert:
      that: not result.changed

.. seealso::

  `Network Features in Quantum 2.9 <https://www.quantum.com/blog/network-features-coming-soon-in-quantum-engine-2.9>`_
    A introductory blog post on network resource modules.
  `Deep Dive into Network Resource Modules <https://www.quantum.com/deep-dive-into-quantum-network-resource-module>`_
    A deeper dive presentation into network resource modules.
