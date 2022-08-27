#!/usr/bin/env python

# given 1 <= a <= b <= 2 ** 1024
#
# find the number of numbers in [a, b] that have a prime number of bits set.


import unittest
import random


def count_bits_set(n):
    """
    return the number of bits set in the binary representation of n.
    """
    if n == 0:
        return 0

    counter = 1
    while n & (n - 1):
        n &= n - 1
        counter += 1

    return counter


class MyTest(unittest.TestCase):
    def count_bits_set_1(self):
        self.assertEqual(0, count_bits_set(0))
        self.assertEqual(1, count_bits_set(1))
        self.assertEqual(1, count_bits_set(2 ** 1))
        self.assertEqual(1, count_bits_set(2 ** 5))
        self.assertEqual(1, count_bits_set(2 ** 32))
        self.assertEqual(1, count_bits_set(2 ** 1 - 1))
        self.assertEqual(2, count_bits_set(2 ** 2 - 1))
        self.assertEqual(3, count_bits_set(2 ** 3 - 1))
        self.assertEqual(4, count_bits_set(2 ** 4 - 1))
        self.assertEqual(5, count_bits_set(2 ** 5 - 1))
        self.assertEqual(6, count_bits_set(2 ** 6 - 1))

    def count_bits_set_2(self):
        n = random.randint(1, 2 ** 64)
        binstr = bin(n)[2:]
        print(n, binstr)
        binstr = list(binstr)
        bits = list(map(int, binstr))
        n_set_control = sum(bits)

        n_set_test = count_bits_set(n)
        self.assertEqual(n_set_control, n_set_test)
