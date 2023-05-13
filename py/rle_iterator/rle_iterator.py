# starting with my solution to leetcode # 900, run-length iterator.  turn it into a real iterable / iterator.
import unittest
from functools import reduce


#
# todo:  make the encode and decode functions inaccessible to anyone who imports this.
# todo:  implement indexing and slicing

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
        self.encoding = encode(encode_me)
        self.length = len(encode_me) if encode_me is not None else 0

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

    def __iter__(self):
        # has to return an iterator
        return RLEIterator(self)

    def __bool__(self):
        return bool(self.encoding)


class RLETest(unittest.TestCase):
    def test_1(self):
        encode_me = '88888!))*&&%%%%%%%%%%%?'
        rle = RLE(encode_me)
        self.assertEqual(len(encode_me), len(rle))

    def test_2(self):
        encode_me = '88888!))*&&%%%%%%%%%%%?'
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
        encode_me = '88888!))*&&%%%%%%%%%%%?'
        rle1 = RLE(encode_me)
        rle2 = RLE(encode_me)
        self.assertTrue(rle1 == rle2)

    def test_repr(self):
        encode_me = '88888!))*&&%%%%%%%%%%%?'
        rle = RLE(encode_me)
        rle2 = eval(repr(rle))
        self.assertEqual(rle, rle2)

    def test_iter(self):
        encode_me = '88888!))*&&%%%%%%%%%%%?'
        rle = RLE(encode_me)
        itr = iter(rle)
        test_str = ''
        while True:
            try:
                test_str += next(itr)
            except StopIteration:
                break
        self.assertEqual(encode_me, test_str)
        with self.assertRaises(StopIteration):
            next(itr)

    def test_iter_2(self):
        encode_me = '88888!))*&&%%%%%%%%%%%?'
        rle = RLE(encode_me)
        decoded = ''.join([x for x in rle])
        self.assertEqual(encode_me, decoded)

    def test_none(self):
        rle = RLE(None)
        self.assertEqual(0, len(rle))
        itr = iter(rle)

        # yes, do it twice
        with self.assertRaises(StopIteration):
            next(itr)
        with self.assertRaises(StopIteration):
            next(itr)

    def test_empty(self):
        rle = RLE('')
        self.assertEqual(0, len(rle))
        itr = iter(rle)

        # yes, do it twice
        with self.assertRaises(StopIteration):
            next(itr)
        with self.assertRaises(StopIteration):
            next(itr)


class RLEIterator(object):
    def __init__(self, rle):
        self.rle = rle
        self.still_mo = bool(self.rle)
        self.current_run = 0
        self.position_in_current_run = 0  # positions start from 1

    def __iter__(self):
        return self

    def __next__(self):
        # cases:
        #
        # 1.  incrementing the pointer keeps us in the current run
        # 2.  or puts us into a new run
        # 3.  incrementing the pointer runs us off the end of the whole encoding
        #     and we have to raise StopIteration for this and future next() invocations.

        # degenerate cases:
        if not self.still_mo:
            raise StopIteration()

        # case 1:
        if self.position_in_current_run + 1 <= self.rle.encoding[self.current_run][1]:
            self.position_in_current_run += 1
            return self.rle.encoding[self.current_run][0]

        # case 2 and 3:

        # advance the pointer to the beginning of the next run.
        self.current_run += 1
        if self.current_run >= len(self.rle.encoding):
            self.still_mo = False
            raise StopIteration()

        self.position_in_current_run = 1
        return self.rle.encoding[self.current_run][0]




class RLEIteratorTest(unittest.TestCase):
    def test_1(self):
        encoding = [3, 'a', 3, 'b', 0, '#', 3, 'c']
        obj = RLEIterator(encoding)
        result = obj.next(2)
        while result != -1:
            print(result)
            result = obj.next(2)

        # a a a b b b c c c
        #   ^   ^   ^   ^   ^

    def test_2(self):
        encoding = [1, 'a', 1, 'b', 1, 'c']
        obj = RLEIterator(encoding)
        result = obj.next(1)
        while result != -1:
            print(result)
            result = obj.next(1)

    def test_3(self):
        encoding = [1, 'a', 5, 'b', 0, '#', 4, 'c']
        obj = RLEIterator(encoding)
        result = obj.next(10)
        while result != -1:
            print(result)
            result = obj.next(10)

    def test_4(self):
        encoding = [1, 'a', 0, '!', 0, '@', 0, '+', 1, 'b']
        obj = RLEIterator(encoding)
        result = obj.next(1)
        while result != -1:
            print(result)
            result = obj.next(1)
