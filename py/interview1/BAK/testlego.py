#!/usr/bin/env python

import unittest
import lego
import pprint

pp = pprint.PrettyPrinter()

class TestLego(unittest.TestCase):
    def test_brick_combo(self):
        self.assertEqual(1, lego.brick_combo(1))
        self.assertEqual(2, lego.brick_combo(2))
        self.assertEqual(4, lego.brick_combo(3))
        self.assertEqual(8, lego.brick_combo(4))
        self.assertEqual(15, lego.brick_combo(5))

    @unittest.skip('meh')
    def test_partition(self):
        expect1 = set(['1'])
        self.assertEqual(expect1, lego.partition(1))

        expect3 = set(['2,1', '3', '1,2', '1,1,1'])
        self.assertEqual(expect3, lego.partition(3))

        expect4 = set(['2,1,1', '1,3', '1,1,2', '1,1,1,1', '4', '1,2,1', '3,1', '2,2'])
        self.assertEqual(expect4, lego.partition(4))

        pp.pprint(lego.organize_partitions(lego.partition(5)))
        pp.pprint(lego.organize_partitions(lego.partition(1)))
        pp.pprint(lego.organize_partitions(lego.partition(10)))

    def test_count(self):
        # height, width
        self.assertEqual(3, lego.count(2, 2))
        self.assertEqual(7, lego.count(3, 2))
        self.assertEqual(9, lego.count(2, 3))
        self.assertEqual(3375, lego.count(4, 4))

    def test_unknown(self):
        lego.count(9, 5)

if __name__ == '__main__':
    unittest.main()

