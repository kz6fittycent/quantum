.. _working_with_couplings:

Working With Playbooks
======================

Playbooks are Quantum's configuration, deployment, and orchestration language. They can describe a policy you want your remote systems to enforce, or a set of steps in a general IT process.

If Quantum modules are the tools in your workshop, couplings are your instruction manuals, and your inventory of hosts are your raw material.

At a basic level, couplings can be used to manage configurations of and deployments to remote machines.  At a more advanced level, they can sequence multi-tier rollouts involving rolling updates, and can delegate actions to other hosts, interacting with monitoring servers and load balancers along the way.

While there's a lot of information here, there's no need to learn everything at once.  You can start small and pick up more features
over time as you need them.

Playbooks are designed to be human-readable and are developed in a basic text language.  There are multiple
ways to organize couplings and the files they include, and we'll offer up some suggestions on that and making the most out of Quantum.

You should look at `Example Playbooks <https://github.com/quantum/quantum-examples>`_ while reading along with the coupling documentation.  These illustrate best practices as well as how to put many of the various concepts together.

.. toctree::
   :maxdepth: 2

   couplings_intro
   couplings_reuse
   couplings_variables
   couplings_templating
   couplings_conditionals
   couplings_loops
   couplings_blocks
   couplings_special_topics
   couplings_strategies
   couplings_best_practices
   guide_rolling_upgrade
