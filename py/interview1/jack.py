#!/usr/bin/env python

import sys

#
# tree traversal not the way to go
#
# ordered subsets of 1..N
# eliminate all where there is some leftmost prefix that adds up to k
#
# max step is 2000 * 2001 / 2 = 2001000
# max k is 4000000
# quickie if k > 2001000

# make list N..1
# mask off rightmost bitwise
# keep going until we find one with no rightmost suffix that adds to k

class MyBreak(Exception):
    pass

def maxStep(n, k):
    numbers = [x for x in xrange(n, 0, -1)]

    bitmask = (1 << n) - 1
    while True:
        mask = [int(x) for x in str(bin(bitmask))[2:].zfill(n)]
        masked = [x * y for x, y in zip(numbers, mask)]

        try:
            # check for a rightmost suffix that adds up to k
            for j in xrange(len(masked)):
                if sum(masked[j:]) == k:
                    raise MyBreak("%s has a suffix that adds to %s" % (masked, k))
            return sum(masked)
        except MyBreak as e:
            pass

        bitmask -= 1

    return 0


if __name__ == '__main__':
    text = sys.stdin.read()
    lines = text.split('\n')

    n = int(lines[0].strip())
    k = int(lines[1].strip())

    print maxStep(n, k)
