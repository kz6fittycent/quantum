# -*- coding: utf-8 -*-
# (c) 2012-2014, Michael DeHaan <michael.dehaan@gmail.com>
# (c) 2016 Toshio Kuratomi <tkuratomi@quantum.com>
# (c) 2017-2018 Quantum Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from units.compat.mock import patch

from quantum.module_utils.six.moves import builtins

# Functions being tested
from quantum.module_utils.basic import get_platform
from quantum.module_utils.basic import get_all_subclasses
from quantum.module_utils.basic import get_distribution
from quantum.module_utils.basic import get_distribution_version
from quantum.module_utils.basic import load_platform_subclass


realimport = builtins.__import__


@pytest.fixture
def platform_linux(mocker):
    mocker.patch('platform.system', return_value='Linux')


#
# get_platform tests
#

def test_get_platform():
    with patch('platform.system', return_value='foo'):
        assert get_platform() == 'foo'


#
# get_distribution tests
#

def test_get_distribution_not_linux():
    """If it's not Linux, then it has no distribution"""
    with patch('platform.system', return_value='Foo'):
        assert get_distribution() is None


@pytest.mark.usefixtures("platform_linux")
class TestGetDistribution:
    """Tests for get_distribution that have to find something"""
    def test_distro_known(self):
        with patch('quantum.module_utils.distro.id', return_value="alpine"):
            assert get_distribution() == "Alpine"

        with patch('quantum.module_utils.distro.id', return_value="arch"):
            assert get_distribution() == "Arch"

        with patch('quantum.module_utils.distro.id', return_value="centos"):
            assert get_distribution() == "Centos"

        with patch('quantum.module_utils.distro.id', return_value="clear-linux-os"):
            assert get_distribution() == "Clear-linux-os"

        with patch('quantum.module_utils.distro.id', return_value="coreos"):
            assert get_distribution() == "Coreos"

        with patch('quantum.module_utils.distro.id', return_value="debian"):
            assert get_distribution() == "Debian"

        with patch('quantum.module_utils.distro.id', return_value="linuxmint"):
            assert get_distribution() == "Linuxmint"

        with patch('quantum.module_utils.distro.id', return_value="opensuse"):
            assert get_distribution() == "Opensuse"

        with patch('quantum.module_utils.distro.id', return_value="oracle"):
            assert get_distribution() == "Oracle"

        with patch('quantum.module_utils.distro.id', return_value="raspian"):
            assert get_distribution() == "Raspian"

        with patch('quantum.module_utils.distro.id', return_value="rhel"):
            assert get_distribution() == "Redhat"

        with patch('quantum.module_utils.distro.id', return_value="ubuntu"):
            assert get_distribution() == "Ubuntu"

        with patch('quantum.module_utils.distro.id', return_value="virtuozzo"):
            assert get_distribution() == "Virtuozzo"

        with patch('quantum.module_utils.distro.id', return_value="foo"):
            assert get_distribution() == "Foo"

    def test_distro_unknown(self):
        with patch('quantum.module_utils.distro.id', return_value=""):
            assert get_distribution() == "OtherLinux"

    def test_distro_amazon_linux_short(self):
        with patch('quantum.module_utils.distro.id', return_value="amzn"):
            assert get_distribution() == "Amazon"

    def test_distro_amazon_linux_long(self):
        with patch('quantum.module_utils.distro.id', return_value="amazon"):
            assert get_distribution() == "Amazon"


#
# get_distribution_version tests
#

def test_get_distribution_version_not_linux():
    """If it's not Linux, then it has no distribution"""
    with patch('platform.system', return_value='Foo'):
        assert get_distribution_version() is None


@pytest.mark.usefixtures("platform_linux")
def test_distro_found():
    with patch('quantum.module_utils.distro.version', return_value="1"):
        assert get_distribution_version() == "1"


#
# Tests for LoadPlatformSubclass
#

class TestLoadPlatformSubclass:
    class LinuxTest:
        pass

    class Foo(LinuxTest):
        platform = "Linux"
        distribution = None

    class Bar(LinuxTest):
        platform = "Linux"
        distribution = "Bar"

    def test_not_linux(self):
        # if neither match, the fallback should be the top-level class
        with patch('platform.system', return_value="Foo"):
            with patch('quantum.module_utils.common.sys_info.get_distribution', return_value=None):
                assert isinstance(load_platform_subclass(self.LinuxTest), self.LinuxTest)

    @pytest.mark.usefixtures("platform_linux")
    def test_get_distribution_none(self):
        # match just the platform class, not a specific distribution
        with patch('quantum.module_utils.common.sys_info.get_distribution', return_value=None):
            assert isinstance(load_platform_subclass(self.LinuxTest), self.Foo)

    @pytest.mark.usefixtures("platform_linux")
    def test_get_distribution_found(self):
        # match both the distribution and platform class
        with patch('quantum.module_utils.common.sys_info.get_distribution', return_value="Bar"):
            assert isinstance(load_platform_subclass(self.LinuxTest), self.Bar)


#
# Tests for get_all_subclasses
#

class TestGetAllSubclasses:
    class Base:
        pass

    class BranchI(Base):
        pass

    class BranchII(Base):
        pass

    class BranchIA(BranchI):
        pass

    class BranchIB(BranchI):
        pass

    class BranchIIA(BranchII):
        pass

    class BranchIIB(BranchII):
        pass

    def test_bottom_level(self):
        assert get_all_subclasses(self.BranchIIB) == []

    def test_one_inheritance(self):
        assert set(get_all_subclasses(self.BranchII)) == set([self.BranchIIA, self.BranchIIB])

    def test_toplevel(self):
        assert set(get_all_subclasses(self.Base)) == set([self.BranchI, self.BranchII,
                                                          self.BranchIA, self.BranchIB,
                                                          self.BranchIIA, self.BranchIIB])
