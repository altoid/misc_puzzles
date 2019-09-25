#!/usr/bin/env python

import sim
import unittest
import random
import pprint

pp = pprint.PrettyPrinter()

class TestSim(unittest.TestCase):

    def test1(self):
        self.assertEqual(21, sim.sim('aaaaaa'))
        self.assertEqual(13, sim.sim('abbababb'))
        self.assertEqual(11, sim.sim('aabbabab'))
        self.assertEqual(11, sim.sim('ababaa'))
        self.assertEqual(3, sim.sim('aa'))

    def test_random(self):
        chars = 'ab'
        s = ''.join([random.choice(chars) for x in xrange(100000)])
        print sim.sim(s)

    def test_x(self):
#        s = 'aaaaaa'
#        s = 'abbababb'
        s = 'ababaa'
#        s = 'aabbabab'
        print sim.sim(s)

if __name__ == '__main__':
    unittest.main()
