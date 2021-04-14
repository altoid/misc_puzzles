#!/usr/bin/env python

# a binary tree but not a binary search tree; we don't maintain BST order.  keeps track of the next place to insert
# a value such that the height is a minimum.  basically we insert in breadth-first order.
#
# we'll do this with an integer.  initialized to 1; this means empty tree.  when we add a node we increment it.
# the bit patten tells us which way to traverse.  0 left, 1 right.  msb always set.

import math


class Node(object):
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class MinHeight(object):
    def __init__(self):
        self.root = None
        self.bitmap = 1

    def insert(self, v):
        n = Node(v)

        if self.bitmap == 1:
            # tree is empty
            self.root = n
            self.bitmap += 1
            return

        ptr = self.root
        # find the largest power of 2 smaller than the bitmap
        log = int(math.log(self.bitmap, 2.0))
        p2 = 1 << log

        # skootch over 1
        p2 >>= 1

        while p2 > 1:
            if p2 & self.bitmap:
                ptr = ptr.right
            else:
                ptr = ptr.left
            p2 >>= 1

        if p2 & self.bitmap:
            ptr.right = n
        else:
            ptr.left = n

        self.bitmap += 1

    def display_helper(self, n, indent):
        print '    ' * indent,
        if not n:
            print 'NULL'
            return

        print n.data
        self.display_helper(n.left, indent + 1)
        self.display_helper(n.right, indent + 1)

    def display(self):
        self.display_helper(self.root, 0)


if __name__ == '__main__':
    t = MinHeight()
    for i in xrange(1, 9):
        t.insert(i)

    t.display()

