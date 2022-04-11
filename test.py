""" Testting custom_list functional """
from unittest import TestCase
import unittest

from custom_list import CustomList


class TestCustomList(TestCase):
    """ Testing CustomList and its functions """

    def test_str(self):
        """ Testing Custom str """
        my_list = CustomList([1, 2, 3, 4, 5])
        test_str = "[1, 2, 3, 4, 5] 15"
        self.assertEqual(test_str, str(my_list))

    def test_add(self):
        """ Testing Custom add """
        list1 = CustomList([1, 2, 3, 4, 5])
        list2 = CustomList([1, 2, 3])

        self.assertEqual([2, 4, 6, 4, 5], list1 + list2)

        list1 = CustomList([5, 4, 3])
        list2 = CustomList([1, 2, 3, 4, 5])

        self.assertEqual([6, 6, 6, 4, 5], list1 + list2)

    def test_sub(self):
        """ Testing Custom sub """
        list1 = CustomList([1, 2, 3, 4, 5])
        list2 = CustomList([1, 2, 3])

        self.assertEqual([0, 0, 0, 4, 5], list1 - list2)

        list1 = CustomList([5, 4, 3])
        list2 = CustomList([1, 2, 3, 4, 5])

        self.assertEqual([4, 2, 0, 4, 5], list1 - list2)

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
