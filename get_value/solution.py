#!/usr/bin/env python

import unittest
from pprint import pprint, pformat


class Tests(unittest.TestCase):

    def setUp(self):
        self.doc = {
            'a': {
                'b': {
                    'c': 'hello'
                },
                'd': {
                    'c': 'sup',
                    'e': {
                        'f': 'blah blah blah'
                    }
                }
            }
        }

    def test1(self):
        pprint(self.doc)
        

if __name__ == '__main__':
    unittest.main()
