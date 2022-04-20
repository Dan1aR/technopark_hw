""" Testting lru functional """
from unittest import TestCase
import unittest

from lru import LRUCache


class TestDataDesc(TestCase):
    ''' Testing LRUCache class '''
    def test_set(self):
        ''' Test set method and overflow '''
        cache = LRUCache(3)
        cache.set('k1', 1)
        cache.set('k2', 2)
        cache.set('k3', 3)

        self.assertTrue('k1' in cache.cache)
        self.assertTrue('k2' in cache.cache)
        self.assertTrue('k3' in cache.cache)

        cache.set('k4', 4)

        self.assertTrue('k1' not in cache.cache)
        self.assertTrue('k2' in cache.cache)
        self.assertTrue('k3' in cache.cache)
        self.assertTrue('k4' in cache.cache)

    def test_get(self):
        ''' Test get method and overflow '''
        cache = LRUCache(3)
        cache.set('k1', 1)
        cache.set('k2', 2)
        cache.set('k3', 3)

        self.assertEqual(cache.get('k1'), 1)
        self.assertEqual(cache.get('k2'), 2)
        self.assertEqual(cache.get('k3'), 3)

        cache.set('k4', 4)

        self.assertEqual(cache.get('k1'), None)
        self.assertEqual(cache.get('k2'), 2)
        self.assertEqual(cache.get('k3'), 3)
        self.assertEqual(cache.get('k4'), 4)

    def test_setitem(self):
        ''' Test setitem and overflow '''
        cache = LRUCache(3)
        cache['k1'] = 1
        cache['k2'] = 2
        cache['k3'] = 3

        self.assertTrue('k1' in cache.cache)
        self.assertTrue('k2' in cache.cache)
        self.assertTrue('k3' in cache.cache)

        cache['k4'] = 4

        self.assertTrue('k1' not in cache.cache)
        self.assertTrue('k2' in cache.cache)
        self.assertTrue('k3' in cache.cache)
        self.assertTrue('k4' in cache.cache)

    def test_getitem(self):
        ''' Test get method and overflow '''
        cache = LRUCache(3)
        cache['k1'] = 1
        cache['k2'] = 2
        cache['k3'] = 3

        self.assertEqual(cache['k0'], None)
        self.assertEqual(cache['k1'], 1)
        self.assertEqual(cache['k2'], 2)
        self.assertEqual(cache['k3'], 3)

        cache['k3'] = 5
        cache['k4'] = 4

        self.assertEqual(cache.get('k1'), None)
        self.assertEqual(cache.get('k2'), 2)
        self.assertEqual(cache.get('k3'), 5)
        self.assertEqual(cache.get('k4'), 4)

    def test_pop(self):
        ''' Test pop '''
        cache = LRUCache(3)
        cache['k1'] = 1
        cache['k2'] = 2
        cache['k3'] = 3

        self.assertEqual(cache['k1'], 1)
        self.assertEqual(cache['k2'], 2)
        self.assertEqual(cache['k3'], 3)

        cache.pop('k1')

        self.assertEqual(cache.get('k1'), None)
        self.assertEqual(cache.get('k2'), 2)
        self.assertEqual(cache.get('k3'), 3)

    def test_len(self):
        ''' Test len '''
        cache = LRUCache(3)
        cache['k1'] = 1
        cache['k2'] = 2
        cache['k3'] = 3
        self.assertEqual(len(cache), 3)

        cache.pop('k1')
        self.assertEqual(len(cache), 2)
        cache['k4'] = 4
        cache['k5'] = 5
        self.assertEqual(len(cache), 3)


    def test_limit1(self):
        ''' Test LRU with limit = 1'''
        cache = LRUCache(1)
        cache['k1'] = 1
        self.assertTrue('k1' in cache.cache)

        cache['k2'] = 2
        self.assertFalse('k1' in cache.cache)
        self.assertTrue('k2' in cache.cache)

        cache['k3'] = 3
        self.assertFalse('k2' in cache.cache)
        self.assertTrue('k3' in cache.cache)

        cache['k4'] = 4
        self.assertFalse('k3' in cache.cache)
        self.assertTrue('k4' in cache.cache)

    def test_complete_displacement(self):
        ''' Test LRU with full el-s displasment '''

        cache = LRUCache(3)
        cache['k1'] = 1
        cache['k2'] = 2
        cache['k3'] = 3

        self.assertTrue('k1' in cache.cache)
        self.assertTrue('k2' in cache.cache)
        self.assertTrue('k3' in cache.cache)

        cache['k4'] = 4
        cache['k5'] = 5
        cache['k6'] = 6

        self.assertFalse('k1' in cache.cache)
        self.assertFalse('k2' in cache.cache)
        self.assertFalse('k3' in cache.cache)
        self.assertTrue('k4' in cache.cache)
        self.assertTrue('k5' in cache.cache)
        self.assertTrue('k6' in cache.cache)

if __name__ == "__main__":
    unittest.main()
