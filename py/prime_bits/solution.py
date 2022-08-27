#!/usr/bin/env python

# given 1 <= a <= b <= 2 ** 1024
#
# find the number of numbers in [a, b] that have a prime number of bits set.


import unittest
import random


binary_coeff_cache = {}


def get_bits(n):
    """
    return a list of 0s and 1s corresponding to the bits in n.  the element at position 0
    is the most significant bit.
    """
    binstr = bin(n)[2:]
    binstr = list(binstr)
    return list(map(int, binstr))


def decorate_zeroes(width, n):
    bits = get_bits(n)
    nbits = len(bits)

    # reverse the bits so that the list is easier to work with.
    bits = bits[::-1]

    decoration = [0] * nbits

    ones_seen = 0
    for i in range(len(bits)):
        if bits[i] == 1:
            ones_seen += 1
        else:
            decoration[i] = ones_seen

    if width > nbits:
        buffer = [sum(bits)] * (width - nbits)
        decoration += buffer

    return decoration


def n_bigger_with_k_bits(width, n):
    """
    given a number n with k bits set, find the number of numbers >= n,
    expressible with <width> bits, that have exactly k bits set.

    consider:

     11  10   9   8   7   6   5   4   3   2   1   0
    +---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   |   | 1 |   | 1 | 1 |   |   | 1 | 1 |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+

    to get the answer, we decorate each of the 0 bits with the number
    of 1s that are to its right:

     11  10   9   8   7   6   5   4   3   2   1   0
    +---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   |   | 1 |   | 1 | 1 |   |   | 1 | 1 |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+
      5   5   5       4           2   2           0

    first we pretend that the bit at 8 has been moved to 11.
    the number of numbers >= n with that bit set is equal to the
    number of ways we can place the remaining bits into the other
    slots:  (11 4) 

    next we pretend that the bit at 8 has been moved to 10.  (10 4)

    then to 9:  (9 4)

    next we hold bit 8 stationary and do the same thing with the bit
    at 6:  move it to 7, then place the remaining 3 bits into the
    remaining 7 slots:  (7 3)

    and so on.  we do this with every 0 bit that is decorated with a
    count > 0.  the final answer is the sum of these binary
    coefficients:

    (11 4) (10 4) (9 4) (7 3) (4 1) (3 1)

    """

    zeroes_decorated = decorate_zeroes(width, n)
    total = 0
    for i in range(len(zeroes_decorated)):
        if zeroes_decorated[i] == 0:
            continue

        total += binary_coefficient(i, zeroes_decorated[i] - 1)
    return total


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
    def test_n_bigger_k_bits_1(self):
        n = 358
        width = 12
        expected = binary_coefficient(11, 4) + binary_coefficient(10, 4) + binary_coefficient(9, 4)
        expected += binary_coefficient(7, 3) + binary_coefficient(4, 1) + binary_coefficient(3, 1)
        self.assertEqual(expected, n_bigger_with_k_bits(width, n))

    def test_decorate_zeroes_1(self):
        n = 358
        width = 12
        decoration = decorate_zeroes(width, n)
        self.assertEqual([0, 0, 0, 2, 2, 0, 0, 4, 0, 5, 5, 5], decoration)

        width = 9
        decoration = decorate_zeroes(width, n)
        self.assertEqual([0, 0, 0, 2, 2, 0, 0, 4, 0], decoration)

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
