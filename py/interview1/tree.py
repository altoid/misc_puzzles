#!/usr/bin/env python

# for prob 2

import unittest

class BSTreeNode:
    def __init__(self, node_value):
        self.value = node_value
        self.left = self.right = None

def _insert_node_into_binarysearchtree(node, data):
    if node == None:
        node = BSTreeNode(data)
    else:
        if (data <= node.value):
            node.left = _insert_node_into_binarysearchtree(node.left, data);
        else:
            node.right = _insert_node_into_binarysearchtree(node.right, data);
    return node

def isPresent(root, val):
    if root is None:
        return 0

    if val == root.value:
        return 1

    if val < root.value:
        return isPresent(root.left, val)

    return isPresent(root.right, val)

class TestTree(unittest.TestCase):
    def test1(self):
        tree = _insert_node_into_binarysearchtree(None, 8)
        tree = _insert_node_into_binarysearchtree(tree, 20)
        tree = _insert_node_into_binarysearchtree(tree, 25)
        tree = _insert_node_into_binarysearchtree(tree, 40)
        tree = _insert_node_into_binarysearchtree(tree, 30)
        tree = _insert_node_into_binarysearchtree(tree, 10)
        tree = _insert_node_into_binarysearchtree(tree, 12)

        self.assertEqual(1, isPresent(tree, 30))
        self.assertEqual(0, isPresent(None, 30))
        self.assertEqual(0, isPresent(tree, 22))

    def test2(self):
        tree = _insert_node_into_binarysearchtree(None, 8)
        tree = _insert_node_into_binarysearchtree(tree, 8)
        tree = _insert_node_into_binarysearchtree(tree, 8)
        tree = _insert_node_into_binarysearchtree(tree, 8)
        tree = _insert_node_into_binarysearchtree(tree, 8)
        tree = _insert_node_into_binarysearchtree(tree, 8)
        tree = _insert_node_into_binarysearchtree(tree, 8)

        self.assertEqual(1, isPresent(tree, 8))
        self.assertEqual(0, isPresent(tree, 7))
        
if __name__ == '__main__':
    unittest.main()



