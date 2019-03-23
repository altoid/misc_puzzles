#!/usr/bin/env python

import unittest
import random
from pprint import pprint

DICTIONARY = '/Users/dtomm/Dropbox/personal/EOWL/all.txt'

with open(DICTIONARY) as f:
    dictionary = f.read().split('\n')

def words_matching_prefix(prefix, wordlist):
    return filter(lambda x: x.startswith(prefix), wordlist)

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
        self.chain = ''

    def display(self):
        for i in xrange(self.size):
            for j in xrange(self.size):
                print self.board[i][j],
            print

    def visit(self, r, c, current_matches):
        if not (0 <= r < self.size):
            return

        if not (0 <= c < self.size):
            return

        if self.board[r][c].visited:
            return

        self.board[r][c].visited = True
        self.chain += self.board[r][c].letter
        new_matches = words_matching_prefix(self.chain, current_matches)

        if new_matches:
            # if current chain is a word, print it out
            w = filter(lambda x: len(x) == len(self.chain), new_matches)
            if w:
                print w[0]

            for dr in xrange(-1, 2):
                for dc in xrange(-1, 2):
                    if dc == 0 and dr == 0:
                        continue
    
                    self.visit(r + dr, c + dc, new_matches)

        self.chain = self.chain[:-1]
        self.board[r][c].visited = False

    def traverse_from(self, r, c):
        self.visit(r, c, dictionary)


class MyTest(unittest.TestCase):
    def test_matches(self):
        prefix = 'neo'
        matches = words_matching_prefix(prefix, dictionary)
        pprint(matches)

if __name__ == '__main__':
    b = Board()
    b.display()

    b.traverse_from(0, 0)
