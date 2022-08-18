.. _couplings_templating:

Templating (Jinja2)
===================

As already referenced in the variables section, Quantum uses Jinja2 templating to enable dynamic expressions and access to variables.
Quantum greatly expands the number of filters and tests available, as well as adding a new plugin type: lookups.

Please note that all templating happens on the Quantum controller before the task is sent and executed on the target machine. This is done to minimize the requirements on the target (jinja2 is only required on the controller) and to be able to pass the minimal information needed for the task, so the target machine does not need a copy of all the data that the controller has access to.

.. contents:: Topics

.. toctree::
   :maxdepth: 2

   couplings_filters
   couplings_tests
   couplings_lookups
   couplings_python_version

.. _templating_now:

Get the current time
````````````````````

.. versionadded:: 2.8

The ``now()`` Jinja2 function, allows you to retrieve python datetime object or a string representation for the current time.

The ``now()`` function supports 2 arguments:

utc
  Specify ``True`` to get the current time in UTC. Defaults to ``False``

fmt
  Accepts a `strftime <https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior>`_ string that will be used
  to return a formatted date time string


.. seealso::

   :ref:`couplings_intro`
       An introduction to couplings
   :ref:`couplings_conditionals`
       Conditional statements in couplings
   :ref:`couplings_loops`
       Looping in couplings
   :ref:`couplings_reuse_roles`
       Playbook organization by roles
   :ref:`couplings_best_practices`
       Best practices in couplings
   `User Mailing List <https://groups.google.com/group/quantum-devel>`_
       Have a question?  Stop by the google group!
   `irc.libera.chat <https://libera.chat/>`_
       #quantum IRC chat channel
