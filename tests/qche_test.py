# coding: utf-8
import json
import mock
import os
import shutil
import tempfile
import unittest

import qche


class QcheTestMixin(object):
    def test_it_evaluates_whether_a_key_is_in_set_when_it_is(self):
        self.cache.put("k")
        self.assertTrue("k" in self.cache)

    def test_it_evaluates_whether_a_key_is_in_set_when_it_is(self):
        self.assertFalse("k" in self.cache)

    def test_it_puts_values_in_cache(self):
        self.cache.put("k", "value")
        self.assertEqual(self.cache.get("k"), "value")

    def test_getting_value_via_getitem_works(self):
        self.cache.put("k", "value")
        self.assertEqual(self.cache["k"], "value")

    def test_putting_value_via_settitem_works(self):
        self.cache["k"] = "value"
        self.assertEqual(self.cache.get("k"), "value")

    def test_it_calls_persist_on_context_manager_exit(self):
        self.cache.persist = mock.Mock()
        with self.cache as c:
            c.put("k", "v")
        self.cache.persist.assert_called_once()


class FilesystemCacheTestMixin(QcheTestMixin):
    def test_it_initializes_empty_cache_correctly(self):
        self.assertDictEqual(self.cache._data, {})
        self.assertEqual(self.cache.size, 0)

    def test_it_loads_data_from_filesystem_upon_initialization(self):
        with open(self.filename, "w") as f:
            f.write(self.cache.serializer.dumps({'key': 'value'}))

        other_cache = self.cache.__class__(self.filename)
        self.assertEqual(other_cache.get("key"), "value")
        self.assertEqual(other_cache.size, 1)

    def test_it_loads_data_dumped_from_same_type_instance(self):
        self.cache.put("key", "value")
        self.cache.persist()

        cache2 = self.cache.__class__(self.filename)
        self.assertEqual(cache2.get("key"), "value")
        self.assertEqual(cache2.size, 1)

    def test_it_loads_data_with_non_ascii_keys(self):
        key = "kẽy"

        self.cache.put(key, "value")
        self.cache.persist()

        cache2 = self.cache.__class__(self.filename)
        self.assertEqual(cache2.get(key), "value")
        self.assertEqual(cache2.size, 1)

    def test_it_persists_data_when_explicitly_told_to(self):
        self.cache.put("key", "value")
        self.cache.persist()

        with open(self.filename, "r") as f:
            contents = f.read()

        self.assertDictEqual(self.cache.serializer.loads(contents), {"key": "value"})


class JsonCacheTest(unittest.TestCase, FilesystemCacheTestMixin):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.filename = os.path.join(self.tmpdir, "qche.tmp")
        self.cache = qche.JsonCache(self.filename)

    def tearDown(self):
        shutil.rmtree(self.tmpdir)


class PickleCacheTest(unittest.TestCase, FilesystemCacheTestMixin):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.filename = os.path.join(self.tmpdir, "qche.tmp")
        self.cache = qche.PickleCache(self.filename)

    def tearDown(self):
        shutil.rmtree(self.tmpdir)


class InMemoyCacheTest(unittest.TestCase, QcheTestMixin):
    def setUp(self):
        self.cache = qche.InMemoryCache()

    def test_it_initializes_empty_cache(self):
        self.assertDictEqual(self.cache._data, {})
        self.assertEqual(self.cache.size, 0)

    def test_it_doesnt_persist_data(self):
        self.cache.put("k", "v")

        cache2 = qche.InMemoryCache()
        self.assertEqual(cache2.get("k"), None)
        self.assertEqual(cache2.size, 0)
