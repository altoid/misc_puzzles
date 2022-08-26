#!/usr/bin/env python

# https://www.metacareers.com/profile/coding_puzzles/?puzzle=228269118726856

# A positive integer is considered uniform if all of its digits are
# equal. For example, 222222 is uniform, while 223223 is not.  Given two
# positive integers AA and BB, determine the number of uniform integers
# between AA and BB, inclusive.  Please take care to write a solution
# which runs within the time limit.
#
# Constraints
# 1 <= A <= B <= 10 ** 12
#
# Sample test case #1
# A = 75
# B = 300
# Expected Return Value = 5
#
# Sample test case #2
# A = 1
# B = 9
# Expected Return Value = 9
#
# Sample test case #3
# A = 999999999999
# B = 999999999999
# Expected Return Value = 1
#
# Sample Explanation
#
# In the first case, the uniform integers between 75 and 300 are
# 77, 88, 99, 111, and 222.
#
# In the second case, all 9 single-digit integers between 1 and 9
# (inclusive) are uniform.
#
# In the third case, the single integer under consideration
# (999,999,999,999) is uniform.

import unittest
import random


def next_uniform_ge(n):
    if n < 10:
        return n

    # observation:  answer always has same number of digits as n.
    # traverse the digits.  keep going until you find a digit != to the first
    # digit.

    digits = list(str(n))
    digits = list(map(int, digits))
    ndigits = len(digits)

    for d in digits[1:]:
        if d == digits[0]:
            continue

        if d < digits[0]:
            result = [str(digits[0])] * ndigits
        else:
            result = [str(digits[0] + 1)] * ndigits

        result = ''.join(result)
        return int(result)

    return n


def next_uniform_le(n):
    ge = next_uniform_ge(n)
    if ge == n:
        return n

    digits = list(str(ge))
    digits = list(map(int, digits))
    ndigits = len(digits)

    if digits[0] > 1:
        result = [str(digits[0] - 1)] * ndigits
        result = ''.join(result)
        return int(result)

    result = 10 ** (ndigits - 1) - 1
    return result


def uniform_in_range(a, b):
    smallest_uniform = next_uniform_ge(a)
    biggest_uniform = next_uniform_le(b)

    # will smallest > biggest ever happen?
    # a = b = 4321, smalllest = 4444, biggest 3333
    # ==> return 0

    if smallest_uniform > biggest_uniform:
        return 0

    # now the number of digits in each is a relevant factor.
    smallest_str = str(smallest_uniform)
    digits_in_smallest = len(smallest_str)
    digit_of_smallest = int(smallest_str[0])

    biggest_str = str(biggest_uniform)
    digits_in_biggest = len(biggest_str)
    digit_of_biggest = int(biggest_str[0])

    if digits_in_biggest == digits_in_smallest:
        return digit_of_biggest - digit_of_smallest + 1

    return (10 - digit_of_smallest) + digit_of_biggest + 9 * (digits_in_biggest - digits_in_smallest - 1)


if __name__ == '__main__':
    x = random.randint(1, 10 ** 12)
    y = random.randint(1, 10 ** 12)
    a = min(x, y)
    b = max(x, y)
    print(a, b, uniform_in_range(a, b))


class MyTest(unittest.TestCase):
    def test_uniform_3(self):
        self.assertEqual(1, uniform_in_range(319454609043, 390169680506))

    def test_uniform_2(self):
        self.assertEqual(18, uniform_in_range(1, 100))
        self.assertEqual(17, uniform_in_range(2, 100))
        self.assertEqual(9, uniform_in_range(10, 100))
        self.assertEqual(27, uniform_in_range(1, 1000))
        self.assertEqual(28, uniform_in_range(1, 1111))

    def test_uniform_1(self):
        self.assertEqual(5, uniform_in_range(75, 300))
        self.assertEqual(9, uniform_in_range(1, 9))
        self.assertEqual(1, uniform_in_range(999999999999, 999999999999))
        self.assertEqual(8 + 5 + 36, uniform_in_range(5432, 987654321))
        self.assertEqual(0, uniform_in_range(6543, 6543))
        self.assertEqual(1, uniform_in_range(888888888, 987654321))
        self.assertEqual(9, uniform_in_range(1111, 9999))
        self.assertEqual(8, uniform_in_range(1112, 9999))
        self.assertEqual(1, uniform_in_range(1, 1))
        self.assertEqual(2, uniform_in_range(1, 2))

    def test_next_ge_3(self):
        self.assertEqual(333333333333, next_uniform_ge(319454609043))
        self.assertEqual(333333333333, next_uniform_ge(333333333329))

    def test_next_ge_2(self):
        self.assertEqual(1, next_uniform_ge(1))
        self.assertEqual(2, next_uniform_ge(2))
        self.assertEqual(9, next_uniform_ge(9))
        self.assertEqual(11, next_uniform_ge(11))
        self.assertEqual(99, next_uniform_ge(90))
        self.assertEqual(99, next_uniform_ge(98))
        self.assertEqual(99, next_uniform_ge(99))
        self.assertEqual(111, next_uniform_ge(100))
        self.assertEqual(222, next_uniform_ge(123))
        self.assertEqual(999, next_uniform_ge(899))
        self.assertEqual(999, next_uniform_ge(889))
        self.assertEqual(888, next_uniform_ge(887))

    def test_next_ge_1(self):
        self.assertEqual(11, next_uniform_ge(10))

    def test_next_le_2(self):
        self.assertEqual(7777, next_uniform_le(8698))

    def test_next_le_1(self):
        self.assertEqual(1, next_uniform_le(1))
        self.assertEqual(2, next_uniform_le(2))
        self.assertEqual(9, next_uniform_le(9))
        self.assertEqual(9, next_uniform_le(10))
        self.assertEqual(11, next_uniform_le(11))
        self.assertEqual(99, next_uniform_le(110))
        self.assertEqual(99, next_uniform_le(100))
        self.assertEqual(111, next_uniform_le(123))
        self.assertEqual(111, next_uniform_le(221))
        self.assertEqual(222, next_uniform_le(222))
        self.assertEqual(999, next_uniform_le(1000))
        self.assertEqual(999, next_uniform_le(1110))
        self.assertEqual(1111, next_uniform_le(1111))
        self.assertEqual(1111, next_uniform_le(1112))
        self.assertEqual(111, next_uniform_le(111))
        self.assertEqual(222, next_uniform_le(222))

        
