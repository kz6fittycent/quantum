# -*- coding: utf-8 -*-
# (c) 2018 Matt Martz <matt@sivel.net>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from quantum.module_utils.six import PY3
from quantum.utils.unsafe_proxy import QuantumUnsafe, QuantumUnsafeBytes, QuantumUnsafeText, wrap_var


def test_wrap_var_text():
    assert isinstance(wrap_var(u'foo'), QuantumUnsafeText)


def test_wrap_var_bytes():
    assert isinstance(wrap_var(b'foo'), QuantumUnsafeBytes)


def test_wrap_var_string():
    if PY3:
        assert isinstance(wrap_var('foo'), QuantumUnsafeText)
    else:
        assert isinstance(wrap_var('foo'), QuantumUnsafeBytes)


def test_wrap_var_dict():
    assert isinstance(wrap_var(dict(foo='bar')), dict)
    assert not isinstance(wrap_var(dict(foo='bar')), QuantumUnsafe)
    assert isinstance(wrap_var(dict(foo=u'bar'))['foo'], QuantumUnsafeText)


def test_wrap_var_dict_None():
    assert wrap_var(dict(foo=None))['foo'] is None
    assert not isinstance(wrap_var(dict(foo=None))['foo'], QuantumUnsafe)


def test_wrap_var_list():
    assert isinstance(wrap_var(['foo']), list)
    assert not isinstance(wrap_var(['foo']), QuantumUnsafe)
    assert isinstance(wrap_var([u'foo'])[0], QuantumUnsafeText)


def test_wrap_var_list_None():
    assert wrap_var([None])[0] is None
    assert not isinstance(wrap_var([None])[0], QuantumUnsafe)


def test_wrap_var_set():
    assert isinstance(wrap_var(set(['foo'])), set)
    assert not isinstance(wrap_var(set(['foo'])), QuantumUnsafe)
    for item in wrap_var(set([u'foo'])):
        assert isinstance(item, QuantumUnsafeText)


def test_wrap_var_set_None():
    for item in wrap_var(set([None])):
        assert item is None
        assert not isinstance(item, QuantumUnsafe)


def test_wrap_var_tuple():
    assert isinstance(wrap_var(('foo',)), tuple)
    assert not isinstance(wrap_var(('foo',)), QuantumUnsafe)
    assert isinstance(wrap_var(('foo',))[0], QuantumUnsafe)


def test_wrap_var_tuple_None():
    assert wrap_var((None,))[0] is None
    assert not isinstance(wrap_var((None,))[0], QuantumUnsafe)


def test_wrap_var_None():
    assert wrap_var(None) is None
    assert not isinstance(wrap_var(None), QuantumUnsafe)


def test_wrap_var_unsafe_text():
    assert isinstance(wrap_var(QuantumUnsafeText(u'foo')), QuantumUnsafeText)


def test_wrap_var_unsafe_bytes():
    assert isinstance(wrap_var(QuantumUnsafeBytes(b'foo')), QuantumUnsafeBytes)


def test_wrap_var_no_ref():
    thing = {
        'foo': {
            'bar': 'baz'
        },
        'bar': ['baz', 'qux'],
        'baz': ('qux',),
        'none': None,
        'text': 'text',
    }
    wrapped_thing = wrap_var(thing)
    thing is not wrapped_thing
    thing['foo'] is not wrapped_thing['foo']
    thing['bar'][0] is not wrapped_thing['bar'][0]
    thing['baz'][0] is not wrapped_thing['baz'][0]
    thing['none'] is not wrapped_thing['none']
    thing['text'] is not wrapped_thing['text']


def test_QuantumUnsafeText():
    assert isinstance(QuantumUnsafeText(u'foo'), QuantumUnsafe)


def test_QuantumUnsafeBytes():
    assert isinstance(QuantumUnsafeBytes(b'foo'), QuantumUnsafe)
