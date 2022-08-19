*****************
Beyond the basics
*****************

This page introduces some concepts that help you manage your Quantum workflow with directory structure and source control. Like the Basic Concepts at the beginning of this guide, these intermediate concepts are common to all uses of Quantum.

.. contents::
   :local:


A typical Quantum filetree
==========================

Quantum expects to find certain files in certain places. As you expand your inventory and create and run more network couplings, keep your files organized in your working Quantum project directory like this:

.. code-block:: console

   .
   ├── backup
   │   ├── vyos.example.net_config.2018-02-08@11:10:15
   │   ├── vyos.example.net_config.2018-02-12@08:22:41
   ├── first_coupling.yml
   ├── inventory
   ├── group_vars
   │   ├── vyos.yml
   │   └── eos.yml
   ├── roles
   │   ├── static_route
   │   └── system
   ├── second_coupling.yml
   └── third_coupling.yml

The ``backup`` directory and the files in it get created when you run modules like ``vyos_config`` with the ``backup: yes`` parameter.


Tracking changes to inventory and couplings: source control with git
====================================================================

As you expand your inventory, roles and couplings, you should place your Quantum projects under source control. We recommend ``git`` for source control. ``git`` provides an audit trail, letting you track changes, roll back mistakes, view history and share the workload of managing, maintaining and expanding your Quantum ecosystem. There are plenty of tutorials and guides to using ``git`` available.
