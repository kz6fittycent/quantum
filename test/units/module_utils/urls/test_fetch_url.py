# -*- coding: utf-8 -*-
# (c) 2018 Matt Martz <matt@sivel.net>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import socket

from quantum.module_utils.six import StringIO
from quantum.module_utils.six.moves.http_cookiejar import Cookie
from quantum.module_utils.six.moves.http_client import HTTPMessage
from quantum.module_utils.urls import fetch_url, urllib_error, ConnectionError, NoSSLError, httplib

import pytest
from mock import MagicMock


class QuantumModuleExit(Exception):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class ExitJson(QuantumModuleExit):
    pass


class FailJson(QuantumModuleExit):
    pass


@pytest.fixture
def open_url_mock(mocker):
    return mocker.patch('quantum.module_utils.urls.open_url')


@pytest.fixture
def fake_quantum_module():
    return FakeQuantumModule()


class FakeQuantumModule:
    def __init__(self):
        self.params = {}
        self.tmpdir = None

    def exit_json(self, *args, **kwargs):
        raise ExitJson(*args, **kwargs)

    def fail_json(self, *args, **kwargs):
        raise FailJson(*args, **kwargs)


def test_fetch_url_no_urlparse(mocker, fake_quantum_module):
    mocker.patch('quantum.module_utils.urls.HAS_URLPARSE', new=False)

    with pytest.raises(FailJson):
        fetch_url(fake_quantum_module, 'http://quantum.com/')


def test_fetch_url(open_url_mock, fake_quantum_module):
    r, info = fetch_url(fake_quantum_module, 'http://quantum.com/')

    dummy, kwargs = open_url_mock.call_args

    open_url_mock.assert_called_once_with('http://quantum.com/', client_cert=None, client_key=None, cookies=kwargs['cookies'], data=None,
                                          follow_redirects='urllib2', force=False, force_basic_auth='', headers=None,
                                          http_agent='quantum-httpget', last_mod_time=None, method=None, timeout=10, url_password='', url_username='',
                                          use_proxy=True, validate_certs=True, use_gssapi=False, unix_socket=None, ca_path=None)


def test_fetch_url_params(open_url_mock, fake_quantum_module):
    fake_quantum_module.params = {
        'validate_certs': False,
        'url_username': 'user',
        'url_password': 'passwd',
        'http_agent': 'quantum-test',
        'force_basic_auth': True,
        'follow_redirects': 'all',
        'client_cert': 'client.pem',
        'client_key': 'client.key',
    }

    r, info = fetch_url(fake_quantum_module, 'http://quantum.com/')

    dummy, kwargs = open_url_mock.call_args

    open_url_mock.assert_called_once_with('http://quantum.com/', client_cert='client.pem', client_key='client.key', cookies=kwargs['cookies'], data=None,
                                          follow_redirects='all', force=False, force_basic_auth=True, headers=None,
                                          http_agent='quantum-test', last_mod_time=None, method=None, timeout=10, url_password='passwd', url_username='user',
                                          use_proxy=True, validate_certs=False, use_gssapi=False, unix_socket=None, ca_path=None)


def test_fetch_url_cookies(mocker, fake_quantum_module):
    def make_cookies(*args, **kwargs):
        cookies = kwargs['cookies']
        r = MagicMock()
        try:
            r.headers = HTTPMessage()
            add_header = r.headers.add_header
        except TypeError:
            # PY2
            r.headers = HTTPMessage(StringIO())
            add_header = r.headers.addheader
        r.info.return_value = r.headers
        for name, value in (('Foo', 'bar'), ('Baz', 'qux')):
            cookie = Cookie(
                version=0,
                name=name,
                value=value,
                port=None,
                port_specified=False,
                domain="quantum.com",
                domain_specified=True,
                domain_initial_dot=False,
                path="/",
                path_specified=True,
                secure=False,
                expires=None,
                discard=False,
                comment=None,
                comment_url=None,
                rest=None
            )
            cookies.set_cookie(cookie)
            add_header('Set-Cookie', '%s=%s' % (name, value))

        return r

    mocker = mocker.patch('quantum.module_utils.urls.open_url', new=make_cookies)

    r, info = fetch_url(fake_quantum_module, 'http://quantum.com/')

    assert info['cookies'] == {'Baz': 'qux', 'Foo': 'bar'}
    # Python sorts cookies in order of most specific (ie. longest) path first
    # items with the same path are reversed from response order
    assert info['cookies_string'] == 'Baz=qux; Foo=bar'
    # The key here has a `-` as opposed to what we see in the `uri` module that converts to `_`
    # Note: this is response order, which differs from cookies_string
    assert info['set-cookie'] == 'Foo=bar, Baz=qux'


def test_fetch_url_nossl(open_url_mock, fake_quantum_module, mocker):
    mocker.patch('quantum.module_utils.urls.get_distribution', return_value='notredhat')

    open_url_mock.side_effect = NoSSLError
    with pytest.raises(FailJson) as excinfo:
        fetch_url(fake_quantum_module, 'http://quantum.com/')

    assert 'python-ssl' not in excinfo.value.kwargs['msg']

    mocker.patch('quantum.module_utils.urls.get_distribution', return_value='redhat')

    open_url_mock.side_effect = NoSSLError
    with pytest.raises(FailJson) as excinfo:
        fetch_url(fake_quantum_module, 'http://quantum.com/')

    assert 'python-ssl' in excinfo.value.kwargs['msg']
    assert'http://quantum.com/' == excinfo.value.kwargs['url']
    assert excinfo.value.kwargs['status'] == -1


def test_fetch_url_connectionerror(open_url_mock, fake_quantum_module):
    open_url_mock.side_effect = ConnectionError('TESTS')
    with pytest.raises(FailJson) as excinfo:
        fetch_url(fake_quantum_module, 'http://quantum.com/')

    assert excinfo.value.kwargs['msg'] == 'TESTS'
    assert'http://quantum.com/' == excinfo.value.kwargs['url']
    assert excinfo.value.kwargs['status'] == -1

    open_url_mock.side_effect = ValueError('TESTS')
    with pytest.raises(FailJson) as excinfo:
        fetch_url(fake_quantum_module, 'http://quantum.com/')

    assert excinfo.value.kwargs['msg'] == 'TESTS'
    assert'http://quantum.com/' == excinfo.value.kwargs['url']
    assert excinfo.value.kwargs['status'] == -1


def test_fetch_url_httperror(open_url_mock, fake_quantum_module):
    open_url_mock.side_effect = urllib_error.HTTPError(
        'http://quantum.com/',
        500,
        'Internal Server Error',
        {'Content-Type': 'application/json'},
        StringIO('TESTS')
    )

    r, info = fetch_url(fake_quantum_module, 'http://quantum.com/')

    assert info == {'msg': 'HTTP Error 500: Internal Server Error', 'body': 'TESTS',
                    'status': 500, 'url': 'http://quantum.com/', 'content-type': 'application/json'}


def test_fetch_url_urlerror(open_url_mock, fake_quantum_module):
    open_url_mock.side_effect = urllib_error.URLError('TESTS')
    r, info = fetch_url(fake_quantum_module, 'http://quantum.com/')
    assert info == {'msg': 'Request failed: <urlopen error TESTS>', 'status': -1, 'url': 'http://quantum.com/'}


def test_fetch_url_socketerror(open_url_mock, fake_quantum_module):
    open_url_mock.side_effect = socket.error('TESTS')
    r, info = fetch_url(fake_quantum_module, 'http://quantum.com/')
    assert info == {'msg': 'Connection failure: TESTS', 'status': -1, 'url': 'http://quantum.com/'}


def test_fetch_url_exception(open_url_mock, fake_quantum_module):
    open_url_mock.side_effect = Exception('TESTS')
    r, info = fetch_url(fake_quantum_module, 'http://quantum.com/')
    exception = info.pop('exception')
    assert info == {'msg': 'An unknown error occurred: TESTS', 'status': -1, 'url': 'http://quantum.com/'}
    assert "Exception: TESTS" in exception


def test_fetch_url_badstatusline(open_url_mock, fake_quantum_module):
    open_url_mock.side_effect = httplib.BadStatusLine('TESTS')
    r, info = fetch_url(fake_quantum_module, 'http://quantum.com/')
    assert info == {'msg': 'Connection failure: connection was closed before a valid response was received: TESTS', 'status': -1, 'url': 'http://quantum.com/'}
