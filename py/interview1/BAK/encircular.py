#!/usr/bin/env python

import sys
import unittest

def hasBoundingCircle(commands):
    # return true if repeatedly executing the command vector can be done in a bounding circle
    # if you're pointing the same direction at the end as when you started, and you moved, no
    direction = 0
    moved = False
    for c in commands:
        if c == 'R':
            direction += 1
        elif c == 'L':
            direction -= 1
        elif c == 'G':
            moved = True

    if moved and direction == 0:
        return 'NO'
    return 'YES'

def doesCircleExist(commands):
    # input is an array of commands
    result = []
    for v in commands:
        result.append(hasBoundingCircle(v))
    return result

class TestEncircular(unittest.TestCase):
    def test_basic(self):
        self.assertEqual('NO', hasBoundingCircle('G'))
        self.assertEqual('NO', hasBoundingCircle('GRGL'))
        self.assertEqual('YES', hasBoundingCircle('L'))
        self.assertEqual('YES', hasBoundingCircle('R'))
        self.assertEqual('YES', hasBoundingCircle('GRGRGRGR'))
        self.assertEqual('YES', hasBoundingCircle('GRGRGRG'))
        self.assertEqual('YES', hasBoundingCircle('GLGLGLGL'))
        self.assertEqual('YES', hasBoundingCircle('GLGLGLG'))

    def test_array(self):
        commands = [
            'G',
            'GRGL',
            'L',
            'R',
            'GRGRGRGR',
            'GRGRGRG',
            'GLGLGLGL',
            'GLGLGLG',
            ]

        expected = [
            'NO',
            'NO',
            'YES',
            'YES',
            'YES',
            'YES',
            'YES',
            'YES',
            ]

        result = doesCircleExist(commands)
        self.assertEqual(expected, result)

        
if __name__ == '__main__':
    unittest.main()

