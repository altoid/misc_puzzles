# starting with my solution to leetcode # 900, run-length iterator.  turn it into a real iterable / iterator.
import unittest
from functools import reduce


#
# todo:  make the encode and decode functions inaccessible to anyone who imports this.
# todo:  implement iteration
# todo:  implement indexing and slicing
#

def enc_helper(acc, value):
    if acc[-1][0] == value:
        acc[-1][1] += 1
    else:
        acc.append([value, 1])

    return acc


def encode(s):
    """
    produce a run-length encoding of s.

    given:

        88888!))*&&%%%%%%%%%%%

    return:

        [['8', 5], ['!', 1], [')', 2], ['*', 1], ['&', 2], ['%', 11]]
    """
    if not s:
        return []

    acc = [[s[0], 1]]
    result = reduce(enc_helper, s[1:], acc)

    return result


def decode(enc):
    """
    given:

        [['8', 5], ['!', 1], [')', 2], ['*', 1], ['&', 2], ['%', 11]]

    return:

        88888!))*&&%%%%%%%%%%%
    """
    return ''.join(list(map(lambda x: x[0] * x[1], enc)))


class RLE(object):
    """
    maintain a run length encoding of the string passed to the constructor.
    """
    def __init__(self, encode_me):
        self.length = len(encode_me)
        self.encoding = encode(encode_me)

    def __len__(self):
        return self.length

    def __str__(self):
        return decode(self.encoding)

    def __repr__(self):
        return "%s('%s')" % (self.__class__.__name__, str(self))

    def __eq__(self, other):
        if not isinstance(other, RLE):
            return NotImplemented

        return other.encoding == self.encoding and self.length == other.length


class RLETest(unittest.TestCase):
    def test_1(self):
        encode_me = '88888!))*&&%%%%%%%%%%%'
        rle = RLE(encode_me)
        self.assertEqual(len(encode_me), len(rle))

    def test_2(self):
        encode_me = '88888!))*&&%%%%%%%%%%%'
        rle = RLE(encode_me)
        self.assertEqual(encode_me, str(rle))

    def test_3(self):
        encode_me = ''
        rle = RLE(encode_me)
        self.assertEqual(len(encode_me), len(rle))

    def test_4(self):
        encode_me = ''
        rle = RLE(encode_me)
        self.assertEqual(encode_me, str(rle))

    def test_eq(self):
        encode_me = '88888!))*&&%%%%%%%%%%%'
        rle1 = RLE(encode_me)
        rle2 = RLE(encode_me)
        self.assertTrue(rle1 == rle2)

    def test_repr(self):
        encode_me = '88888!))*&&%%%%%%%%%%%'
        rle = RLE(encode_me)
        rle2 = eval(repr(rle))
        self.assertEqual(rle, rle2)


class RLEIterator(object):
    def __init__(self, encoding):
        self.encoding = encoding
        self.current_run = 0
        self.position_in_current_run = 0  # positions start from 1
        self.still_mo = bool(self.encoding)

    def point_to_next_run(self):
        """
        set the pointer to the beginning of the next nontrivial run.  sets still_mo to False if doing so runs off
        the end of the encoding.  returns the number of places the pointer was moved, or -1 if we couldn't move it.
        """
        advance = self.encoding[self.current_run] - self.position_in_current_run + 1
        self.current_run += 2
        while self.current_run < len(self.encoding) and self.encoding[self.current_run] == 0:
            self.current_run += 2

        if self.current_run >= len(self.encoding):
            self.still_mo = False
            return -1

        self.position_in_current_run = 1

        return advance

    def next(self, n):

        # cases:
        #
        # 1.  incrementing the pointer keeps us in the current run
        # 2.  or puts us into a new run
        # 2a. possibly skipping 1 or more whole runs along the way
        # 3.  incrementing the pointer runs us off the end of the whole encoding
        #     and we have to return -1 for this and future next() invocations.

        # degenerate cases:
        if not self.still_mo:
            return -1

        # case 1:
        if self.position_in_current_run + n <= self.encoding[self.current_run]:
            self.position_in_current_run += n
            return self.encoding[self.current_run + 1]

        # case 2:

        # advance the pointer to the beginning of the next run.
        advance = self.point_to_next_run()
        if advance < 0:
            return -1

        n -= advance

        while self.still_mo and n - self.encoding[self.current_run] > 0:
            n -= self.encoding[self.current_run]
            self.current_run += 2
            if self.current_run >= len(self.encoding):
                self.still_mo = False

        if not self.still_mo:
            return -1

        self.position_in_current_run += n
        return self.encoding[self.current_run + 1]
