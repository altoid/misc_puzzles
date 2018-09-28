#!/usr/bin/env python

import unittest

class Node(object):
    def __init__(self, label):
        self.label = label
        self.children = []

def serialize_helper(node, acc):
    if not node:
        acc.append(None)
        return

    acc.append(node.label)

    nkids = len(node.children)

    left = None
    if nkids > 0:
        left = node.children[0]

    right = None
    if nkids > 1:
        right = node.children[1]

    # for serializing, we still have to serialize the left and
    # right children, even if there aren't any

    serialize_helper(left, acc)
    serialize_helper(right, acc)

def deserialize_helper(n, stack):
    top = stack[-1]

    while len(top.children) > 1:
        top = stack.pop()
        if not stack:
            # root node is at bottom of stack
            return top

        top = stack[-1]

    node = Node(n) if n else None
    top.children.append(node)

    if node:
        stack.append(node)


def deserialize(ser):
    if not ser:
        return None

    if not ser[0]:
        # bad dog!
        raise Exception("degenerate root node of serialized tree")

    stack = [Node(ser[0])]

    for n in ser[1:]:
        deserialize_helper(n, stack)

    
def serialize(root):
    accumulator = []
    serialize_helper(root, accumulator)
    return accumulator

    
class Tests(unittest.TestCase):
    def test1(self):
        r = Node(1)
        n2 = Node(2)
        n3 = Node(3)
        n4 = Node(4)
        n5 = Node(5)
        n9 = Node(9)

        r.children += [n2, n3]
        n2.children += [None, n9]
        n3.children += [n4, n5]

        ser = serialize(r)
        self.assertEqual([1, 2, None, 9, None, None, 3, 4, None, None, 5, None, None], ser)
