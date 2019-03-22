#!/usr/bin/env python

import unittest

def partition(a, l, r, n):
    # array, left bound, right bound, number of partitions

    if n == 1:
        result = [[l, r]]
        yield result
        return

    f = (r - l + 1) - n

    for i in xrange(f):
        x = [[l, l + i + 1]]
        for p in partition(a, l + i + 1, r, n - 1):
            result = x + p
            yield result

def partition_sums(a, partition):
    return [sum(a[x[0]:x[1]]) for x in partition]

def minmax(a, n):
    mmax = None

    for p in partition(a, 0, len(a), n):
        mx = max(partition_sums(a, p))
        if mmax is None:
            mmax = mx
        else:
            mmax = min(mmax, mx)

    if mmax < 1:
        return -1

    return mmax

class MyTest(unittest.TestCase):
    def test1(self):
        a = [12,34,67,90]
        self.assertEqual(113, minmax(a, 2))

