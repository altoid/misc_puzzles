#!/usr/bin/env python

# given a list of ints and another int k, find all of the subarrays that add up to k

import random
import unittest
from pprint import pprint


def running_sum(arr):
    """
    given a list of ints arr, return another list b such that b[i] == SUM(arr[0..i])
    """
    total = 0
    result = []
    for a in arr:
        total += a
        result.append(total)

    return result


def solution(arr, k):
    arr_running_sum = running_sum(arr)

    # maps each value in arr_running_sum to its position(s) in that list.
    running_sums_to_positions = {}

    # maps each value in arr_running_sum to what you have to add to it to get k.
    running_sums_to_addends = {}

    i = 0
    for v in arr:
        if v == k:
            # this is a special case.  initialize running_sums_to_positions so that
            # we will always get arr[k] as a single-element subarray.
            if 0 not in running_sums_to_positions:
                running_sums_to_positions[0] = []
            running_sums_to_positions[0].append(i - 1)
        i += 1

    i = 0
    for v in arr_running_sum:
        if v not in running_sums_to_positions:
            running_sums_to_positions[v] = []
        running_sums_to_positions[v].append(i)
        i += 1

    # running_sum[i] == k is also a special case
    for v in arr_running_sum:
        if v == k:
            if 0 not in running_sums_to_positions:
                running_sums_to_positions[0] = []
            if -1 not in running_sums_to_positions[0]:
                running_sums_to_positions[0].append(-1)

    for v in arr_running_sum:
        if v not in running_sums_to_addends:
            running_sums_to_addends[v] = v - k

    result = set()
    for i in range(len(arr)):
        minuend = arr_running_sum[i]

        if minuend not in running_sums_to_addends:
            continue

        if running_sums_to_addends[minuend] not in running_sums_to_positions:
            continue

        subtrahends = running_sums_to_positions[running_sums_to_addends[minuend]]
        subtrahends = filter(lambda x: x < i, subtrahends)

        if subtrahends:
            for s in subtrahends:
                t = (s + 1, i + 1)
                result.add(t)
                # print("range (%s, %s)" % t)
                # print(arr[t[0]:t[1]])

    if result:
        return result


if __name__ == '__main__':
    arr = [random.randint(-10, 10) for _ in range(111)]
    print(arr)
    result = solution(arr, 5)

    if result:
        shortest = min(result, key=lambda x: x[1] - x[0])
        if shortest:
            print("shortest subarrays:")
            sub = arr[shortest[0]:shortest[1]]
            print("arr[%s:%s] = %s, sum = %s, length = %s" % (shortest[0], shortest[1], sub, sum(sub), shortest[1] - shortest[0]))

        longest = max(result, key=lambda x: x[1] - x[0])
        if longest:
            print("longest subarrays:")
            sub = arr[longest[0]:longest[1]]
            print("arr[%s:%s] = %s, sum = %s, length = %s" % (longest[0], longest[1], sub, sum(sub), longest[1] - longest[0]))

    # for r in result:
    #     sub = arr[r[0]:r[1]]
    #     print("arr[%s:%s] = %s, sum = %s" % (r[0], r[1], sub, sum(sub)))


class MyTest(unittest.TestCase):
    def test1(self):
        test_arr = [1] * 15
        expected = list(range(1, 16))
        self.assertEqual(expected, running_sum(test_arr))

    def test2(self):
        test_arr = [5]
        expected = {(0, 1)}
        self.assertEqual(expected, solution(test_arr, 5))

    def test3(self):
        test_arr = [1, 4]
        expected = {(0, 2)}
        self.assertEqual(expected, solution(test_arr, 5))

    def test4(self):
        test_arr = [1, 4, 5]
        expected = {(0, 2), (2, 3)}
        self.assertEqual(expected, solution(test_arr, 5))

    def test5(self):
        test_arr = [6]
        self.assertIsNone(solution(test_arr, 5))

    def test6(self):
        test_arr = [3, 2, 1, 1, 1, 1, 1, 2, 3, 5, 5]
        expected = {(0, 2), (1, 5), (2, 7), (10, 11), (9, 10), (7, 9), (4, 8)}
        self.assertEqual(expected, solution(test_arr, 5))

    def test7(self):
        test_arr = []
        self.assertIsNone(solution(test_arr, 5))

    def test8(self):
        test_arr = [0, 0, 5]
        expected = {(0, 3), (1, 3), (2, 3)}
        self.assertEqual(expected, solution(test_arr, 5))

    def test9(self):
        test_arr = [1] * 10
        expected = {(0, 5), (1, 6), (2, 7), (3, 8), (4, 9), (5, 10)}
        self.assertEqual(expected, solution(test_arr, 5))
