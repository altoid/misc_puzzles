#!/usr/bin/env python

import unittest
import random
from pprint import pprint

DICTIONARY = '/Users/dtomm/Dropbox/personal/EOWL/all.txt'

class Dictionary(object):

    def __init__(self):
        with open(DICTIONARY) as f:
            self.dictionary = f.read().split('\n')


class Cell(object):
    def __init__(self, letter):
        self._letter = letter
        self.visited = False

    @property
    def letter(self):
        return self._letter

    def __str__(self):
        return self.letter

class Board(object):

    alphabet = 'abcdefghijklmnoprstuvwxyz' # omit q
    size = 4

    def __init__(self):
        self.board = []
        for i in xrange(self.size):
            self.board.append([Cell(random.choice(self.alphabet)) for x in xrange(self.size)])
        self.chain = []

    def display(self):
        for i in xrange(self.size):
            for j in xrange(self.size):
                print self.board[i][j],
            print

    def visit(self, r, c):
        if not (0 <= r < self.size):
            return

        if not (0 <= c < self.size):
            return

        if self.board[r][c].visited:
            return

        self.board[r][c].visited = True
        self.chain.append(self.board[r][c].letter)
        print ''.join(self.chain)

        for dr in xrange(-1, 2):
            for dc in xrange(-1, 2):
                if dc == 0 and dr == 0:
                    continue

                self.visit(r + dr, c + dc)

        del self.chain[-1]
        self.board[r][c].visited = False

    def traverse_from(self, r, c):
        self.visit(r, c)


if __name__ == '__main__':
    d = Dictionary()
    print d.dictionary[:11]

    b = Board()
    b.display()

    b.traverse_from(0, 0)
