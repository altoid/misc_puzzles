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
        self.results = set()

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
                self.results.add(w[0])

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

    def test_display(self):
        ncolumns = 3
        l = list('abcdefghij')
        nrows = len(l) / ncolumns
        leftovers = len(l) % ncolumns
        result = [0] * len(l)

        c = 0
        n = 0
        while c < leftovers:
            i = 0
            while i < nrows + 1:
                result[i * ncolumns + c] = l[n]
                i += 1
                n += 1
            c += 1

        for 
            result[] = l[n]

        print result

if __name__ == '__main__':
    b = Board()
    b.display()

    for r in xrange(Board.size):
        for c in xrange(Board.size):
            b.traverse_from(r, c)

    print 'found %s words!' % len(b.results)

    # display them nicely across 5 columns
    max_word_len = max([len(x) for x in b.results])
    margin = 5
    ncolumns = 5

    nrows = len(b.results) / ncolumns
    leftovers = len(b.results) % ncolumns

    sorted_list = sorted(b.results)

    for r in xrange(nrows):
        for c in xrange(ncolumns):
            print sorted_list[r * ncolumns + c].ljust(max_word_len + margin),
        print
    if leftovers:
        for i in xrange(leftovers):
            print sorted_list[nrows * ncolumns + i].ljust(max_word_len + margin),
        print

        


