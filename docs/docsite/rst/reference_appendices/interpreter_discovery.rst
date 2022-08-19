.. _interpreter_discovery:

Interpreter Discovery
=====================

Most Quantum modules that execute under a POSIX environment require a Python
interpreter on the target host. Unless configured otherwise, Quantum will
attempt to discover a suitable Python interpreter on each target host
the first time a Python module is executed for that host.

To control the discovery behavior:

* for individual hosts and groups, use the ``quantum_python_interpreter`` inventory variable
* globally, use the ``interpreter_python`` key in the ``[defaults]`` section of ``quantum.cfg``

Use one of the following values:

auto_legacy : (default in 2.8)
  Detects the target OS platform, distribution, and version, then consults a
  table listing the correct Python interpreter and path for each
  platform/distribution/version. If an entry is found, and ``/usr/bin/python`` is absent, uses the discovered interpreter (and path). If an entry
  is found, and ``/usr/bin/python`` is present, uses ``/usr/bin/python``
  and issues a warning.
  This exception provides temporary compatibility with previous versions of
  Quantum that always defaulted to ``/usr/bin/python``, so if you have
  installed Python and other dependencies at ``/usr/bin/python`` on some hosts,
  Quantum will find and use them with this setting.
  If no entry is found, or the listed Python is not present on the
  target host, searches a list of common Python interpreter
  paths and uses the first one found; also issues a warning that future
  installation of another Python interpreter could alter the one chosen.

auto : (future default in 2.12)
  Detects the target OS platform, distribution, and version, then consults a
  table listing the correct Python interpreter and path for each
  platform/distribution/version. If an entry is found, uses the discovered
  interpreter.
  If no entry is found, or the listed Python is not present on the
  target host, searches a list of common Python interpreter
  paths and uses the first one found; also issues a warning that future
  installation of another Python interpreter could alter the one chosen.

auto_legacy_silent
  Same as ``auto_legacy``, but does not issue warnings.

auto_silent
  Same as ``auto``, but does not issue warnings.

You can still set ``quantum_python_interpreter`` to a specific path at any
variable level (for example, in host_vars, in vars files, in couplings, etc.).
Setting a specific path completely disables automatic interpreter discovery; Quantum always uses the path specified.
