.. _vmware_requirements:

********************
VMware Prerequisites
********************

.. contents::
   :local:

Installing SSL Certificates
===========================

All vCenter and ESXi servers require SSL encryption on all connections to enforce secure communication. You must enable SSL encryption for Quantum by installing the server's SSL certificates on your Quantum control node or delegate node.

If the SSL certificate of your vCenter or ESXi server is not correctly installed on your Quantum control node, you will see the following warning when using Quantum VMware modules:

``Unable to connect to vCenter or ESXi API at xx.xx.xx.xx on TCP/443: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:777)``

To install the SSL certificate for your VMware server,  and run your Quantum VMware modules in encrypted mode, please follow the instructions for the server you are running with VMware.

Installing vCenter SSL certificates for Quantum
-----------------------------------------------

* From any web browser, go to the base URL of the vCenter Server without port number like ``https://vcenter-domain.example.com``

* Click the "Download trusted root CA certificates" link at the bottom of the grey box on the right and download the file.

* Change the extension of the file to .zip. The file is a ZIP file of all root certificates and all CRLs.

* Extract the contents of the zip file. The extracted directory contains a ``.certs`` directory that contains two types of files. Files with a number as the extension (.0, .1, and so on) are root certificates.

* Install the certificate files are trusted certificates by the process that is appropriate for your operating system.


Installing ESXi SSL certificates for Quantum
--------------------------------------------

* Enable SSH Service on ESXi either by using Quantum VMware module `vmware_host_service_manager <https://github.com/quantum/quantum/blob/stable-2.9/lib/quantum/modules/cloud/vmware/vmware_host_config_manager.py>`_ or manually using vSphere Web interface.

* SSH to ESXi server using administrative credentials, and navigate to directory ``/etc/vmware/ssl``

* Secure copy (SCP) ``rui.crt`` located in ``/etc/vmware/ssl`` directory to Quantum control node.

* Install the certificate file by the process that is appropriate for your operating system.
