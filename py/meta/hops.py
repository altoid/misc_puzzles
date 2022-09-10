#!/usr/bin/env python

# https://www.metacareers.com/profile/coding_puzzles/?puzzle=977526253003069

import unittest
import random
from pprint import pprint


# idea - assuming the frogs hop left to right, gather the frogs together forming larger and
# larger clusters that move to the right.
#
# 1 0 1 0 1 1 0
# 0 1 1 0 1 1 0
# 0 0 1 1 1 1 0
#
# from here each frog leaves starting from the left.
#
# no idea if this is a minimal solution
#
# we identify each cluster by size and distance to the next cluster to the right.
#
# is it just equal to the number of 0s between the first frog and the end?  + the number of frogs?


def generate_case(pads, frogs):
    arr = list(range(1, frogs + 1))
    arr += [0] * ((pads - 1) - frogs)
    random.shuffle(arr)
    arr += [0]
    return arr


def solution(npads, nfrogs, config):
    """
    in the general case we can't construct an array because N is too large
    """

    # 1. sort the list
    # 2. figure out the number of empty pads between the frogs.
    # 3. figure out the number of empty pads between the rightmost frog an the end.
    #    rightmost pad is always empty, do not count it.
    # 4. add these to the number of frogs.

    config_sorted = sorted(config)
    interfrog_gaps = 0
    for i in range(nfrogs - 1):
        gap = (config_sorted[i + 1] - config_sorted[i]) - 1
        interfrog_gaps += gap

    # everything is 1-based because fuck.

    rightmost_gap = (npads - max(config)) - 1

    return interfrog_gaps + rightmost_gap + nfrogs


class MyTest(unittest.TestCase):
    def test1(self):
        pads = 15
        frogs = 7
        arr = generate_case(pads, frogs)
        self.assertEqual(pads, len(arr))
        pprint(arr)

    def test2(self):
        self.assertEqual(4, solution(6, 3, [5, 2, 4]))
