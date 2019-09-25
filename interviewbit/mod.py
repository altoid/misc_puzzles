#!/usr/bin/env python

def f(x, n, d):
    # find (x ** n) mod d

    result = 1
    t = x
    while n != 0:
        if n & 1:
            result = (result * t) % d

        t = (t * t) % d
        n = n >> 1
    return result

x = 71045970
n = 41535484
d = 64735492

print x, n, d, f(x, n, d)

x = 3
n = 6
d = 5000

print x, n, d, f(x, n, d)

x = 2473659827643985762934875692834765982374658
n = 9237458726493659283745
d = 3475862754

print x, n, d, f(x, n, d)
