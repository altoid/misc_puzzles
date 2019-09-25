#!/usr/bin/env python

import jack
import unittest
import pprint

pp = pprint.PrettyPrinter()

class TestJack(unittest.TestCase):

    def test1(self):
        self.assertEqual(3, jack.maxStep(2, 2))
        self.assertEqual(2, jack.maxStep(2, 1))
        self.assertEqual(5, jack.maxStep(3, 3))
        self.assertEqual(14, jack.maxStep(5, 10))
        self.assertEqual(14, jack.maxStep(5, 6))

    def test_badass(self):
        print jack.maxStep(500, 333)

    def test_unknown(self):
        print jack.maxStep(5, 10)

if __name__ == '__main__':
    unittest.main()
