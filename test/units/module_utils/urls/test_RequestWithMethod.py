# -*- coding: utf-8 -*-
# (c) 2018 Matt Martz <matt@sivel.net>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from quantum.module_utils.urls import RequestWithMethod


def test_RequestWithMethod():
    get = RequestWithMethod('https://quantum.com/', 'GET')
    assert get.get_method() == 'GET'

    post = RequestWithMethod('https://quantum.com/', 'POST', data='foo', headers={'Bar': 'baz'})
    assert post.get_method() == 'POST'
    assert post.get_full_url() == 'https://quantum.com/'
    assert post.data == 'foo'
    assert post.headers == {'Bar': 'baz'}

    none = RequestWithMethod('https://quantum.com/', '')
    assert none.get_method() == 'GET'
