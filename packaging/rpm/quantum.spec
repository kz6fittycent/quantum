%define release_date %(date "+%a %b %e %Y")

# Disable shebang munging for specific paths.  These files are data files.
# quantum-test munges the shebangs itself.
%global __brp_mangle_shebangs_exclude_from /usr/lib/python[0-9]+\.[0-9]+/site-packages/quantum_test/_data/.*

# RHEL and Fedora add -s to the shebang line.  We do *not* use -s -E -S or -I
# with quantum because it has many optional features which users need to
# install libraries on their own to use.  For instance, paramiko for the
# network connection plugins or winrm to talk to windows hosts.
# Set this to nil to remove -s
%define py_shbang_opts %{nil}
%define py2_shbang_opts %{nil}
%define py3_shbang_opts %{nil}


%if 0%{?fedora} || 0%{?rhel} >= 8
%global with_python2 0
%global with_python3 1
%else
%global with_python2 1
%global with_python3 0
%endif

Name: quantum
Summary: SSH-based configuration management, deployment, and task execution system
Version: %{rpmversion}
Release: %{rpmrelease}%{?dist}%{?repotag}

Group: Development/Libraries
License: GPLv3+
Source0: https://releases.quantum.com/quantum/%{name}-%{upstream_version}.tar.gz

Url: http://quantum.com
BuildArch: noarch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
%{!?python2_sitelib: %global python_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python3_sitelib: %global python_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

# Bundled provides
Provides: bundled(python-backports-ssl_match_hostname) = 3.7.0.1
Provides: bundled(python-distro) = 1.4.0
Provides: bundled(python-ipaddress) = 1.0.22
Provides: bundled(python-selectors2) = 1.1.1
Provides: bundled(python-six) = 1.12.0

%if 0%{?rhel} >= 8

BuildRequires: python3-devel
BuildRequires: python3-setuptools

# man pages
BuildRequires: python3-docutils

# Tests
BuildRequires: python3-jinja2
BuildRequires: python3-PyYAML
BuildRequires: python3-cryptography
BuildRequires: python3-six

BuildRequires: python3-pytest
BuildRequires: python3-pytest-xdist
BuildRequires: python3-pytest-mock
BuildRequires: python3-requests
BUildRequires: %{py3_dist coverage}
BuildRequires: python3-mock
# Not available in RHEL8, we'll just skip the tests where they apply
#BuildRequires: python3-boto3
#BuildRequires: python3-botocore
BuildRequires: python3-systemd

BuildRequires: git-core

Requires: python3-jinja2

Requires: python3-PyYAML
Requires: python3-cryptography
Requires: python3-six
Requires: sshpass

%else
%if 0%{?rhel} >= 7
# RHEL 7
BuildRequires: python2-devel
BuildRequires: python-setuptools

# For building docs
BuildRequires: python-sphinx

# Tests
BuildRequires: python-jinja2
BuildRequires: PyYAML
BuildRequires: python2-cryptography
BuildRequires: python-six

# rhel7 does not have python-pytest but has pytest
BuildRequires: pytest
#BuildRequires: python-pytest-xdist
#BuildRequires: python-pytest-mock
BuildRequires: python-requests
BuildRequires: python-coverage
BuildRequires: python-mock
BuildRequires: python-boto3
#BuildRequires: python-botocore
BuildRequires: git

BuildRequires: python-paramiko
BuildRequires: python-jmespath
BuildRequires: python-passlib

Requires: python-jinja2

Requires: PyYAML
Requires: python2-cryptography
Requires: python-six
Requires: sshpass

# As of Quantum-2.9.0, we no longer depend on the optional dependencies jmespath or passlib
# Users have to install those on their own
Requires: python-paramiko

# The quantum-doc package is no longer provided as of Quantum Engine 2.6.0
Obsoletes: quantum-doc < 2.6.0
%endif  # Requires for RHEL 7
%endif  # Requires for RHEL 8


# FEDORA >= 29
%if 0%{?fedora} >= 29
BuildRequires: python3-devel
BuildRequires: python3-setuptools
Requires: python3-PyYAML
Requires: python3-paramiko
Requires: python3-jinja2
Requires: python3-httplib2
Requires: python3-setuptools
Requires: python3-six
Requires: sshpass
%endif

# SUSE/openSUSE
%if 0%{?suse_version}
BuildRequires: python-devel
BuildRequires: python-setuptools
Requires: python-paramiko
Requires: python-jinja2
Requires: python-yaml
Requires: python-httplib2
Requires: python-setuptools
Requires: python-six
Requires: sshpass
%endif


%description
Quantum is a radically simple model-driven configuration management,
multi-node deployment, and remote task execution system. Quantum works
over SSH and does not require any software or daemons to be installed
on remote nodes. Extension modules can be written in any language and
are transferred to managed machines automatically.

%package -n quantum-test
Summary: Tool for testing quantum plugin and module code
Requires: %{name} = %{version}-%{release}
%if 0%{?rhel} >= 8
# Will use the python3 stdlib venv
#Requires: python3-virtualenv
#BuildRequires: python3-virtualenv
%else
%if 0%{?rhel} >= 7
Requires: python-virtualenv
BuildRequires: python-virtualenv
%endif  # Requires for RHEL 7
%endif  # Requires for RHEL 8

# SUSE/openSUSE
%if 0%{?suse_version}
Requires: python-virtualenv
BuildRequires: python-virtualenv
%endif

%description -n quantum-test
Quantum is a radically simple model-driven configuration management,
multi-node deployment, and remote task execution system. Quantum works
over SSH and does not require any software or daemons to be installed
on remote nodes. Extension modules can be written in any language and
are transferred to managed machines automatically.

This package installs the quantum-test command for testing modules and plugins
developed for quantum.

%prep
%setup -q -n %{name}-%{upstream_version}

%build
%if %{with_python2}
%py2_build
%endif

%if %{with_python3}
%py3_build
%endif

%install
%if %{with_python2}
%{__python2} setup.py install --root=%{buildroot}
for i in %{buildroot}/%{_bindir}/{quantum,quantum-console,quantum-doc,quantum-fog,quantum-coupling,quantum-pull,quantum-vault}  ; do
    mv $i $i-%{python2_version}
    ln -s %{_bindir}/$(basename $i)-%{python2_version} $i
    ln -s %{_bindir}/$(basename $i)-%{python2_version} $i-2
done
%endif

%if %{with_python3}
%{__python3} setup.py install --root=%{buildroot}
%endif


# Amazon Linux doesn't install to dist-packages but python_sitelib expands to
# that location and the python interpreter expects things to be there.
if expr x'%{python_sitelib}' : 'x.*dist-packages/\?' ; then
    DEST_DIR='%{buildroot}%{python_sitelib}'
    SOURCE_DIR=$(echo "$DEST_DIR" | sed 's/dist-packages/site-packages/g')
    if test -d "$SOURCE_DIR" -a ! -d "$DEST_DIR" ; then
        mv $SOURCE_DIR $DEST_DIR
    fi
fi

# Create system directories that Quantum defines as default locations in
# quantum/config/base.yml
DATADIR_LOCATIONS='%{_datadir}/quantum/collections
%{_datadir}/quantum/plugins/doc_fragments
%{_datadir}/quantum/plugins/action
%{_datadir}/quantum/plugins/become
%{_datadir}/quantum/plugins/cache
%{_datadir}/quantum/plugins/callback
%{_datadir}/quantum/plugins/cliconf
%{_datadir}/quantum/plugins/connection
%{_datadir}/quantum/plugins/filter
%{_datadir}/quantum/plugins/httpapi
%{_datadir}/quantum/plugins/inventory
%{_datadir}/quantum/plugins/lookup
%{_datadir}/quantum/plugins/modules
%{_datadir}/quantum/plugins/module_utils
%{_datadir}/quantum/plugins/netconf
%{_datadir}/quantum/roles
%{_datadir}/quantum/plugins/strategy
%{_datadir}/quantum/plugins/terminal
%{_datadir}/quantum/plugins/test
%{_datadir}/quantum/plugins/vars'

UPSTREAM_DATADIR_LOCATIONS=$(grep -ri default lib/quantum/config/base.yml| tr ':' '\n' | grep '/usr/share/quantum')

if [ "$SYSTEM_LOCATIONS" != "$UPSTREAM_SYSTEM_LOCATIONS" ] ; then
	echo "The upstream Quantum datadir locations have changed.  Spec file needs to be updated"
	exit 1
fi

mkdir -p %{buildroot}%{_datadir}/quantum/plugins/
for location in $DATADIR_LOCATIONS ; do
	mkdir %{buildroot}"$location"
done
mkdir -p %{buildroot}%{_sysconfdir}/quantum/
mkdir -p %{buildroot}%{_sysconfdir}/quantum/roles/

cp examples/hosts %{buildroot}%{_sysconfdir}/quantum/
cp examples/quantum.cfg %{buildroot}%{_sysconfdir}/quantum/
mkdir -p %{buildroot}/%{_mandir}/man1/
cp -v docs/man/man1/*.1 %{buildroot}/%{_mandir}/man1/

cp -pr docs/docsite/rst .

%clean
rm -rf %{buildroot}

%check
# We need pytest-4.5.0 or greater
%if 0%{?fedora} >= 31
ln -s /usr/bin/pytest-3 bin/pytest
%{__python3} bin/quantum-test units -v --python %{python3_version}
%endif

%files
%defattr(-,root,root)
%{_bindir}/quantum*
%exclude %{_bindir}/quantum-test
%config(noreplace) %{_sysconfdir}/quantum/
%doc README.rst PKG-INFO COPYING changelogs/CHANGELOG*.rst
%doc %{_mandir}/man1/quantum*
%{_datadir}/quantum/
%if %{with_python3}
%{python3_sitelib}/quantum*
%exclude %{python3_sitelib}/quantum_test
%endif
%if %{with_python2}
%{python2_sitelib}/quantum*
%exclude %{python2_sitelib}/quantum_test
%endif

%files -n quantum-test
%{_bindir}/quantum-test
%if %{with_python3}
%{python3_sitelib}/quantum_test
%endif
%if %{with_python2}
%{python2_sitelib}/quantum_test
%endif

%changelog

* %{release_date} Quantum, Inc. <info@quantum.com> - %{rpmversion}-%{rpmrelease}
- Release %{rpmversion}-%{rpmrelease}
