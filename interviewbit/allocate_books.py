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

a = [1,7,2,4,6,1,8,0,9]

#for p in partition(a, 0, len(a), 1):
#    print p
#
#for p in partition(a, 0, len(a), 2):
#    print p
#

def minmax(a, n):
    mmax = None

    for p in partition(a, 0, len(a), n):
#        print p
#        print partition_sums(a, p)
        mx = max(partition_sums(a, p))
        if mmax is None:
            mmax = mx
        else:
            mmax = min(mmax, mx)

    if mmax < 1:
        return -1

    return mmax

print a, minmax(a, 3)

a =  [12,34,67,90]
print a, minmax(a, 2)

