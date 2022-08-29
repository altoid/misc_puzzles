#!/usr/bin/env python


# not part of prime bits solution, but related fun problem:  given a positive integer, find the next
# largest number with the same number of bits set.  so if we are given this:
#
#     +---+---+---+---+---+---+---+---+---+---+---+---+
#     |   |   |   | 1 |   | 1 | 1 |   |   | 1 | 1 |   |
#     +---+---+---+---+---+---+---+---+---+---+---+---+
#
# the answer is this:
#
#     +---+---+---+---+---+---+---+---+---+---+---+---+
#     |   |   |   | 1 |   | 1 | 1 |   | 1 |   |   | 1 |
#     +---+---+---+---+---+---+---+---+---+---+---+---+
#
# the next few in the sequence are
#
#  0 0 0 1 0 1 1 0 1 0 1 0
#  0 0 0 1 0 1 1 0 1 1 0 0
#  0 0 0 1 0 1 1 1 0 0 0 1
#
# method:  traverse from the right and find the first 0 following a 1.  if there is no 0 following
# (to the left of) a 1, the number has no successor.
#
# otherwise, swap the 0 with the 1 to its right.  any 1s to the right of this must be moved
# all the way to the right.

import unittest
import random


def same_bits_successor(n, width):
    """
    width is the max number of bits we will permit in any successor.
    """

    assert n < 2 ** width

    if n == 0:
        return None

    # convert the number to a bit vector

    n_str = bin(n)[2:]
    bits = list(map(int, n_str))

    # flip the bit vector around so the indexing arithmetic is easier.
    bits = bits[::-1]

    # add 0 padding if necessary
    bits += [0] * (width - len(bits))

    # find the first 0 that comes after a 1.
    i = 0
    zero_span = None
    if bits[i] == 0:
        zero_span = [i, i]

    while bits[i] == 0:
        # we know we will find at least one 1 bit (we already checked n == 0)
        if zero_span:
            zero_span[1] = i
        i += 1

    one_span = [i, i]
    while i < width and bits[i] == 1:
        one_span[1] = i
        i += 1

    if i == width:
        return None

    # swap the 1 and 0
    bits[i], bits[i - 1] = bits[i - 1], bits[i]
    one_span[1] -= 1

    # now swap the 0 and 1 spans
    if zero_span and one_span[0] <= one_span[1]:
        ones = [1] * (one_span[1] - one_span[0] + 1)
        zeroes = [0] * (zero_span[1] - zero_span[0] + 1)
        bits = ones + zeroes + bits[i - 1:]

    # flip the bit vector around and change it into a number
    bits = bits[::-1]
    result = 0
    for b in bits:
        result *= 2
        if b:
            result += 1

    return result


class MyTest(unittest.TestCase):
    def test_degenerate_cases(self):
        self.assertIsNone(same_bits_successor(0, 8))
        self.assertIsNone(same_bits_successor(1, 1))
        self.assertIsNone(same_bits_successor(2 ** 8 - 1, 8))
        self.assertIsNone(same_bits_successor(7 << 5, 8))

    def test_1(self):
        n = 7
        w = 6
        successors = [11, 13, 14, 19, 21, 22, 25, 26, 28]
        for s in successors:
            self.assertEqual(s, same_bits_successor(n, w))
            n = s

    def test_2(self):
        self.assertEqual(19, same_bits_successor(14, 6))

    def test_3(self):
        self.assertEqual(21, same_bits_successor(19, 6))

