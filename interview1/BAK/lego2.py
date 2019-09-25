#!/usr/bin/env python

import sys
import math
import fractions

choose_cache = {}
def choose(n, r):
    if (n, r) not in choose_cache:
        result = int( reduce(lambda x, y: x*y, (fractions.Fraction(n-i, i+1) for i in range(r)), 1) )
#    print "choose(%s %s) = %s" % (n, r, result)
        choose_cache[(n, r)] = result
        choose_cache[(n, n - r)] = result

    return choose_cache[(n, r)]

def brick_combo(n):
    '''
    how many ways are there to partition n
    into 1, 2, 3, 4?
    '''

    sum = 0
    for i in xrange(4):
        sum += choose(n - 1, i)
    return sum

def count(height_n, width_m):

    print "111111111"
    result = brick_combo(width_m) ** height_n
    print "222222222"

    p2 = [2 ** (x - 1) for x in xrange(width_m, 0, -1)]
    print p2
    print "333333333"

    heights = [x ** height_n for x in p2]
    print heights
    print "444444444"

#    print result
#    print p2
#    print heights

    multiplier = -1
    for seams in xrange(1, width_m):
#        print "calculating choose(%s, %s)" % (width_m - 1, seams)
        coefficient = choose(width_m - 1, seams)
        addend = (multiplier * coefficient * heights[seams])
        result += addend
        multiplier = -multiplier

    print "555555555"
    result = result % 1000000007
    return result


if __name__ == '__main__':
    text = sys.stdin.read()
    lines = text.split('\n')
    ncases = int(lines[0].strip())

    for i in range(ncases):
        height_n, width_m = (int(x) for x in lines[i + 1].split())
        print count(height_n, width_m)
