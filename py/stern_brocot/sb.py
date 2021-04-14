#!/usr/bin/env python

import unittest

# rules:
#
# representative rationals are always >= 1
# no path component contains a 0
#

def path_to_fraction(path):
    """
    the representation of a rational number by a path is not unique.

    [a0; a1 a2 a3 ... a(k-1), 1] = [a0; a1 a2 a3 ... a(k-1) + 1]

    these representations are unique if the last element in the path is > 1.
    so we hack the paths to put a 2 at the end of each.

    if len(path) = 1 then d = 1 and n = a0

    :param path:  list of integers
    :return: [numerator, denominator]
    """

    if len(path) == 1:
        return path[0], 1

    copy = list(path)
    copy.append(2)

    numerator = copy[-1]
    denominator = 1
    for n in reversed(copy[:-1]):
        numerator, denominator = denominator, numerator
        numerator = denominator * n + numerator

    return numerator, denominator


def fraction_to_path(numerator, denominator):

    result = []

    # do we need to reduce to lowest terms?

    if denominator == 1:
        result.append(numerator)
        return result

    while denominator != 1:
        p = numerator // denominator
        result.append(p)
        numerator = numerator - p * denominator
        numerator, denominator = denominator, numerator

    # result.append(numerator)
    return result


if __name__ == '__main__':
    path = [1, 2, 3, 5, 11, 31, 1, 46, 4562, 14, 1]
    n, d = path_to_fraction(path)
    print n, d
    print fraction_to_path(n, d)


class MyTest(unittest.TestCase):
    def test_p2f_1(self):
        path = [1, 2, 3, 4]

        (n, d) = path_to_fraction(path)
        print n, d
        self.assertEqual(96, n)
        self.assertEqual(67, d)

    def test_p2f_2(self):
        path = [2]
        (n, d) = path_to_fraction(path)
        self.assertEqual(2, n)
        self.assertEqual(1, d)

    def test_f2p_1(self):
        n = 96
        d = 67

        path = fraction_to_path(n, d)
        self.assertEqual([1, 2, 3, 4], path)

    def test_f2p_2(self):
        n = 2
        d = 1

        path = fraction_to_path(n, d)
        self.assertEqual([2], path)

    def test_p2f_3(self):
        path = [1]
        n, d = path_to_fraction(path)
        p2 = fraction_to_path(n, d)
        print n, d
        print p2
        self.assertEqual(p2, path)

    def test_p2f_4(self):
        path = [1, 1]
        n, d = path_to_fraction(path)
        p2 = fraction_to_path(n, d)
        print n, d
        print p2
        self.assertEqual(p2, path)

    def test_p2f_5(self):
        path = [1, 1, 1, 1, 1, 1, 1]
        n, d = path_to_fraction(path)
        p2 = fraction_to_path(n, d)
        print n, d
        print p2
        self.assertEqual(p2, path)
