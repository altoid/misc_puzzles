#!/usr/bin/env python

# given 1 <= a <= b <= 2 ** 1024
#
# find the number of numbers in [a, b] that have a prime number of bits set.
#


import unittest
import random

binary_coeff_cache = {}

PRIMES = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
    31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
    73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
    127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
    179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
    233, 239, 241, 251, 257, 263, 269, 271, 277, 281,
    283, 293, 307, 311, 313, 317, 331, 337, 347, 349,
    353, 359, 367, 373, 379, 383, 389, 397, 401, 409,
    419, 421, 431, 433, 439, 443, 449, 457, 461, 463,
    467, 479, 487, 491, 499, 503, 509, 521, 523, 541,
    547, 557, 563, 569, 571, 577, 587, 593, 599, 601,
    607, 613, 617, 619, 631, 641, 643, 647, 653, 659,
    661, 673, 677, 683, 691, 701, 709, 719, 727, 733,
    739, 743, 751, 757, 761, 769, 773, 787, 797, 809,
    811, 821, 823, 827, 829, 839, 853, 857, 859, 863,
    877, 881, 883, 887, 907, 911, 919, 929, 937, 941,
    947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013,
    1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069,
    1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151,
    1153, 1163, 1171, 1181, 1187, 1193, 1201, 1213, 1217, 1223,
    1229, 1231, 1237, 1249, 1259, 1277, 1279, 1283, 1289, 1291,
    1297, 1301, 1303, 1307, 1319, 1321, 1327, 1361, 1367, 1373,
    1381, 1399, 1409, 1423, 1427, 1429, 1433, 1439, 1447, 1451,
    1453, 1459, 1471, 1481, 1483, 1487, 1489, 1493, 1499, 1511,
    1523, 1531, 1543, 1549, 1553, 1559, 1567, 1571, 1579, 1583,
    1597, 1601, 1607, 1609, 1613, 1619, 1621, 1627, 1637, 1657,
    1663, 1667, 1669, 1693, 1697, 1699, 1709, 1721, 1723, 1733,
    1741, 1747, 1753, 1759, 1777, 1783, 1787, 1789, 1801, 1811,
    1823, 1831, 1847, 1861, 1867, 1871, 1873, 1877, 1879, 1889,
    1901, 1907, 1913, 1931, 1933, 1949, 1951, 1973, 1979, 1987,
    1993, 1997, 1999, 2003, 2011, 2017, 2027, 2029, 2039
]


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

def successor_with_one_fewer_bits(n, width):
    """
    find the smallest number m > n such that m 1 fewer bits.  return None if no number meets
    this condition.

    examples.  width is 16 in all cases.

    1101 1110 0101 0010 = 56914
    1101 1110 0110 0000 = 56928
    1101 1110 1000 0000 = 56960
    1111 1100 0000 0000 = 64512
    None
    """
    if n == 0:
        return None

    # clear the lowest-order 1 bit.
    m = n & (n - 1)

    # in this case, n is a power of 2 and there is no successor with fewer bits.
    if m == 0:
        return None

    # if m is all 1s to the left of all 0s, then there is no successor with fewer bits.
    # we've already removed one bit and we can't make m bigger by moving bits around.
    # i.e. 111....100000...000
    bits = get_bits(m)
    bits = [0] * (width - len(bits)) + bits

    first_zero = None
    last_one = None
    i = 0
    for b in bits:
        if b == 1:
            last_one = i
        i += 1

    # now find the first zero to the left of the last 1
    i = last_one - 1
    while i >= 0:
        if bits[i] == 0:
            first_zero = i
            break
        i -= 1

    if first_zero is None:
        return None

    # now swap them
    bits[last_one], bits[first_zero] = bits[first_zero], bits[last_one]

    # change the bits into a number
    result = 0
    for b in bits:
        result *= 2
        if b:
            result += 1

    return result


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
    expressible with <width> bits, that have more than k bits set.

    to do this, set to 1 the lowest x 0 bits, then run n_bigger_with_same bits on the result.
    keep doing this until there are no more 0 bits left.
    """
    total = 0
    next = add_bits(n, 1, width)
    while next is not None:
        # add 1 because n_bigger_with_same_bits returns a count for the number of numbers strictly
        # greater than next.  but next is already bigger than n, so we have to count that too.
        i = n_bigger_with_same_bits(next, width)
        total += i
        next = add_bits(next, 1, width)

    return total


def n_bigger_with_same_bits(n, width):
    """
    given a number n with k bits set, find the number of numbers >= n,
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
    total = 1  # including n in the count
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
    def successor_check(self, m, n):
        bits_n = get_bits(n)
        bits_m = get_bits(m)
        self.assertEqual(sum(bits_m) + 1, sum(bits_n))

    def test_successor_fewer_bits_1(self):
        n = 56914
        m = 56928
        self.assertEqual(m, successor_with_one_fewer_bits(n, 12))
        self.successor_check(m, n)

        n = 56928
        m = 56960
        self.assertEqual(m, successor_with_one_fewer_bits(n, 12))
        self.successor_check(m, n)

        n = 56960
        m = 64512
        self.assertEqual(m, successor_with_one_fewer_bits(n, 12))
        self.successor_check(m, n)

        self.assertIsNone(successor_with_one_fewer_bits(64512, 12))

    def test_successor_fewer_bits_2(self):
        self.assertIsNone(successor_with_one_fewer_bits(1, 12))
        self.assertIsNone(successor_with_one_fewer_bits(0, 12))
        self.assertIsNone(successor_with_one_fewer_bits(2 ** 12 - 1, 12))
        self.assertIsNone(successor_with_one_fewer_bits(2 ** 5, 12))

    def test_successor_fewer_bits_3(self):
        self.assertIsNone(successor_with_one_fewer_bits(7, 3))
        self.assertIsNone(successor_with_one_fewer_bits(6, 3))
        self.assertIsNone(successor_with_one_fewer_bits(4, 3))

    def test_successor_fewer_bits_4(self):
        self.assertEqual(4, successor_with_one_fewer_bits(3, 3))
        self.assertEqual(12, successor_with_one_fewer_bits(7, 5))

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

    def test_add_bits_3(self):
        self.assertIsNone(add_bits(1, 1, 1))

    def test_n_bigger_more_bits_1(self):
        n = 358
        result = n_bigger_with_more_bits(n, 12)
        self.assertEqual(2460, result)

    def test_n_bigger_more_bits_2(self):
        width = 12
        mask = 1
        allbits = 2 ** width - 1
        while mask < 2 ** width:
            self.assertEqual(1, n_bigger_with_more_bits(allbits ^ mask, width))
            mask <<= 1

    def test_n_bigger_more_bits_3(self):
        self.assertEqual(0, n_bigger_with_more_bits(1, 1))

    def test_n_bigger_same_bits_1(self):
        n = 358
        width = 12
        expected = 1
        expected += binary_coefficient(11, 4) + binary_coefficient(10, 4) + binary_coefficient(9, 4)
        expected += binary_coefficient(7, 3) + binary_coefficient(4, 1) + binary_coefficient(3, 1)
        self.assertEqual(expected, n_bigger_with_same_bits(n, width))

    def test_n_bigger_same_bits_2(self):
        self.assertEqual(1, n_bigger_with_same_bits(4095, 12))

    def test_n_bigger_same_bits_3(self):
        width = 12
        self.assertEqual(1, n_bigger_with_same_bits(2 ** width - 1, width))

    def test_n_bigger_same_bits_4(self):
        self.assertEqual(4, n_bigger_with_same_bits(4087, 12))

    def test_n_bigger_same_bits_5(self):
        self.assertEqual(1, n_bigger_with_same_bits(4094, 12))

    def test_n_bigger_same_bits_6(self):
        width = 12
        mask = 1
        ngreater = 1
        allbits = 2 ** width - 1
        while mask < 2 ** width:
            self.assertEqual(ngreater, n_bigger_with_same_bits(allbits ^ mask, width))
            ngreater += 1
            mask <<= 1

    def test_n_bigger_same_bits_7(self):
        self.assertEqual(1, n_bigger_with_same_bits(1, 1))

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
