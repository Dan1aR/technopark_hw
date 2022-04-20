""" Testting desc functional """
from unittest import TestCase
import unittest

from desc import Data, IntegerExeption, StringExeption, PositiveExeption


class TestDataDesc(TestCase):
    """ Testing CustomClass and its attrs """
    def test_init(self):
        """ Testing init withouth exception """
        inst = Data(2, 'Wo', 5)
        self.assertEqual(inst.num, 2)
        self.assertEqual(inst.name, 'Wo')
        self.assertEqual(inst.price, 5)

    def test_desc_change_vals(self):
        """ Testing descs changing values """
        inst = Data(2, 'Wo', 5)
        inst.num = 3
        self.assertEqual(3, inst.num)

        inst.name = 'Lee'
        self.assertEqual('Lee', inst.name)

        inst.price = 300
        self.assertEqual(300, inst.price)

    def test_init_exceptions(self):
        """ Testing init with exception """
        with self.assertRaises(IntegerExeption):
            inst = Data(2.5, 'Wo', 5)
            self.assertEqual(2.5, inst.num)

        with self.assertRaises(StringExeption):
            inst = Data(2, 4, 5)
            self.assertEqual(4, inst.name)

        with self.assertRaises(PositiveExeption):
            inst = Data(2, 'Wo', -5)
            self.assertEqual(-5, inst.price)

    def test_assign_exceptions(self):
        """ Testing exceptions with assignment"""
        with self.assertRaises(IntegerExeption):
            inst = Data(2, 'Wo', 5)
            inst.num = 2.5
            self.assertEqual(2.5, inst.num)

        with self.assertRaises(StringExeption):
            inst = Data(2, 'Wo', 5)
            inst.name = 4
            self.assertEqual(4, inst.name)

        with self.assertRaises(PositiveExeption):
            inst = Data(2, 'Wo', 5)
            inst.price = -5
            self.assertEqual(-5, inst.price)

    def test_fromat_answer(self):
        """ Testing format answer func """
        inst = Data(2, 'Wo', 5)
        ans = inst.format_answer()
        true_ans = '2, Wo, 5'
        self.assertEqual(ans, true_ans)

    def test_whole_price(self):
        """ Testing whole price func """
        inst = Data(2, 'Wo', 5)
        self.assertEqual(inst.num * inst.price, inst.whole_price())


if __name__ == "__main__":
    unittest.main()
