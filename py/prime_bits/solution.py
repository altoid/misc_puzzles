#!/usr/bin/env python

# given 1 <= a <= b <= 2 ** 1024
#
# find the number of numbers in [a, b] that have a prime number of bits set.


import unittest
import random


binary_coeff_cache = {}

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


def binary_coefficient(n, k):
    assert n > 0
    assert 1 <= k <= n

    from_this = n
    choose_this = k
    if k > (n - k + 1):
        choose_this = n - k + 1

    if (from_this, choose_this) not in binary_coeff_cache:
        if from_this == 1 or choose_this == 1:
            result = 1
        else:
            result = binary_coefficient(n - 1, k - 1) + binary_coefficient(n - 1, k)

        binary_coeff_cache[(from_this, choose_this)] = result

    return binary_coeff_cache[(from_this, choose_this)]


class MyTest(unittest.TestCase):
    def test_binary_coeff_1(self):
        self.assertEqual(1, binary_coefficient(1, 1))
        self.assertEqual(1, binary_coefficient(2, 1))
        self.assertEqual(1, binary_coefficient(2, 2))
        self.assertEqual(1, binary_coefficient(1, 1))

        self.assertEqual(1, binary_coefficient(5, 1))
        self.assertEqual(4, binary_coefficient(5, 2))
        self.assertEqual(6, binary_coefficient(5, 3))
        self.assertEqual(4, binary_coefficient(5, 4))
        self.assertEqual(1, binary_coefficient(5, 5))

        # (n 3) is a triangle number
        for n in range(3, 100):
            self.assertEqual(((n - 2) * (n - 1)) // 2, binary_coefficient(n, 3))

    def test_count_bits_set_1(self):
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

    def test_count_bits_set_2(self):
        n = random.randint(1, 2 ** 64)
        binstr = bin(n)[2:]
        binstr = list(binstr)
        bits = list(map(int, binstr))
        n_set_control = sum(bits)

        n_set_test = count_bits_set(n)
        self.assertEqual(n_set_control, n_set_test)
