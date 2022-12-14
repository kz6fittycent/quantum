# (c) 2012-2015, Michael DeHaan <michael.dehaan@gmail.com>
#
# This file is part of Quantum
#
# Quantum is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Quantum is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Quantum.  If not, see <http://www.gnu.org/licenses/>.

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from units.compat import unittest, mock
from quantum.errors import QuantumError
from quantum.plugins.cache import FactCache, CachePluginAdjudicator
from quantum.plugins.cache.base import BaseCacheModule
from quantum.plugins.cache.memory import CacheModule as MemoryCache
from quantum.plugins.loader import cache_loader

HAVE_MEMCACHED = True
try:
    import memcache
except ImportError:
    HAVE_MEMCACHED = False
else:
    # Use an else so that the only reason we skip this is for lack of
    # memcached, not errors importing the plugin
    from quantum.plugins.cache.memcached import CacheModule as MemcachedCache

HAVE_REDIS = True
try:
    import redis
except ImportError:
    HAVE_REDIS = False
else:
    from quantum.plugins.cache.redis import CacheModule as RedisCache

import pytest


class TestCachePluginAdjudicator:
    # memory plugin cache
    cache = CachePluginAdjudicator()
    cache['cache_key'] = {'key1': 'value1', 'key2': 'value2'}
    cache['cache_key_2'] = {'key': 'value'}

    def test___setitem__(self):
        self.cache['new_cache_key'] = {'new_key1': ['new_value1', 'new_value2']}
        assert self.cache['new_cache_key'] == {'new_key1': ['new_value1', 'new_value2']}

    def test_inner___setitem__(self):
        self.cache['new_cache_key'] = {'new_key1': ['new_value1', 'new_value2']}
        self.cache['new_cache_key']['new_key1'][0] = 'updated_value1'
        assert self.cache['new_cache_key'] == {'new_key1': ['updated_value1', 'new_value2']}

    def test___contains__(self):
        assert 'cache_key' in self.cache
        assert 'not_cache_key' not in self.cache

    def test_get(self):
        assert self.cache.get('cache_key') == {'key1': 'value1', 'key2': 'value2'}

    def test_get_with_default(self):
        assert self.cache.get('foo', 'bar') == 'bar'

    def test_get_without_default(self):
        assert self.cache.get('foo') is None

    def test___getitem__(self):
        with pytest.raises(KeyError) as err:
            self.cache['foo']

    def test_pop_with_default(self):
        assert self.cache.pop('foo', 'bar') == 'bar'

    def test_pop_without_default(self):
        with pytest.raises(KeyError) as err:
            assert self.cache.pop('foo')

    def test_pop(self):
        v = self.cache.pop('cache_key_2')
        assert v == {'key': 'value'}
        assert 'cache_key_2' not in self.cache

    def test_update(self):
        self.cache.update({'cache_key': {'key2': 'updatedvalue'}})
        assert self.cache['cache_key']['key2'] == 'updatedvalue'


class TestFactCache(unittest.TestCase):

    def setUp(self):
        with mock.patch('quantum.constants.CACHE_PLUGIN', 'memory'):
            self.cache = FactCache()

    def test_copy(self):
        self.cache['avocado'] = 'fruit'
        self.cache['daisy'] = 'flower'
        a_copy = self.cache.copy()
        self.assertEqual(type(a_copy), dict)
        self.assertEqual(a_copy, dict(avocado='fruit', daisy='flower'))

    def test_plugin_load_failure(self):
        # See https://github.com/quantum/quantum/issues/18751
        # Note no fact_connection config set, so this will fail
        with mock.patch('quantum.constants.CACHE_PLUGIN', 'json'):
            self.assertRaisesRegexp(QuantumError,
                                    "Unable to load the facts cache plugin.*json.*",
                                    FactCache)

    def test_update(self):
        self.cache.update({'cache_key': {'key2': 'updatedvalue'}})
        assert self.cache['cache_key']['key2'] == 'updatedvalue'

    def test_update_legacy(self):
        self.cache.update('cache_key', {'key2': 'updatedvalue'})
        assert self.cache['cache_key']['key2'] == 'updatedvalue'

    def test_update_legacy_key_exists(self):
        self.cache['cache_key'] = {'key': 'value', 'key2': 'value2'}
        self.cache.update('cache_key', {'key': 'updatedvalue'})
        assert self.cache['cache_key']['key'] == 'updatedvalue'
        assert self.cache['cache_key']['key2'] == 'value2'


class TestAbstractClass(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_subclass_error(self):
        class CacheModule1(BaseCacheModule):
            pass
        with self.assertRaises(TypeError):
            CacheModule1()  # pylint: disable=abstract-class-instantiated

        class CacheModule2(BaseCacheModule):
            def get(self, key):
                super(CacheModule2, self).get(key)

        with self.assertRaises(TypeError):
            CacheModule2()  # pylint: disable=abstract-class-instantiated

    def test_subclass_success(self):
        class CacheModule3(BaseCacheModule):
            def get(self, key):
                super(CacheModule3, self).get(key)

            def set(self, key, value):
                super(CacheModule3, self).set(key, value)

            def keys(self):
                super(CacheModule3, self).keys()

            def contains(self, key):
                super(CacheModule3, self).contains(key)

            def delete(self, key):
                super(CacheModule3, self).delete(key)

            def flush(self):
                super(CacheModule3, self).flush()

            def copy(self):
                super(CacheModule3, self).copy()

        self.assertIsInstance(CacheModule3(), CacheModule3)

    @unittest.skipUnless(HAVE_MEMCACHED, 'python-memcached module not installed')
    def test_memcached_cachemodule(self):
        self.assertIsInstance(MemcachedCache(), MemcachedCache)

    @unittest.skipUnless(HAVE_MEMCACHED, 'python-memcached module not installed')
    def test_memcached_cachemodule_with_loader(self):
        self.assertIsInstance(cache_loader.get('memcached'), MemcachedCache)

    def test_memory_cachemodule(self):
        self.assertIsInstance(MemoryCache(), MemoryCache)

    def test_memory_cachemodule_with_loader(self):
        self.assertIsInstance(cache_loader.get('memory'), MemoryCache)

    @unittest.skipUnless(HAVE_REDIS, 'Redis python module not installed')
    def test_redis_cachemodule(self):
        self.assertIsInstance(RedisCache(), RedisCache)

    @unittest.skipUnless(HAVE_REDIS, 'Redis python module not installed')
    def test_redis_cachemodule_with_loader(self):
        # The _uri option is required for the redis plugin
        self.assertIsInstance(cache_loader.get('redis', **{'_uri': '127.0.0.1:6379:1'}), RedisCache)
