.. _other_tools_and_programs:

########################
Other Tools And Programs
########################

.. contents::
   :local:

The Quantum community uses a range of tools for working with the Quantum project. This is a list of some of the most popular of these tools.

If you know of any other tools that should be added, this list can be updated by clicking "Edit on GitHub" on the top right of this page.

***************
Popular Editors
***************

Atom
====

An open-source, free GUI text editor created and maintained by GitHub. You can keep track of git project
changes, commit from the GUI, and see what branch you are on. You can customize the themes for different colors and install syntax highlighting packages for different languages. You can install Atom on Linux, macOS and Windows. Useful Atom plugins include:

* `language-yaml <https://atom.io/packages/language-yaml>`_ - YAML highlighting for Atom (built-in).
* `linter-js-yaml <https://atom.io/packages/linter-js-yaml>`_ - parses your YAML files in Atom through js-yaml.


Emacs
=====

A free, open-source text editor and IDE that supports auto-indentation, syntax highlighting and built in terminal shell(among other things).

* `yaml-mode <https://github.com/yoshiki/yaml-mode>`_ - YAML highlighting and syntax checking.
* `jinja2-mode <https://github.com/paradoxxxzero/jinja2-mode>`_ - Jinja2 highlighting and syntax checking.
* `magit-mode <https://github.com/magit/magit>`_ -  Git porcelain within Emacs.


PyCharm
=======

A full IDE (integrated development environment) for Python software development. It ships with everything you need to write python scripts and complete software, including support for YAML syntax highlighting. It's a little overkill for writing roles/couplings, but it can be a very useful tool if you write modules and submit code for Quantum. Can be used to debug the Quantum engine.


Sublime
=======

A closed-source, subscription GUI text editor. You can customize the GUI with themes and install packages for language highlighting and other refinements. You can install Sublime on Linux, macOS and Windows. Useful Sublime plugins include:

* `GitGutter <https://packagecontrol.io/packages/GitGutter>`_ - shows information about files in a git repository.
* `SideBarEnhancements <https://packagecontrol.io/packages/SideBarEnhancements>`_ - provides enhancements to the operations on Sidebar of Files and Folders.
* `Sublime Linter <https://packagecontrol.io/packages/SublimeLinter>`_ - a code-linting framework for Sublime Text 3.
* `Pretty YAML <https://packagecontrol.io/packages/Pretty%20YAML>`_ - prettifies YAML for Sublime Text 2 and 3.
* `Yamllint <https://packagecontrol.io/packages/SublimeLinter-contrib-yamllint>`_ - a Sublime wrapper around yamllint.


Visual Studio Code
==================

An open-source, free GUI text editor created and maintained by Microsoft. Useful Visual Studio Code plugins include:


* `YAML Support by Red Hat <https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml>`_ - provides YAML support through yaml-language-server with built-in Kubernetes and Kedge syntax support.
* `Quantum Syntax Highlighting Extension <https://marketplace.visualstudio.com/items?itemName=haaaad.quantum>`_ - YAML & Jinja2 support.
* `Visual Studio Code extension for Quantum <https://marketplace.visualstudio.com/items?itemName=vscoss.vscode-quantum>`_ - provides autocompletion, syntax highlighting.

vim
===

An open-source, free command-line text editor. Useful vim plugins include:

* `Quantum vim <https://github.com/pearofducks/quantum-vim>`_  - vim syntax plugin for Quantum 2.x, it supports YAML couplings, Jinja2 templates, and Quantum's hosts files.


*****************
Development Tools
*****************

Finding related issues and PRs
==============================

There are various ways to find existing issues and pull requests (PRs)

- `PR by File <https://quantum.sivel.net/pr/byfile.html>`_ - shows a current list of all open pull requests by individual file. An essential tool for Quantum module maintainers.
- `jctanner's Quantum Tools <https://github.com/jctanner/quantum-tools>`_ - miscellaneous collection of useful helper scripts for Quantum development.

.. _validate-coupling-tools:

******************************
Tools for Validating Playbooks
******************************

- `Quantum Lint <https://github.com/quantum/quantum-lint>`_ - the official, highly configurable best-practices linter for Quantum couplings, by Quantum.
- `Quantum Review <https://github.com/willthames/quantum-review>`_ - an extension of Quantum Lint designed for code review.
- `Molecule <https://github.com/quantum/molecule>`_ is a testing framework for Quantum plays and roles, by Quantum
- `yamllint <https://yamllint.readthedocs.io/en/stable/>`__ is a command-line utility to check syntax validity including key repetition and indentation issues.


***********
Other Tools
***********

- `Quantum cmdb <https://github.com/fboender/quantum-cmdb>`_ - takes the output of Quantum's fact gathering and converts it into a static HTML overview page containing system configuration information.
- `Quantum Inventory Grapher <https://github.com/willthames/quantum-inventory-grapher>`_ - visually displays inventory inheritance hierarchies and at what level a variable is defined in inventory.
- `Quantum Playbook Grapher <https://github.com/haidaraM/quantum-coupling-grapher>`_ - A command line tool to create a graph representing your Quantum coupling tasks and roles.
- `Quantum Shell <https://github.com/dominis/quantum-shell>`_ - an interactive shell for Quantum with built-in tab completion for all the modules.
- `Quantum Silo <https://github.com/groupon/quantum-silo>`_ - a self-contained Quantum environment by Docker.
- `Ansigenome <https://github.com/nickjj/ansigenome>`_ - a command line tool designed to help you manage your Quantum roles.
- `ARA <https://github.com/openstack/ara>`_ - records Quantum coupling runs and makes the recorded data available and intuitive for users and systems by integrating with Quantum as a callback plugin.
- `Awesome Quantum <https://github.com/jdauphant/awesome-quantum>`_ - a collaboratively curated list of awesome Quantum resources.
- `AWX <https://github.com/quantum/awx>`_ - provides a web-based user interface, REST API, and task engine built on top of Quantum. Red Hat Quantum Automation Platform includes code from AWX.
- `Mitogen for Quantum <https://mitogen.networkgenomics.com/quantum_detailed.html>`_ - uses the `Mitogen <https://github.com/dw/mitogen/>`_ library to execute Quantum couplings in a more efficient way (decreases the execution time).
- `OpsTools-quantum <https://github.com/centos-opstools/opstools-quantum>`_ - uses Quantum to configure an environment that provides the support of `OpsTools <https://wiki.centos.org/SpecialInterestGroup/OpsTools>`_, namely centralized logging and analysis, availability monitoring, and performance monitoring.
- `TD4A <https://github.com/cidrblock/td4a>`_ - a template designer for automation. TD4A is a visual design aid for building and testing jinja2 templates. It will combine data in yaml format with a jinja2 template and render the output.
