#!/usr/bin/env python

import unittest


def path_to_fraction(path):
    """

    :param path:  list of integers
    :return: [numerator, denominator]
    """

    numerator = path[-1]
    denominator = 1
    for n in reversed(path[:-1]):
        numerator, denominator = denominator, numerator
        numerator = denominator * n + numerator

    return numerator, denominator


def fraction_to_path(numerator, denominator):

    result = []

    while denominator != 1:
        p = numerator // denominator
        result.append(p)
        numerator = numerator - p * denominator
        numerator, denominator = denominator, numerator

    result.append(numerator)
    return result


class MyTest(unittest.TestCase):
    def test_p2f_1(self):
        path = [1, 2, 3, 4]

        (n, d) = path_to_fraction(path)
        self.assertEqual(43, n)
        self.assertEqual(30, d)

    def test_p2f_2(self):
        path = [2]
        (n, d) = path_to_fraction(path)
        self.assertEqual(2, n)
        self.assertEqual(1, d)

    def test_f2p_1(self):
        n = 43
        d = 30

        path = fraction_to_path(n, d)
        self.assertEqual([1, 2, 3, 4], path)

    def test_f2p_2(self):
        n = 2
        d = 1

        path = fraction_to_path(n, d)
        self.assertEqual([2], path)
