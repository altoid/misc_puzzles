#!/usr/bin/env python

# given 1 <= a <= b <= 2 ** 1024
#
# find the number of numbers in [a, b] that have a prime number of bits set.
#


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
    """
    given a bit vector, create an array of integers that shows, for each 0 bit position, the number
    of 1 bits from the least significant bit up to and including that position.  put another way,
    show the number of 1 bits to the right of, and including, that position.

    11  10   9   8   7   6   5   4   3   2   1   0
    +---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   |   | 1 |   | 1 | 1 |   |   | 1 | 1 |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+
      5   5   5   0   4   0   0   2   2   0   0   0

    TODO:  currently puts 0 in the location of each 1 bit.  not sure if we should bit-count those too.
    """
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

# TODO: next we have to find all the numbers bigger than n with 1 fewer set bits than n.  then two fewer, etc.
# for the 1 fewer case, find the first 0 following a 1.  set the 0 and clear the 1.  if there is a lower
# 1 bit, clear it.  if there isn't, repeat.
#
# TODO: then we find all the numbers bigger than n with x more bits.  to do this,
# set to 1 the lowest x 0 bits, then run n_bigger_with_same bits.


def add_bits(n, b, width):
    """
    return a value m > n.  we do this by setting to 1 the least significant b 0 bits.
    if the lowest <width> bits are already set, return None.
    if we can only set fewer than b bits, return None.
    """
    if n == 2 ** width - 1:
        return None

    mask = 1
    result = n
    i = 0
    while mask < 2 ** width:
        if mask & n == 0:
            i += 1
            result |= mask
        if i == b:
            break

        mask <<= 1

    if i == b:
        return result


def n_bigger_with_more_bits(n, width):
    """
    given a number n with k bits set, find the number of numbers >= n,
    expressible with <width> bits, that have more k bits set.

    to do this, set to 1 the lowest x 0 bits, then run n_bigger_with_same bits on the result.
    keep doing this until there are no more 0 bits left.
    """
    total = 0
    next = add_bits(n, 1, width)
    print("n = %s, width = %s" % (n, width))
    while next is not None:
        i = n_bigger_with_same_bits(next, width)
        total += i
        print("next = %s, i = %s, total = %s" % (next, i, total))
        next = add_bits(next, 1, width)

    return total


def n_bigger_with_same_bits(n, width):
    """
    given a number n with k bits set, find the number of numbers > n,
    expressible with <width> bits, that have exactly k bits set.

    consider:

     11  10   9   8   7   6   5   4   3   2   1   0
    +---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   |   | 1 |   | 1 | 1 |   |   | 1 | 1 |   |  ==> 358
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
    assert 0 <= k <= n

    from_this = n
    choose_this = k
    if k > (n - k):
        choose_this = n - k

    if (from_this, choose_this) not in binary_coeff_cache:
        if from_this <= 1 or choose_this == 0:
            result = 1
        else:
            result = binary_coefficient(n - 1, k - 1) + binary_coefficient(n - 1, k)

        binary_coeff_cache[(from_this, choose_this)] = result

    return binary_coeff_cache[(from_this, choose_this)]


class MyTest(unittest.TestCase):
    def test_add_1_bit(self):
        n = 358
        adding = [1, 8, 16, 128, 512, 1024, 2048]
        for b in adding:
            result = add_bits(n, 1, 12)
            self.assertEqual(n + b, result)
            n = result

    def test_add_bits_1(self):
        n = 358
        adding = [1, 8, 16, 128, 512, 1024, 2048]
        b = 1
        check = n
        for a in adding:
            result = add_bits(n, b, 12)
            self.assertEqual(check + a, result)
            check += a
            b += 1

    def test_add_bits_2(self):
        self.assertIsNone(add_bits(2 ** 12 - 1, 1, 12))
        self.assertIsNone(add_bits(358, 12, 12))

    def test_n_bigger_more_bits_1(self):
        n = 358
        result = n_bigger_with_more_bits(n, 12)
        self.assertEqual(1439, result)

    def test_n_bigger_more_bits_2(self):
        width = 12
        mask = 1
        allbits = 2 ** width - 1
        while mask < 2 ** width:
            self.assertEqual(1, n_bigger_with_more_bits(allbits ^ mask, width))
            mask <<= 1

    def test_n_bigger_same_bits_1(self):
        n = 358
        width = 12
        expected = binary_coefficient(11, 4) + binary_coefficient(10, 4) + binary_coefficient(9, 4)
        expected += binary_coefficient(7, 3) + binary_coefficient(4, 1) + binary_coefficient(3, 1)
        self.assertEqual(expected, n_bigger_with_same_bits(n, width))

    def test_n_bigger_same_bits_2(self):
        self.assertEqual(0, n_bigger_with_same_bits(4095, 12))

    def test_n_bigger_same_bits_3(self):
        width = 12
        self.assertEqual(0, n_bigger_with_same_bits(2 ** width - 1, width))

    def test_n_bigger_same_bits_4(self):
        self.assertEqual(3, n_bigger_with_same_bits(4087, 12))

    def test_n_bigger_same_bits_5(self):
        self.assertEqual(0, n_bigger_with_same_bits(4094, 12))

    def test_n_bigger_same_bits_6(self):
        width = 12
        mask = 1
        ngreater = 0
        allbits = 2 ** width - 1
        while mask < 2 ** width:
            self.assertEqual(ngreater, n_bigger_with_same_bits(allbits ^ mask, width))
            ngreater += 1
            mask <<= 1

    def test_decorate_zeroes_1(self):
        n = 358
        width = 12
        decoration = decorate_zeroes(width, n)
        self.assertEqual([0, 0, 0, 2, 2, 0, 0, 4, 0, 5, 5, 5], decoration)

        width = 9
        decoration = decorate_zeroes(width, n)
        self.assertEqual([0, 0, 0, 2, 2, 0, 0, 4, 0], decoration)

    def test_binary_coeff_0(self):
        self.assertEqual(1, binary_coefficient(0, 0))

    def test_binary_coeff_1(self):
        self.assertEqual(1, binary_coefficient(1, 0))
        self.assertEqual(1, binary_coefficient(1, 1))

        self.assertEqual(1, binary_coefficient(2, 0))
        self.assertEqual(2, binary_coefficient(2, 1))
        self.assertEqual(1, binary_coefficient(2, 2))

        self.assertEqual(1140, binary_coefficient(20, 3))

    def test_binary_coeff_3_1(self):
        self.assertEqual(3, binary_coefficient(3, 1))

    def test_binary_coeff_3_2(self):
        self.assertEqual(3, binary_coefficient(3, 2))

    def test_binary_coeff_3_3(self):
        self.assertEqual(1, binary_coefficient(3, 3))

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
