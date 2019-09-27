#!/usr/bin/env python

# syntax rules

import unittest
import fileinput

def indentation(line):
    if not line:
        return 0

    i = 0
    for c in line:
        if c != ' ':
            break
        i += 1
    return i

def is_valid(lines):
    """

    :param lines:
    :return:  the line number of the first invalid line,
    -1 if all lines valid
    """

    indentation_levels = [0]
    after_block = False
    counter = 1

    for l in lines:
        if not l:
            counter += 1
            continue

        line_indent = indentation(l)
        if after_block:
            if line_indent > indentation_levels[-1]:
                indentation_levels.append(line_indent)
                after_block = False
                counter += 1
                continue
            return counter
        if line_indent == indentation_levels[-1]:
            if l[-1] != ':':
                counter += 1
                continue
            after_block = True
        elif line_indent < indentation_levels[-1]:
            indentation_levels = indentation_levels[:-1]
            if line_indent != indentation_levels[-1]:
                return counter
        counter += 1

    return -1


if __name__ == '__main__':
    fi = fileinput.input()


class MyTest(unittest.TestCase):
    def test_indentation(self):
        self.assertEqual(0, indentation(None))
        self.assertEqual(0, indentation(""))
        self.assertEqual(0, indentation("i like cheese"))
        self.assertEqual(3, indentation("   indented"))
        self.assertEqual(4, indentation("    "))

    def test_valid(self):
        text = """
x = 5
for i in range(1, 10):
    if i == 2:
        print "hard to read"
    else:
          x = 3
          print "stop"
print "done"
"""
        lines = text.split('\n')
        self.assertEqual(-1, is_valid(lines))

    def test_invalid(self):
        text = """
   x = 5
for i in range(1, 10):
    if i == 2:
        print "hard to read"
    else:
          x = 3
          print "stop"
print "done"
"""
        lines = text.split('\n')
        self.assertEqual(0, is_valid(lines))

    def test_noblocks(self):
        text = """
x = 5
print "done"
"""
        lines = text.split('\n')
        self.assertEqual(-1, is_valid(lines))


    def test5(self):
        text = """
if x == 5:
print "done"
"""
        lines = text.split('\n')
        self.assertEqual(3, is_valid(lines))
