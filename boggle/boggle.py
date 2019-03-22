#!/usr/bin/env python

import unittest
import random

DICTIONARY = '/Users/dtomm/Dropbox/personal/EOWL/all.txt'

class Dictionary(object):

    def __init__(self):
        pass

class Board(object):

    alphabet = 'abcdefghijklmnoprstuvwxyz' # omit q
    size = 4

    def __init__(self):
        self.board = []
        for i in xrange(self.size * self.size):
            self.board.append(random.choice(self.alphabet))


if __name__ == '__main__':
    b = Board()
    print b.board
