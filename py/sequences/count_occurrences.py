#!/usr/bin/env python

# given strings S and T, find the number of times T appears in S as a subsequence.


import unittest

helper_calls = 0


def helper(s, t, i, j, level):
    print("%s(i = %s, j = %s)" % ("    " * level, i, j))
    global helper_calls
    helper_calls += 1
    if i == len(s) and j == len(t):
        return 1

    if i == len(s):
        return 0

    count = 0
    if s[i] == t[j]:
        count += helper(s, t, i + 1, j + 1, level + 1)
    count += helper(s, t, i + 1, j, level + 1)

    return count


def count_subsequences(s, t):
    if len(t) > len(s):
        return 0

    global helper_calls
    helper_calls = 0

    result = helper(s, t, 0, 0, 0)
    print("helper_calls:  %s" % helper_calls)
    return result


if __name__ == '__main__':
    pass


class MyTest(unittest.TestCase):
    def test_1(self):
        s = 'ababc'
        t = 'abc'
        expecting = 3
        self.assertEqual(expecting, count_subsequences(s, t))
