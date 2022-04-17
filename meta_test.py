""" Testting meta class attributes """
from unittest import TestCase
import unittest

from meta import CustomClass


class TestCustomClass(TestCase):
    """ Testing CustomClass and its attrs """
    def test_class_init(self):
        """ Testing Custom init attrs """
        inst = CustomClass()
        self.assertTrue('custom_x' in dir(inst))
        self.assertFalse('x' in dir(inst))
        self.assertTrue('custom_val' in dir(inst))
        self.assertFalse('val' in dir(inst))
        self.assertTrue('custom_line' in dir(inst))
        self.assertFalse('line' in dir(inst))

    def test_class_init_values(self):
        """ Testing Custom init attrs values """
        inst = CustomClass()
        self.assertEqual(inst.custom_x, 50)
        self.assertEqual(inst.custom_val, 99)
        self.assertEqual(inst.custom_line(), 100)

    def test_additional_attrs(self):
        """ Testing Custom new attrs """
        inst = CustomClass()
        inst.new_attr = 10
        self.assertTrue('custom_new_attr' in dir(inst))
        self.assertFalse('new_attr' in dir(inst))
        self.assertEqual(inst.custom_new_attr, 10)


if __name__ == "__main__":
    unittest.main()
