#!/usr/bin/env python

import unittest

class Node(object):
    def __init__(self, label):
        self.label = label
        self.children = []

    def __str__(self):
        return str(self.label)

    def __expr__(self):
        return str(self.label)


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


def serialize(root):
    accumulator = []
    if root:
        serialize_helper(root, accumulator)
    return accumulator


def deserialize(ser):
    if not ser:
        return None

    if not ser[0]:
        return None

    stack = [Node(ser[0])]

    for n in ser[1:]:
        top = stack[-1]

        # unwind stack to find the most recently-seen node with fewer than 2 children
        while len(top.children) > 1:
            stack.pop()
            top = stack[-1]
    
        node = Node(n) if n else None
        top.children.append(node)

        if node:
            stack.append(node)

    return stack[0]

    
class Tests(unittest.TestCase):
    def test1(self):
        """
        test everything.  create a tree, serialize it, deserialize it, serialize THAT, and make sure
        both serializations are the same.
        """

        r = Node(1)
        n2 = Node(2)
        n3 = Node(3)
        n4 = Node(4)
        n5 = Node(5)
        n9 = Node(9)

        r.children += [n2, n3]
        n2.children += [None, n9]
        n3.children += [n4, n5]

        ser1 = serialize(r)
        self.assertEqual([1, 2, None, 9, None, None, 3, 4, None, None, 5, None, None], ser1)

        deser = deserialize(ser1)
        ser2 = serialize(deser)

        self.assertEqual(ser1, ser2)

    def test_empty_tree(self):
        r = None
        ser1 = serialize(r)
        deser = deserialize(ser1)
        ser2 = serialize(deser)

        self.assertEqual(ser1, ser2)
        self.assertEqual([], ser1)

    def test_singleton_tree(self):
        r = Node(1)
        ser1 = serialize(r)
        deser = deserialize(ser1)
        ser2 = serialize(deser)

        self.assertEqual(ser1, ser2)
        self.assertEqual([1, None, None], ser1)

    def test_left_child_only(self):
        r = Node(1)
        n2 = Node(2)

        r.children += [n2, None]
        ser1 = serialize(r)
        deser = deserialize(ser1)
        ser2 = serialize(deser)

        self.assertEqual(ser1, ser2)
        self.assertEqual([1, 2, None, None, None], ser1)

    def test_right_child_only(self):
        r = Node(1)
        n3 = Node(3)

        r.children += [None, n3]
        ser1 = serialize(r)
        deser = deserialize(ser1)
        ser2 = serialize(deser)

        self.assertEqual(ser1, ser2)
        self.assertEqual([1, None, 3, None, None], ser1)
