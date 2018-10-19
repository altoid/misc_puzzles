#!/usr/bin/env python

import sys
import unittest

def hasBoundingCircle(commands):
    # return true if repeatedly executing the command vector can be done in a bounding circle

    # if we aren't in the same place we started, and we are pointed the same direction as when we started, no

    location = [0, 0]
    directions = ['n', 'e', 's', 'w']
    direction = 0
    moved = False
    for c in commands:
        if c == 'R':
            direction += 1
            direction = direction % 4
        elif c == 'L':
            direction += 3
            direction = direction % 4
        elif c == 'G':
            moved = True
            if directions[direction] == 'e':
                location[0] += 1
            elif directions[direction] == 'n':
                location[1] += 1
            elif directions[direction] == 'w':
                location[0] -= 1
            elif directions[direction] == 's':
                location[1] -= 1

    if location != [0, 0] and direction == 0:
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

