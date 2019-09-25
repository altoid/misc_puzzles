#!/usr/bin/env python

from __future__ import division
from math import floor

def my_sqrt(n):
    x = 1
    xprime = (x + n / x) / 2

    while abs(x - xprime) > 0.01:
        x = xprime
        xprime = (x + n / x) / 2

    return int(floor(x))

def test(n):
    print n, my_sqrt(n)

test(11)
test(9)
test(13)
test(16)
test(17)

