#!/usr/bin/env python3

import unittest
from pprint import pprint
import random

LETTERS = 5
WORD_LIST = './5_letters.txt'
dictionary = None


def match(guess, solution):
    assert guess
    assert solution
    assert len(guess) == LETTERS
    assert len(solution) == LETTERS

    """
    returns a list of ints.  len(result) == LETTERS.
    each element in the list corresponds to a letter in <guess>.
    if result[i] == 2, letter <i> is correct and in the correct position.
    if result[i] == 1, letter <i> is correct but not in the correct position.
    if result[i] == 0, letter <i> is not correct.
    """

    result = [0] * LETTERS
    visits = [False] * LETTERS

    for i in range(LETTERS):
        for j in range(LETTERS):
            if visits[j]:
                continue
            if guess[i] == solution[j]:
                result[i] = 1
                visits[j] = True
                break

    for i in range(LETTERS):
        if guess[i] == solution[i]:
            result[i] += 1

    return result


def display(matches, guess):
    for i in range(LETTERS):
        if matches[i] == 2:
            print("| *%s* " % guess[i], end='')
        elif matches[i] == 1:
            print("| (%s) " % guess[i], end='')
        else:
            print("|  %s  " % guess[i], end='')
    print("|")


def read_dict():
    global dictionary

    file = open(WORD_LIST)
    contents = file.read()
    file.close()
    dictionary = set(contents.split('\n'))


def select_word():
    global dictionary

    temp_list = list(dictionary)
    return random.choice(temp_list)


def guess_is_legit(guess):
    global dictionary

    return guess in dictionary


if __name__ == '__main__':
    read_dict()
    solution = select_word()

    while True:
        guess = input('--> ')
        guess = guess.strip()
        if guess == 'quit':
            print("quitting...")
            break

        if not guess:
            continue

        if not guess_is_legit(guess):
            print("%s is not a word" % guess)
            continue

        m = match(guess, solution)
        display(m, guess)

        if all(x == 2 for x in m):
            print("you win!")
            break


class WordleTest(unittest.TestCase):
    def test1(self):
        guess = 'abcde'
        solution = 'zyxwa'
        result = match(guess, solution)
        self.assertEqual([1, 0, 0, 0, 0], result)

    def test2(self):
        guess = 'abcde'
        solution = 'azyxw'
        result = match(guess, solution)
        self.assertEqual([2, 0, 0, 0, 0], result)

    def test3(self):
        guess = 'aaawa'
        solution = 'azyxw'
        result = match(guess, solution)
        self.assertEqual([2, 0, 0, 1, 0], result)

    def test4(self):
        guess = 'abcde'
        solution = 'bcdea'
        result = match(guess, solution)
        self.assertEqual([1, 1, 1, 1, 1], result)

    def test5(self):
        guess = 'abcde'
        solution = 'abcde'
        result = match(guess, solution)
        self.assertEqual([2, 2, 2, 2, 2], result)

    def test6(self):
        guess = 'aaaaa'
        solution = 'aaaaa'
        result = match(guess, solution)
        self.assertEqual([2, 2, 2, 2, 2], result)

