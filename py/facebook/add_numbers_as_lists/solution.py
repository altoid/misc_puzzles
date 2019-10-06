#!/usr/bin/env python

import unittest

def listify(n):
    result = str(n)
    result = result[::-1]
    result = map(int, result)
    return result

def addem(l1, l2):
    result = []

    p1 = 0
    p2 = 0

    carry = 0

    while True:
        sum = 0

        sum += carry

        if p1 < len(l1):
            sum += l1[p1]
            p1 += 1

        if p2 < len(l2):
            sum += l2[p2]
            p2 += 1

        if sum > 9:
            sum %= 10
            carry = 1
        else:
            carry = 0

        result.append(sum)

        if p1 >= len(l1) and p2 >= len(l2):
            break

    if carry > 0:
        result.append(carry)

    return result

 
class MyTest(unittest.TestCase):

    def test_listify(self):
        self.assertEqual([0], listify(0))
        self.assertEqual([3, 2, 1], listify(123))
    
    def test_addem_1(self):
        def test_add(a, b):
            l1 = listify(a)
            l2 = listify(b)
            control = listify(a + b)
            self.assertEqual(control, addem(l1, l2))

        test_add(342, 465)
        test_add(34299, 465)
        test_add(9, 9)
        test_add(9, 99)
        test_add(9999, 99999999)
