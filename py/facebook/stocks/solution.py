#!/usr/bin/env python

import unittest

# this solves parts I, II, and III

# identify all the increasing subarrays

def find_subarrays(a):
    transactions = []
    start = 0

    for p in xrange(1, len(a)):
        if a[p] >= a[p - 1]:
            # continue current subarray
            continue

        end = p - 1
        if end > start:
            transactions.append((start, end))
        start = p

    end = len(a) - 1
    if end > start:
        transactions.append((start, end))

    # sort the transactions by decreasing magnitude
    result = sorted(transactions, cmp=lambda x, y: cmp(a[x[1]] - a[x[0]], a[y[1]] - a[y[0]]), reverse=True)

    for r in result:
        delta = a[r[1]] - a[r[0]]
        print "a[%s] - a[%s] = %s" % (r[1], r[0], delta)


class MyTest(unittest.TestCase):
    def test1(self):
        a = [1, 7, 2, 4, 6, 1, 8, 4]
        find_subarrays(a)

    def test2(self):
        a = [7, 6, 5, 4, 3, 2, 1]
        find_subarrays(a)
