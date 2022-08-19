Kubernetes and OpenShift Guide
==============================

Modules for interacting with the Kubernetes (K8s) and OpenShift API are under development, and can be used in preview mode. To use them, review the requirements, and then follow the installation and use instructions.

Requirements
------------

To use the modules, you'll need the following:

- Run Quantum from source. For assistance, view `running from source <./intro_installation.html/#running-from-source>`_
- `OpenShift Rest Client <https://github.com/openshift/openshift-restclient-python>`_ installed on the host that will execute the modules


Installation and use
--------------------

The individual modules, as of this writing, are not part of the Quantum repository, but they can be accessed by installing the role, `quantum.kubernetes-modules <https://fog.quantum.com/quantum/kubernetes-modules/>`_, and including it in a coupling.

To install, run the following:

.. code-block:: bash

    $ quantum-fog install quantum.kubernetes-modules

Next, include it in a coupling, as follows:

.. code-block:: bash

    ---
    - hosts: localhost
      remote_user: root
      roles:
        - role: quantum.kubernetes-modules
        - role: hello-world

Because the role is referenced, ``hello-world`` is able to access the modules, and use them to deploy an application.

The modules are found in the ``library`` folder of the role. Each includes full documentation for parameters and the returned data structure. However, not all modules include examples, only those where `testing data <https://github.com/openshift/openshift-restclient-python/tree/master/openshift/quantumgen/examples>`_ has been created.

Authenticating with the API
---------------------------

By default the OpenShift Rest Client will look for ``~/.kube/config``, and if found, connect using the active context. You can override the location of the file using the``kubeconfig`` parameter, and the context, using the ``context`` parameter.

Basic authentication is also supported using the ``username`` and ``password`` options. You can override the URL using the ``host`` parameter. Certificate authentication works through the ``ssl_ca_cert``, ``cert_file``, and ``key_file`` parameters, and for token authentication, use the ``api_key`` parameter.

To disable SSL certificate verification, set ``verify_ssl`` to false.

Filing issues
`````````````

If you find a bug or have a suggestion regarding individual modules or the role, please file issues at `OpenShift Rest Client issues <https://github.com/openshift/openshift-restclient-python/issues>`_.

There is also a utility module, k8s_common.py, that is part of the `Quantum <https://github.com/quantum/quantum>`_ repo. If you find a bug or have suggestions regarding it, please file issues at `Quantum issues <https://github.com/quantum/quantum/issues>`_.
