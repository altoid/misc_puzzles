#!/usr/bin/env python

import unittest
from pprint import pprint


# reference:  https://web.stanford.edu/class/cs97si/10-string-algorithms.pdf

def preprocess(pattern):
    # returns pi table for pattern
    if not pattern:
        return []

    length = len(pattern)
    result = [0] * length

    beginning = 0
    counter = 0
    p = 1
    while p < length:
        if pattern[p] == pattern[beginning]:
            counter += 1
            result[p] = counter
            beginning += 1
        else:
            counter = 0
            beginning = 0
        p += 1

    result = [-1] + result
    return result


def match(text, pattern):
    # return the first index in text where pattern is found, or else None
    stop = len(text) - len(pattern) + 1
    if stop < 0:
        return None

    pi_table = preprocess(pattern)
    #print(pi_table)

    anchor = 0
    while anchor < stop:
        # print("--------------")
        # print(text)
        # print("%s%s" % (' ' * anchor, pattern))
        p = 0
        while p < len(pattern) and pattern[p] == text[anchor + p]:
            p += 1
        if p == len(pattern):
            return anchor

        # print("anchor is %s, mismatch at %s" % (anchor, anchor + p))
        # p is the number of letters we've matched in this round.  if p is 0, then table[0] = -1, so
        # we will still shift by at least 1.
        shiftby = p - pi_table[p]
        # print("shifting by %s" % shiftby)
        anchor += shiftby


class MatchTest(unittest.TestCase):
    def test_1(self):
        text = 'ababababca'
        pattern = 'abc'
        expecting = 6

        index = match(text, pattern)
        self.assertEqual(expecting, index)

    def test_2(self):
        text = 'abc abcdab abcdabcdabde'
        pattern = 'abcdabd'
        expecting = 15

        index = match(text, pattern)
        self.assertEqual(expecting, index)


class PreprocessTest(unittest.TestCase):
    def test_1(self):
        pattern = 'ababababca'
        expecting = [-1, 0, 0, 1, 2, 3, 4, 5, 6, 0, 1]

        pi_table = preprocess(pattern)
        self.assertEqual(expecting, pi_table)

    def test_2(self):
        pattern = 'a'
        expecting = [-1, 0]

        pi_table = preprocess(pattern)
        self.assertEqual(expecting, pi_table)

    def test_3(self):
        pattern = ''
        expecting = []

        pi_table = preprocess(pattern)
        self.assertEqual(expecting, pi_table)

    def test_4(self):
        pattern = 'abcdabd'
        expecting = [-1, 0, 0, 0, 0, 1, 2, 0]

        pi_table = preprocess(pattern)
        self.assertEqual(expecting, pi_table)
