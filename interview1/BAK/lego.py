#!/usr/bin/env python

import math
import pprint

pp = pprint.PrettyPrinter()

def choose(n, r):
    return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))

def count(height_n, width_m):

#    total # of combinations
#    - number that have a seam in one position
#    + number that have a seam in two positions
#    - number that have a seam in 3 positions
#
#    +/- number that have a seam in width - 1 positions

    result = brick_combo(width_m) ** height_n
    print ">>>>>> initial result:  %s" % result

    multiplier = -1
    partition_dict = organize_partitions(partition(width_m))
    for seams in xrange(1, width_m):

        print "seams: %s  coefficient (%s %s)" % (
            seams, width_m - 1, seams)
        coefficient = choose(width_m, seams)

        ntowers = seams + 1

        print "%s: %s" % (ntowers, pp.pformat(partition_dict[ntowers]))
        towers = partition_dict[ntowers]

        partial_sum = 0
        for t in towers:
            partial_product = 1
            for s in t:
                partial_product *= (brick_combo(s) ** height_n)
            print "checking %s:  pproduct = %s" % (t, partial_product)

            partial_sum += partial_product
        print "partial sum for seams = %s: %s" % (seams, partial_sum)
        d = partial_sum * multiplier
        result += d

        multiplier = -multiplier

    result = result % 1000000007
    print "### final result:  %s" % result
    return result

def organize_partitions(partitions):
    '''
    partitions are sets of comma separated strings
    turn this into a dict
    key is length of partition
    value is list of lists of ints whose length is the key
    '''

    result = {}
    for p in partitions:
        sublist = [int(x) for x in p.split(',')]
        l = len(sublist)
        if l not in result:
            result[l] = []
        result[l].append(sublist)

    return result

def partition(n):
    '''
    generate partitions of the integer n

    returns a set of comma-separated strings, each string is a partition
    '''
    if n == 1:
        return set('1')

    result = set()
    for k in range(1, n):
        # result is the set of all partitions of n - k, to which k has been added.
        # do this for all k [1..n)
        # then put n into the set
        sub = partition(n - k)
        for s in sub:
            ilist = [x for x in s.split(',')]
            for i in xrange(len(ilist)):
                j = ','.join(ilist[:i] + [str(k)] + ilist[i:])
                result.add(j)
            j = ','.join(ilist + [str(k)])
            result.add(j)

    result.add(','.join([str(n)]))
    return result

def brick_combo(n):
    '''
    how many ways are there to partition n
    into 1, 2, 3, 4?
    '''

    if n == 1:
        return 1

    if n == 2:
        return 1 + brick_combo(1)

    if n == 3:
        return 1 + brick_combo(1) + brick_combo(2)

    if n == 4:
        return 1 + brick_combo(3) + brick_combo(2) + brick_combo(1)

    return brick_combo(n - 1) + brick_combo(n - 2) + brick_combo(n - 3) + brick_combo(n - 4)

# we also need # of ways to partition
# a row of width N into 2, 3, .. N chunks


# 1:
# 1
#
# 2:
# 2
# 1 1
#
# 3:
# 3
# 2 1
# 1 2
# 1 1 1
# 
# 4:
# 4
# 1 3
# 1 2 1
# 1 1 2
# 1 1 1 1
# 2 1 1
# 2 2
# 3 1
# 
# 5
# 
# 1 4
# 1 1 3
# 1 1 2 1
# 1 1 1 2
# 
# 1 1 1 1 1
# 1 2 1 1
# 1 2 2
# 1 3 1
# 
# 2 3
# 2 2 1
# 2 1 2
# 2 1 1 1
# 
# 3 2
# 3 1 1
# 4 1

