#!/usr/bin/env python

import unittest
from pprint import pprint


# references
#
# https://web.stanford.edu/class/cs97si/10-string-algorithms.pdf
# http://www.cs.kent.edu/~dragan/DAAA/PatternMatching.pdf

def preprocess(pattern):
    # returns pi table for pattern
    if not pattern:
        return []

    result = [0] * len(pattern)
    beginning = 0
    p = 1
    prefixlen = 0
    while p < len(pattern):
        if pattern[p] != pattern[beginning]:
            prefixlen = 0
            result[p] = prefixlen
            beginning = 0
            if pattern[p] != pattern[beginning]:
                p += 1
        else:
            prefixlen += 1
            result[p] = prefixlen
            beginning += 1
            p += 1

    return [-1] + result

def match(text, pattern):
    # return the first index in text where pattern is found, or else None
    stop = len(text) - len(pattern) + 1
    if stop < 0:
        return -1

    pi_table = preprocess(pattern)
    print(pi_table)

    anchor = 0
    while anchor < stop:
        print("--------------")
        print(text)
        print("%s%s" % (' ' * anchor, pattern))
        p = 0
        while p < len(pattern) and pattern[p] == text[anchor + p]:
            p += 1
        if p == len(pattern):
            return anchor

        print("anchor is %s, p is %s, mismatch at %s" % (anchor, p, anchor + p))
        # p is the number of letters we've matched in this round.  if p is 0, then table[0] = -1, so
        # we will still shift by at least 1.
        shiftby = p - pi_table[p]
        print("shifting by %s" % shiftby)
        anchor += shiftby

    return -1


if __name__ == '__main__':
    #pattern = 'aabaaac'
    #pattern = 'abcdabcdabde'
    #pattern = 'abcdabd'
    pattern = 'aaacecaa'
    result = preprocess(pattern)
    print(result)

class MatchTest(unittest.TestCase):
    def test_3(self):
        text = "aabaaabaaac"
        pattern = "aabaaac"
        expecting = 4

        index = match(text, pattern)
        self.assertEqual(expecting, index)

    def test_2(self):
        text = 'ababababca'
        pattern = 'abc'
        expecting = 6

        index = match(text, pattern)
        self.assertEqual(expecting, index)

    def test_1(self):
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

    def test_5(self):
        pattern = 'aabaaac'
        expecting = [-1, 0, 1, 0, 1, 2, 1, 0]

        pi_table = preprocess(pattern)
        self.assertEqual(expecting, pi_table)
