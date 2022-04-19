""" Testting custom_list functional """
from unittest import TestCase
import unittest

from custom_list import CustomList


class TestCustomList(TestCase):
    """ Testing CustomList and its functions """
    def assert_equal_foreach(self, first, second):
        """ Equal for each element """
        self.assertEqual(len(first), len(second))
        for left, right in zip(first, second):
            self.assertEqual(left, right)

    def test_str(self):
        """ Testing Custom str """
        my_list = CustomList([1, 2, 3, 4, 5])
        test_str = "[1, 2, 3, 4, 5] 15"
        self.assertEqual(test_str, str(my_list))

    def test_add(self):
        """ Testing Custom add """
        list1 = CustomList([1, 2, 3, 4, 5])
        list2 = CustomList([1, 2, 3])
        ans = list1 + list2
        self.assert_equal_foreach([2, 4, 6, 4, 5], ans)
        self.assert_equal_foreach([1, 2, 3, 4, 5], list1)
        self.assert_equal_foreach([1, 2, 3], list2)
        self.assertIsInstance(ans, CustomList)

        list1 = CustomList([5, 4, 3])
        list2 = CustomList([1, 2, 3, 4, 5])
        ans = list1 + list2
        self.assert_equal_foreach([6, 6, 6, 4, 5], ans)
        self.assert_equal_foreach([5, 4, 3], list1)
        self.assert_equal_foreach([1, 2, 3, 4, 5], list2)
        self.assertIsInstance(ans, CustomList)

        list1 = CustomList([5, 4, 3])
        list2 = CustomList([1, 2, 3])
        ans = list1 + list2
        self.assert_equal_foreach([6, 6, 6], ans)
        self.assert_equal_foreach([5, 4, 3], list1)
        self.assert_equal_foreach([1, 2, 3], list2)
        self.assertIsInstance(ans, CustomList)

    def test_add_with_list_left(self):
        """ Testing Custom add with list """
        list1 = [1, 2, 3, 4, 5]
        list2 = CustomList([1, 2, 3])
        ans = list1 + list2
        self.assert_equal_foreach([2, 4, 6, 4, 5], ans)
        self.assert_equal_foreach([1, 2, 3, 4, 5], list1)
        self.assert_equal_foreach([1, 2, 3], list2)
        self.assertIsInstance(ans, CustomList)

        list1 = [5, 4, 3]
        list2 = CustomList([1, 2, 3, 4, 5])
        ans = list1 + list2
        self.assert_equal_foreach([6, 6, 6, 4, 5], ans)
        self.assert_equal_foreach([5, 4, 3], list1)
        self.assert_equal_foreach([1, 2, 3, 4, 5], list2)
        self.assertIsInstance(ans, CustomList)

        list1 = [5, 4, 3]
        list2 = CustomList([1, 2, 3])
        ans = list1 + list2
        self.assert_equal_foreach([6, 6, 6], ans)
        self.assert_equal_foreach([5, 4, 3], list1)
        self.assert_equal_foreach([1, 2, 3], list2)
        self.assertIsInstance(ans, CustomList)

    def test_add_with_list_right(self):
        """ Testing Custom add with list """
        list1 = CustomList([1, 2, 3, 4, 5])
        list2 = [1, 2, 3]
        ans = list1 + list2
        self.assert_equal_foreach([2, 4, 6, 4, 5], ans)
        self.assert_equal_foreach([1, 2, 3, 4, 5], list1)
        self.assert_equal_foreach([1, 2, 3], list2)
        self.assertIsInstance(ans, CustomList)

        list1 = CustomList([5, 4, 3])
        list2 = [1, 2, 3, 4, 5]
        ans = list1 + list2
        self.assert_equal_foreach([6, 6, 6, 4, 5], ans)
        self.assert_equal_foreach([5, 4, 3], list1)
        self.assert_equal_foreach([1, 2, 3, 4, 5], list2)
        self.assertIsInstance(ans, CustomList)

        list1 = CustomList([5, 4, 3])
        list2 = [1, 2, 3]
        ans = list1 + list2
        self.assert_equal_foreach([6, 6, 6], ans)
        self.assert_equal_foreach([5, 4, 3], list1)
        self.assert_equal_foreach([1, 2, 3], list2)
        self.assertIsInstance(ans, CustomList)

    def test_sub(self):
        """ Testing Custom sub """
        list1 = CustomList([1, 2, 3, 4, 5])
        list2 = CustomList([1, 2, 3])
        ans = list1 - list2
        self.assert_equal_foreach([0, 0, 0, 4, 5], ans)
        self.assert_equal_foreach([1, 2, 3, 4, 5], list1)
        self.assert_equal_foreach([1, 2, 3], list2)
        self.assertIsInstance(ans, CustomList)

        list1 = CustomList([5, 4, 3])
        list2 = CustomList([1, 2, 3, 4, 5])
        ans = list1 - list2
        self.assert_equal_foreach([4, 2, 0, -4, -5], ans)
        self.assert_equal_foreach([5, 4, 3], list1)
        self.assert_equal_foreach([1, 2, 3, 4, 5], list2)
        self.assertIsInstance(ans, CustomList)

        list1 = CustomList([5, 4, 3])
        list2 = CustomList([1, 2, 3])
        ans = list1 - list2
        self.assert_equal_foreach([4, 2, 0], ans)
        self.assert_equal_foreach([5, 4, 3], list1)
        self.assert_equal_foreach([1, 2, 3], list2)
        self.assertIsInstance(ans, CustomList)

    def test_sub_with_list_left(self):
        """ Testing Custom sub with list"""
        list1 = [1, 2, 3, 4, 5]
        list2 = CustomList([1, 2, 3])
        ans = list1 - list2
        self.assert_equal_foreach([0, 0, 0, 4, 5], ans)
        self.assert_equal_foreach([1, 2, 3, 4, 5], list1)
        self.assert_equal_foreach([1, 2, 3], list2)
        self.assertIsInstance(ans, CustomList)

        list1 = [5, 4, 3]
        list2 = CustomList([1, 2, 3, 4, 5])
        ans = list1 - list2
        self.assert_equal_foreach([4, 2, 0, -4, -5], ans)
        self.assert_equal_foreach([5, 4, 3], list1)
        self.assert_equal_foreach([1, 2, 3, 4, 5], list2)
        self.assertIsInstance(ans, CustomList)

        list1 = [5, 4, 3]
        list2 = CustomList([1, 2, 3])
        ans = list1 - list2
        self.assert_equal_foreach([4, 2, 0], ans)
        self.assert_equal_foreach([5, 4, 3], list1)
        self.assert_equal_foreach([1, 2, 3], list2)
        self.assertIsInstance(ans, CustomList)

    def test_sub_with_list_right(self):
        """ Testing Custom sub with list """
        list1 = CustomList([1, 2, 3, 4, 5])
        list2 = [1, 2, 3]
        ans = list1 - list2
        self.assert_equal_foreach([0, 0, 0, 4, 5], ans)
        self.assert_equal_foreach([1, 2, 3, 4, 5], list1)
        self.assert_equal_foreach([1, 2, 3], list2)
        self.assertIsInstance(ans, CustomList)

        list1 = CustomList([5, 4, 3])
        list2 = [1, 2, 3, 4, 5]
        ans = list1 - list2
        self.assert_equal_foreach([4, 2, 0, -4, -5], ans)
        self.assert_equal_foreach([5, 4, 3], list1)
        self.assert_equal_foreach([1, 2, 3, 4, 5], list2)
        self.assertIsInstance(ans, CustomList)

        list1 = CustomList([5, 4, 3])
        list2 = [1, 2, 3]
        ans = list1 - list2
        self.assert_equal_foreach([4, 2, 0], ans)
        self.assert_equal_foreach([5, 4, 3], list1)
        self.assert_equal_foreach([1, 2, 3], list2)
        self.assertIsInstance(ans, CustomList)

    def test_eq(self):
        """ Testing Custom eq """
        list1 = CustomList([1, 2, 3])
        list2 = CustomList([1, 2, 3])
        self.assertTrue(list1 == list2)
        list1 = CustomList([1, 2, 3, 4])
        list2 = CustomList([1, 2, 3])
        self.assertFalse(list1 == list2)

    def test_ne(self):
        """ Testing Custom ne """
        list1 = CustomList([1, 2, 3])
        list2 = CustomList([1, 2, 3])
        self.assertFalse(list1 != list2)
        list1 = CustomList([1, 2, 3, 4])
        list2 = CustomList([1, 2, 3])
        self.assertTrue(list1 != list2)

    def test_lt(self):
        """ Testing Custom lt """
        list1 = CustomList([1, 2, 3, 4])
        list2 = CustomList([1, 2, 3])
        self.assertFalse(list1 < list2)
        list1 = CustomList([1, 2, 3])
        list2 = CustomList([1, 2, 3, 4])
        self.assertTrue(list1 < list2)

    def test_le(self):
        """ Testing Custom le """
        list1 = CustomList([1, 2, 3, 4])
        list2 = CustomList([1, 2, 3])
        self.assertFalse(list1 <= list2)
        list1 = CustomList([1, 2, 3])
        list2 = CustomList([1, 2, 3, 4])
        self.assertTrue(list1 <= list2)
        list1 = CustomList([1, 2, 3])
        list2 = CustomList([1, 2, 3])
        self.assertTrue(list1 <= list2)

    def test_gt(self):
        """ Testing Custom gt """
        list1 = CustomList([1, 2, 3, 4])
        list2 = CustomList([1, 2, 3])
        self.assertTrue(list1 > list2)
        list1 = CustomList([1, 2, 3])
        list2 = CustomList([1, 2, 3, 4])
        self.assertFalse(list1 > list2)

    def test_ge(self):
        """ Testing Custom ge """
        list1 = CustomList([1, 2, 3, 4])
        list2 = CustomList([1, 2, 3])
        self.assertTrue(list1 >= list2)
        list1 = CustomList([1, 2, 3])
        list2 = CustomList([1, 2, 3, 4])
        self.assertFalse(list1 >= list2)
        list1 = CustomList([1, 2, 3])
        list2 = CustomList([1, 2, 3])
        self.assertTrue(list1 >= list2)


if __name__ == "__main__":
    unittest.main()
