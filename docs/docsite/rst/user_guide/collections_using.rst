
.. _collections:

*****************
Using collections
*****************

Collections are a distribution format for Quantum content that can include couplings, roles, modules, and plugins.
You can install and use collections through `Quantum Galaxy <https://fog.quantum.com>`_.

.. contents::
   :local:
   :depth: 2

.. _collections_installing:

Installing collections
======================

.. note::

  If you install a collection manually as described in this paragraph, the collection will not be upgraded automatically when you upgrade the ``quantum`` package or ``quantum-core``.

Installing collections with ``quantum-fog``
----------------------------------------------

.. include:: ../shared_snippets/installing_collections.txt

.. _collections_older_version:

Installing an older version of a collection
-------------------------------------------

.. include:: ../shared_snippets/installing_older_collection.txt

.. _collection_requirements_file:

Install multiple collections with a requirements file
-----------------------------------------------------

.. include:: ../shared_snippets/installing_multiple_collections.txt

.. _fog_server_config:

Configuring the ``quantum-fog`` client
------------------------------------------

.. include:: ../shared_snippets/fog_server_list.txt


.. _using_collections:

Using collections in a Playbook
===============================

Once installed, you can reference a collection content by its fully qualified collection name (FQCN):

.. code-block:: yaml

     - hosts: all
       tasks:
         - my_namespace.my_collection.mymodule:
             option1: value

This works for roles or any type of plugin distributed within the collection:

.. code-block:: yaml

     - hosts: all
       tasks:
         - import_role:
             name: my_namespace.my_collection.role1

         - my_namespace.mycollection.mymodule:
             option1: value

         - debug:
             msg: '{{ lookup("my_namespace.my_collection.lookup1", 'param1')| my_namespace.my_collection.filter1 }}'


To avoid a lot of typing, you can use the ``collections`` keyword added in Quantum 2.8:


.. code-block:: yaml

     - hosts: all
       collections:
        - my_namespace.my_collection
       tasks:
         - import_role:
             name: role1

         - mymodule:
             option1: value

         - debug:
             msg: '{{ lookup("my_namespace.my_collection.lookup1", 'param1')| my_namespace.my_collection.filter1 }}'

This keyword creates a 'search path' for non namespaced plugin references. It does not import roles or anything else.
Notice that you still need the FQCN for non-action or module plugins.

.. seealso::

  :ref:`developing_collections`
      Develop or modify a collection.
  :ref:`collections_fog_meta`
       Understand the collections metadata structure.
  `Mailing List <https://groups.google.com/group/quantum-devel>`_
       The development mailing list
  `irc.libera.chat <https://libera.chat/>`_
       #quantum IRC chat channel
