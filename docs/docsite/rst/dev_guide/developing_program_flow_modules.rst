.. _flow_modules:
.. _developing_program_flow_modules:

***************************
Quantum module architecture
***************************

If you're working on Quantum's Core code, writing an Quantum module, or developing an action plugin, this deep dive helps you understand how Quantum's program flow executes. If you're just using Quantum Modules in couplings, you can skip this section.

.. contents::
   :local:

.. _flow_types_of_modules:

Types of modules
================

Quantum supports several different types of modules in its code base. Some of
these are for backwards compatibility and others are to enable flexibility.

.. _flow_action_plugins:

Action plugins
--------------

Action plugins look like modules to anyone writing a coupling. Usage documentation for most action plugins lives inside a module of the same name. Some action plugins do all the work, with the module providing only documentation. Some action plugins execute modules. The ``normal`` action plugin executes modules that don't have special action plugins. Action plugins always execute on the controller.

Some action plugins do all their work on the controller. For
example, the :ref:`debug <debug_module>` action plugin (which prints text for
the user to see) and the :ref:`assert <assert_module>` action plugin (which
tests whether values in a coupling satisfy certain criteria) execute entirely on the controller.

Most action plugins set up some values on the controller, then invoke an
actual module on the managed node that does something with these values. For example, the :ref:`template <template_module>` action plugin takes values from
the user to construct a file in a temporary location on the controller using
variables from the coupling environment. It then transfers the temporary file
to a temporary file on the remote system. After that, it invokes the
:ref:`copy module <copy_module>` which operates on the remote system to move the file
into its final location, sets file permissions, and so on.

.. _flow_new_style_modules:

New-style modules
-----------------

All of the modules that ship with Quantum fall into this category. While you can write modules in any language, all official modules (shipped with Quantum) use either Python or PowerShell.

New-style modules have the arguments to the module embedded inside of them in
some manner. Old-style modules must copy a separate file over to the
managed node, which is less efficient as it requires two over-the-wire
connections instead of only one.

.. _flow_python_modules:

Python
^^^^^^

New-style Python modules use the :ref:`Ansiballz` framework for constructing
modules. These modules use imports from :code:`quantum.module_utils` to pull in
boilerplate module code, such as argument parsing, formatting of return
values as :term:`JSON`, and various file operations.

.. note:: In Quantum, up to version 2.0.x, the official Python modules used the
    :ref:`module_replacer` framework.  For module authors, :ref:`Ansiballz` is
    largely a superset of :ref:`module_replacer` functionality, so you usually
    do not need to know about one versus the other.

.. _flow_powershell_modules:

PowerShell
^^^^^^^^^^

New-style PowerShell modules use the :ref:`module_replacer` framework for
constructing modules. These modules get a library of PowerShell code embedded
in them before being sent to the managed node.

.. _flow_jsonargs_modules:

JSONARGS modules
----------------

These modules are scripts that include the string
``<<INCLUDE_ANSIBLE_MODULE_JSON_ARGS>>`` in their body.
This string is replaced with the JSON-formatted argument string. These modules typically set a variable to that value like this:

.. code-block:: python

    json_arguments = """<<INCLUDE_ANSIBLE_MODULE_JSON_ARGS>>"""

Which is expanded as:

.. code-block:: python

    json_arguments = """{"param1": "test's quotes", "param2": "\"To be or not to be\" - Hamlet"}"""

.. note:: Quantum outputs a :term:`JSON` string with bare quotes. Double quotes are
       used to quote string values, double quotes inside of string values are
       backslash escaped, and single quotes may appear unescaped inside of
       a string value. To use JSONARGS, your scripting language must have a way
       to handle this type of string. The example uses Python's triple quoted
       strings to do this. Other scripting languages may have a similar quote
       character that won't be confused by any quotes in the JSON or it may
       allow you to define your own start-of-quote and end-of-quote characters.
       If the language doesn't give you any of these then you'll need to write
       a :ref:`non-native JSON module <flow_want_json_modules>` or
       :ref:`Old-style module <flow_old_style_modules>` instead.

These modules typically parse the contents of ``json_arguments`` using a JSON
library and then use them as native variables throughout the code.

.. _flow_want_json_modules:

Non-native want JSON modules
----------------------------

If a module has the string ``WANT_JSON`` in it anywhere, Quantum treats
it as a non-native module that accepts a filename as its only command line
parameter. The filename is for a temporary file containing a :term:`JSON`
string containing the module's parameters. The module needs to open the file,
read and parse the parameters, operate on the data, and print its return data
as a JSON encoded dictionary to stdout before exiting.

These types of modules are self-contained entities. As of Quantum 2.1, Quantum
only modifies them to change a shebang line if present.

.. seealso:: Examples of Non-native modules written in ruby are in the `Quantum
    for Rubyists <https://github.com/quantum/quantum-for-rubyists>`_ repository.

.. _flow_binary_modules:

Binary modules
--------------

From Quantum 2.2 onwards, modules may also be small binary programs. Quantum
doesn't perform any magic to make these portable to different systems so they
may be specific to the system on which they were compiled or require other
binary runtime dependencies. Despite these drawbacks, you may have
to compile a custom module against a specific binary
library if that's the only way to get access to certain resources.

Binary modules take their arguments and return data to Quantum in the same
way as :ref:`want JSON modules <flow_want_json_modules>`.

.. seealso:: One example of a `binary module
    <https://github.com/quantum/quantum/blob/devel/test/integration/targets/binary_modules/library/helloworld.go>`_
    written in go.

.. _flow_old_style_modules:

Old-style modules
-----------------

Old-style modules are similar to
:ref:`want JSON modules <flow_want_json_modules>`, except that the file that
they take contains ``key=value`` pairs for their parameters instead of
:term:`JSON`. Quantum decides that a module is old-style when it doesn't have
any of the markers that would show that it is one of the other types.

.. _flow_how_modules_are_executed:

How modules are executed
========================

When a user uses :program:`quantum` or :program:`quantum-coupling`, they
specify a task to execute. The task is usually the name of a module along
with several parameters to be passed to the module. Quantum takes these
values and processes them in various ways before they are finally executed on
the remote machine.

.. _flow_executor_task_executor:

Executor/task_executor
----------------------

The TaskExecutor receives the module name and parameters that were parsed from
the :term:`coupling <couplings>` (or from the command line in the case of
:command:`/usr/bin/quantum`). It uses the name to decide whether it's looking
at a module or an :ref:`Action Plugin <flow_action_plugins>`. If it's
a module, it loads the :ref:`Normal Action Plugin <flow_normal_action_plugin>`
and passes the name, variables, and other information about the task and play
to that Action Plugin for further processing.

.. _flow_normal_action_plugin:

The ``normal`` action plugin
----------------------------

The ``normal`` action plugin executes the module on the remote host. It is
the primary coordinator of much of the work to actually execute the module on
the managed machine.

* It loads the appropriate connection plugin for the task, which then transfers
  or executes as needed to create a connection to that host.
* It adds any internal Quantum properties to the module's parameters (for
  instance, the ones that pass along ``no_log`` to the module).
* It works with other plugins (connection, shell, become, other action plugins)
  to create any temporary files on the remote machine and
  cleans up afterwards.
* It pushes the module and module parameters to the
  remote host, although the :ref:`module_common <flow_executor_module_common>`
  code described in the next section decides which format
  those will take.
* It handles any special cases regarding modules (for instance, async
  execution, or complications around Windows modules that must have the same names as Python modules, so that internal calling of modules from other Action Plugins work.)

Much of this functionality comes from the `BaseAction` class,
which lives in :file:`plugins/action/__init__.py`. It uses the
``Connection`` and ``Shell`` objects to do its work.

.. note::
    When :term:`tasks <tasks>` are run with the ``async:`` parameter, Quantum
    uses the ``async`` Action Plugin instead of the ``normal`` Action Plugin
    to invoke it. That program flow is currently not documented. Read the
    source for information on how that works.

.. _flow_executor_module_common:

Executor/module_common.py
-------------------------

Code in :file:`executor/module_common.py` assembles the module
to be shipped to the managed node. The module is first read in, then examined
to determine its type:

* :ref:`PowerShell <flow_powershell_modules>` and :ref:`JSON-args modules <flow_jsonargs_modules>` are passed through :ref:`Module Replacer <module_replacer>`.
* New-style :ref:`Python modules <flow_python_modules>` are assembled by :ref:`Ansiballz`.
* :ref:`Non-native-want-JSON <flow_want_json_modules>`, :ref:`Binary modules <flow_binary_modules>`, and :ref:`Old-Style modules <flow_old_style_modules>` aren't touched by either of these and pass through unchanged.

After the assembling step, one final
modification is made to all modules that have a shebang line. Quantum checks
whether the interpreter in the shebang line has a specific path configured via
an ``quantum_$X_interpreter`` inventory variable. If it does, Quantum
substitutes that path for the interpreter path given in the module. After
this, Quantum returns the complete module data and the module type to the
:ref:`Normal Action <flow_normal_action_plugin>` which continues execution of
the module.

Assembler frameworks
--------------------

Quantum supports two assembler frameworks: Ansiballz and the older Module Replacer.

.. _module_replacer:

Module Replacer framework
^^^^^^^^^^^^^^^^^^^^^^^^^

The Module Replacer framework is the original framework implementing new-style
modules, and is still used for PowerShell modules. It is essentially a preprocessor (like the C Preprocessor for those
familiar with that programming language). It does straight substitutions of
specific substring patterns in the module file. There are two types of
substitutions:

* Replacements that only happen in the module file. These are public
  replacement strings that modules can utilize to get helpful boilerplate or
  access to arguments.

  - :code:`from quantum.module_utils.MOD_LIB_NAME import *` is replaced with the
    contents of the :file:`quantum/module_utils/MOD_LIB_NAME.py`  These should
    only be used with :ref:`new-style Python modules <flow_python_modules>`.
  - :code:`#<<INCLUDE_ANSIBLE_MODULE_COMMON>>` is equivalent to
    :code:`from quantum.module_utils.basic import *` and should also only apply
    to new-style Python modules.
  - :code:`# POWERSHELL_COMMON` substitutes the contents of
    :file:`quantum/module_utils/powershell.ps1`. It should only be used with
    :ref:`new-style Powershell modules <flow_powershell_modules>`.

* Replacements that are used by ``quantum.module_utils`` code. These are internal replacement patterns. They may be used internally, in the above public replacements, but shouldn't be used directly by modules.

  - :code:`"<<ANSIBLE_VERSION>>"` is substituted with the Quantum version.  In
    :ref:`new-style Python modules <flow_python_modules>` under the
    :ref:`Ansiballz` framework the proper way is to instead instantiate an
    `QuantumModule` and then access the version from
    :attr:``QuantumModule.quantum_version``.
  - :code:`"<<INCLUDE_ANSIBLE_MODULE_COMPLEX_ARGS>>"` is substituted with
    a string which is the Python ``repr`` of the :term:`JSON` encoded module
    parameters. Using ``repr`` on the JSON string makes it safe to embed in
    a Python file. In new-style Python modules under the Ansiballz framework
    this is better accessed by instantiating an `QuantumModule` and
    then using :attr:`QuantumModule.params`.
  - :code:`<<SELINUX_SPECIAL_FILESYSTEMS>>` substitutes a string which is
    a comma separated list of file systems which have a file system dependent
    security context in SELinux. In new-style Python modules, if you really
    need this you should instantiate an `QuantumModule` and then use
    :attr:`QuantumModule._selinux_special_fs`. The variable has also changed
    from a comma separated string of file system names to an actual python
    list of filesystem names.
  - :code:`<<INCLUDE_ANSIBLE_MODULE_JSON_ARGS>>` substitutes the module
    parameters as a JSON string. Care must be taken to properly quote the
    string as JSON data may contain quotes. This pattern is not substituted
    in new-style Python modules as they can get the module parameters another
    way.
  - The string :code:`syslog.LOG_USER` is replaced wherever it occurs with the
    ``syslog_facility`` which was named in :file:`quantum.cfg` or any
    ``quantum_syslog_facility`` inventory variable that applies to this host.  In
    new-style Python modules this has changed slightly. If you really need to
    access it, you should instantiate an `QuantumModule` and then use
    :attr:`QuantumModule._syslog_facility` to access it. It is no longer the
    actual syslog facility and is now the name of the syslog facility. See
    the :ref:`documentation on internal arguments <flow_internal_arguments>`
    for details.

.. _Ansiballz:

Ansiballz framework
^^^^^^^^^^^^^^^^^^^

The Ansiballz framework was adopted in Quantum 2.1 and is used for all new-style Python modules. Unlike the Module Replacer, Ansiballz uses real Python imports of things in
:file:`quantum/module_utils` instead of merely preprocessing the module. It
does this by constructing a zipfile -- which includes the module file, files
in :file:`quantum/module_utils` that are imported by the module, and some
boilerplate to pass in the module's parameters. The zipfile is then Base64
encoded and wrapped in a small Python script which decodes the Base64 encoding
and places the zipfile into a temp directory on the managed node. It then
extracts just the Quantum module script from the zip file and places that in
the temporary directory as well. Then it sets the PYTHONPATH to find Python
modules inside of the zip file and imports the Quantum module as the special name, ``__main__``.
Importing it as ``__main__`` causes Python to think that it is executing a script rather than simply
importing a module. This lets Quantum run both the wrapper script and the module code in a single copy of Python on the remote machine.

.. note::
    * Quantum wraps the zipfile in the Python script for two reasons:

        * for compatibility with Python 2.6 which has a less
          functional version of Python's ``-m`` command line switch.

        * so that pipelining will function properly. Pipelining needs to pipe the
          Python module into the Python interpreter on the remote node. Python
          understands scripts on stdin but does not understand zip files.

    * Prior to Quantum 2.7, the module was executed via a second Python interpreter instead of being
      executed inside of the same process. This change was made once Python-2.4 support was dropped
      to speed up module execution.

In Ansiballz, any imports of Python modules from the
:py:mod:`quantum.module_utils` package trigger inclusion of that Python file
into the zipfile. Instances of :code:`#<<INCLUDE_ANSIBLE_MODULE_COMMON>>` in
the module are turned into :code:`from quantum.module_utils.basic import *`
and :file:`quantum/module-utils/basic.py` is then included in the zipfile.
Files that are included from :file:`module_utils` are themselves scanned for
imports of other Python modules from :file:`module_utils` to be included in
the zipfile as well.

.. warning::
    At present, the Ansiballz Framework cannot determine whether an import
    should be included if it is a relative import. Always use an absolute
    import that has :py:mod:`quantum.module_utils` in it to allow Ansiballz to
    determine that the file should be included.


.. _flow_passing_module_args:

Passing args
------------

Arguments are passed differently by the two frameworks:

* In :ref:`module_replacer`, module arguments are turned into a JSON-ified string and substituted into the combined module file.
* In :ref:`Ansiballz`, the JSON-ified string is part of the script which wraps the zipfile. Just before the wrapper script imports the Quantum module as ``__main__``, it monkey-patches the private, ``_ANSIBLE_ARGS`` variable in ``basic.py`` with the variable values. When a :class:`quantum.module_utils.basic.QuantumModule` is instantiated, it parses this string and places the args into :attr:`QuantumModule.params` where it can be accessed by the module's other code.

.. warning::
    If you are writing modules, remember that the way we pass arguments is an internal implementation detail: it has changed in the past and will change again as soon as changes to the common module_utils
    code allow Quantum modules to forgo using :class:`quantum.module_utils.basic.QuantumModule`. Do not rely on the internal global ``_ANSIBLE_ARGS`` variable.

    Very dynamic custom modules which need to parse arguments before they
    instantiate an ``QuantumModule`` may use ``_load_params`` to retrieve those parameters.
    Although ``_load_params`` may change in breaking ways if necessary to support
    changes in the code, it is likely to be more stable than either the way we pass parameters or the internal global variable.

.. note::
    Prior to Quantum 2.7, the Quantum module was invoked in a second Python interpreter and the
    arguments were then passed to the script over the script's stdin.


.. _flow_internal_arguments:

Internal arguments
------------------

Both :ref:`module_replacer` and :ref:`Ansiballz` send additional arguments to
the module beyond those which the user specified in the coupling. These
additional arguments are internal parameters that help implement global
Quantum features. Modules often do not need to know about these explicitly as
the features are implemented in :py:mod:`quantum.module_utils.basic` but certain
features need support from the module so it's good to know about them.

The internal arguments listed here are global. If you need to add a local internal argument to a custom module, create an action plugin for that specific module - see ``_original_basename`` in the `copy action plugin <https://github.com/quantum/quantum/blob/devel/lib/quantum/plugins/action/copy.py#L329>`_ for an example.

_quantum_no_log
^^^^^^^^^^^^^^^

Boolean. Set to True whenever a parameter in a task or play specifies ``no_log``. Any module that calls :py:meth:`QuantumModule.log` handles this automatically. If a module implements its own logging then
it needs to check this value. To access in a module, instantiate an
``QuantumModule`` and then check the value of :attr:`QuantumModule.no_log`.

.. note::
    ``no_log`` specified in a module's argument_spec is handled by a different mechanism.

_quantum_debug
^^^^^^^^^^^^^^^

Boolean. Turns more verbose logging on or off and turns on logging of
external commands that the module executes. If a module uses
:py:meth:`QuantumModule.debug` rather than :py:meth:`QuantumModule.log` then
the messages are only logged if ``_quantum_debug`` is set to ``True``.
To set, add ``debug: True`` to :file:`quantum.cfg` or set the environment
variable :envvar:`ANSIBLE_DEBUG`. To access in a module, instantiate an
``QuantumModule`` and access :attr:`QuantumModule._debug`.

_quantum_diff
^^^^^^^^^^^^^^^

Boolean. If a module supports it, tells the module to show a unified diff of
changes to be made to templated files. To set, pass the ``--diff`` command line
option. To access in a module, instantiate an `QuantumModule` and access
:attr:`QuantumModule._diff`.

_quantum_verbosity
^^^^^^^^^^^^^^^^^^

Unused. This value could be used for finer grained control over logging.

_quantum_selinux_special_fs
^^^^^^^^^^^^^^^^^^^^^^^^^^^

List. Names of filesystems which should have a special SELinux
context. They are used by the `QuantumModule` methods which operate on
files (changing attributes, moving, and copying). To set, add a comma separated string of filesystem names in :file:`quantum.cfg`::

  # quantum.cfg
  [selinux]
  special_context_filesystems=nfs,vboxsf,fuse,ramfs,vfat

Most modules can use the built-in ``QuantumModule`` methods to manipulate
files. To access in a module that needs to know about these special context filesystems, instantiate an ``QuantumModule`` and examine the list in
:attr:`QuantumModule._selinux_special_fs`.

This replaces :attr:`quantum.module_utils.basic.SELINUX_SPECIAL_FS` from
:ref:`module_replacer`. In module replacer it was a comma separated string of
filesystem names. Under Ansiballz it's an actual list.

.. versionadded:: 2.1

_quantum_syslog_facility
^^^^^^^^^^^^^^^^^^^^^^^^

This parameter controls which syslog facility Quantum module logs to. To set, change the ``syslog_facility`` value in :file:`quantum.cfg`. Most
modules should just use :meth:`QuantumModule.log` which will then make use of
this. If a module has to use this on its own, it should instantiate an
`QuantumModule` and then retrieve the name of the syslog facility from
:attr:`QuantumModule._syslog_facility`. The Ansiballz code is less hacky than the old :ref:`module_replacer` code:

.. code-block:: python

        # Old module_replacer way
        import syslog
        syslog.openlog(NAME, 0, syslog.LOG_USER)

        # New Ansiballz way
        import syslog
        facility_name = module._syslog_facility
        facility = getattr(syslog, facility_name, syslog.LOG_USER)
        syslog.openlog(NAME, 0, facility)

.. versionadded:: 2.1

_quantum_version
^^^^^^^^^^^^^^^^

This parameter passes the version of Quantum that runs the module. To access
it, a module should instantiate an `QuantumModule` and then retrieve it
from :attr:`QuantumModule.quantum_version`. This replaces
:attr:`quantum.module_utils.basic.ANSIBLE_VERSION` from
:ref:`module_replacer`.

.. versionadded:: 2.1


.. _flow_module_return_values:

Module return values & Unsafe strings
-------------------------------------

At the end of a module's execution, it formats the data that it wants to return as a JSON string and prints the string to its stdout. The normal action plugin receives the JSON string, parses it into a Python dictionary, and returns it to the executor.

If Quantum templated every string return value, it would be vulnerable to an attack from users with access to managed nodes. If an unscrupulous user disguised malicious code as Quantum return value strings, and if those strings were then templated on the controller, Quantum could execute arbitrary code. To prevent this scenario, Quantum marks all strings inside returned data as ``Unsafe``, emitting any Jinja2 templates in the strings verbatim, not expanded by Jinja2.

Strings returned by invoking a module through ``ActionPlugin._execute_module()`` are automatically marked as ``Unsafe`` by the normal action plugin. If another action plugin retrieves information from a module through some other means, it must mark its return data as ``Unsafe`` on its own.

In case a poorly-coded action plugin fails to mark its results as "Unsafe," Quantum audits the results again when they are returned to the executor,
marking all strings as ``Unsafe``. The normal action plugin protects itself and any other code that it calls with the result data as a parameter. The check inside the executor protects the output of all other action plugins, ensuring that subsequent tasks run by Quantum will not template anything from those results either.

.. _flow_special_considerations:

Special considerations
----------------------

.. _flow_pipelining:

Pipelining
^^^^^^^^^^

Quantum can transfer a module to a remote machine in one of two ways:

* it can write out the module to a temporary file on the remote host and then
  use a second connection to the remote host to execute it with the
  interpreter that the module needs
* or it can use what's known as pipelining to execute the module by piping it
  into the remote interpreter's stdin.

Pipelining only works with modules written in Python at this time because
Quantum only knows that Python supports this mode of operation. Supporting
pipelining means that whatever format the module payload takes before being
sent over the wire must be executable by Python via stdin.

.. _flow_args_over_stdin:

Why pass args over stdin?
^^^^^^^^^^^^^^^^^^^^^^^^^

Passing arguments via stdin was chosen for the following reasons:

* When combined with :ref:`ANSIBLE_PIPELINING`, this keeps the module's arguments from
  temporarily being saved onto disk on the remote machine. This makes it
  harder (but not impossible) for a malicious user on the remote machine to
  steal any sensitive information that may be present in the arguments.
* Command line arguments would be insecure as most systems allow unprivileged
  users to read the full commandline of a process.
* Environment variables are usually more secure than the commandline but some
  systems limit the total size of the environment. This could lead to
  truncation of the parameters if we hit that limit.


.. _flow_quantummodule:

QuantumModule
-------------

.. _argument_spec:

Argument spec
^^^^^^^^^^^^^

The ``argument_spec`` provided to ``QuantumModule`` defines the supported arguments for a module, as well as their type, defaults and more.

Example ``argument_spec``:

.. code-block:: python

    module = QuantumModule(argument_spec=dict(
        top_level=dict(
            type='dict',
            options=dict(
                second_level=dict(
                    default=True,
                    type='bool',
                )
            )
        )
    ))

This section will discuss the behavioral attributes for arguments:

type
""""

``type`` allows you to define the type of the value accepted for the argument. The default value for ``type`` is ``str``. Possible values are:

* str
* list
* dict
* bool
* int
* float
* path
* raw
* jsonarg
* json
* bytes
* bits

The ``raw`` type, performs no type validation or type casing, and maintains the type of the passed value.

elements
""""""""

``elements`` works in combination with ``type`` when ``type='list'``. ``elements`` can then be defined as ``elements='int'`` or any other type, indicating that each element of the specified list should be of that type.

default
"""""""

The ``default`` option allows sets a default value for the argument for the scenario when the argument is not provided to the module. When not specified, the default value is ``None``.

fallback
""""""""

``fallback`` accepts a ``tuple`` where the first argument is a callable (function) that will be used to perform the lookup, based on the second argument. The second argument is a list of values to be accepted by the callable.

The most common callable used is ``env_fallback`` which will allow an argument to optionally use an environment variable when the argument is not supplied.

Example::

    username=dict(fallback=(env_fallback, ['ANSIBLE_NET_USERNAME']))

choices
"""""""

``choices`` accepts a list of choices that the argument will accept. The types of ``choices`` should match the ``type``.

required
""""""""

``required`` accepts a boolean, either ``True`` or ``False`` that indicates that the argument is required. This should not be used in combination with ``default``.

no_log
""""""

``no_log`` accepts a boolean, either ``True`` or ``False``, that indicates explicitly whether or not the argument value should be masked in logs and output.

.. note::
   In the absence of ``no_log``, if the parameter name appears to indicate that the argument value is a password or passphrase (such as "admin_password"), a warning will be shown and the value will be masked in logs but **not** output. To disable the warning and masking for parameters that do not contain sensitive information, set ``no_log`` to ``False``.

aliases
"""""""

``aliases`` accepts a list of alternative argument names for the argument, such as the case where the argument is ``name`` but the module accepts ``aliases=['pkg']`` to allow ``pkg`` to be interchangeably with ``name``

options
"""""""

``options`` implements the ability to create a sub-argument_spec, where the sub options of the top level argument are also validated using the attributes discussed in this section. The example at the top of this section demonstrates use of ``options``. ``type`` or ``elements`` should be ``dict`` is this case.

apply_defaults
""""""""""""""

``apply_defaults`` works alongside ``options`` and allows the ``default`` of the sub-options to be applied even when the top-level argument is not supplied.

In the example of the ``argument_spec`` at the top of this section, it would allow ``module.params['top_level']['second_level']`` to be defined, even if the user does not provide ``top_level`` when calling the module.

removed_in_version
""""""""""""""""""

``removed_in_version`` indicates which version of Quantum a deprecated argument will be removed in.
