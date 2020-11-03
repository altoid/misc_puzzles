#!/usr/bin/env python

# determine whether an integer is a palindrome.
#
# cases:
#
# very large number
# 2 digit number
# 3 digit number
# 1 digit number
# negative number

import unittest

def is_palindrome(x):
    # reverse the number and see if it's equal

    x_copy = x
    rev_x = 0

    while x_copy != 0:
        rev_x *= 10
        rev_x += x_copy % 10
        x_copy //= 10

    return rev_x == x

class MyTest(unittest.TestCase):
    def test_simple(self):
        self.assertFalse(is_palindrome(12345))
        
    def test_1_digit(self):
        self.assertTrue(is_palindrome(1))
        self.assertTrue(is_palindrome(0))
        self.assertTrue(is_palindrome(9))
        
    def test_2_digits(self):
        self.assertTrue(is_palindrome(11))
        self.assertTrue(is_palindrome(99))
        self.assertFalse(is_palindrome(42))
        self.assertFalse(is_palindrome(10))

    def test_3_digits(self):
        self.assertTrue(is_palindrome(111))
        self.assertTrue(is_palindrome(121))
        self.assertTrue(is_palindrome(999))

        self.assertFalse(is_palindrome(100))
        self.assertFalse(is_palindrome(198))
        self.assertFalse(is_palindrome(908))

    def test_large(self):
        self.assertTrue(is_palindrome(12345678912345678987654321987654321))
        self.assertFalse(is_palindrome(1234567891234567898765432198765321))
                        
