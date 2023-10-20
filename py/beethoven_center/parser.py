#!/usr/bin/env python

import unittest
import sys

# call number parser


class CallNumber:
    def __init__(self, raw):
        # all fields are strings

        self.raw = raw
        self.subject_letters = ''
        self.subject_number = ''
        self.cutter1_letter = ''
        self.cutter1_number = ''
        self.cutter2_letter = ''
        self.cutter2_number = ''
        self.cutter3_letter = ''
        self.cutter3_number = ''
        self.opus_type = ''  # op, WoO, etc.
        self.opus_number = ''
        self.year = ''  # year but might be followed by a single letter, e.g. 1921a
        self.extra = ''  # used to indicate volume number, copy number, etc.

        self.raw = self.raw.strip()

        i = 0
        while i < len(self.raw) and self.raw[i].isalpha():
            self.subject_letters += self.raw[i]
            i += 1

        while i < len(self.raw) and self.raw[i].isspace():
            i += 1

        while i < len(self.raw) and self.raw[i].isdigit():
            self.subject_number += self.raw[i]
            i += 1

        while i < len(self.raw) and self.raw[i].isspace():
            i += 1

        # subject number should be followed by a '.'

        if i < len(self.raw):
            if self.raw[i] == '.':
                i += 1
            else:
                print("a. choking on character %s [%s]" % (i, self.raw[i]))
                sys.exit()

        while i < len(self.raw) and self.raw[i].isspace():
            i += 1

        if i < len(self.raw) and self.raw[i].isdigit():
            self.subject_number += '.'
            while i < len(self.raw) and self.raw[i].isdigit():
                self.subject_number += self.raw[i]
                i += 1

            while i < len(self.raw) and self.raw[i].isspace():
                i += 1

            if i < len(self.raw):
                if self.raw[i] == '.':
                    i += 1
                else:
                    print("b. choking on character %s [%s]" % (i, self.raw[i]))
                    sys.exit()

            while i < len(self.raw) and self.raw[i].isspace():
                i += 1

        # should be at cutter 1 now
        if i < len(self.raw) and self.raw[i].isalpha():
            self.cutter1_letter = self.raw[i]
            i += 1
            while i < len(self.raw) and self.raw[i].isspace():
                i += 1
            while i < len(self.raw) and self.raw[i].isdigit():
                self.cutter1_number += self.raw[i]
                i += 1
            while i < len(self.raw) and self.raw[i].isspace():
                i += 1

        # cutter 2
        if i < len(self.raw) and self.raw[i].isalpha():
            self.cutter2_letter = self.raw[i]
            i += 1
            while i < len(self.raw) and self.raw[i].isspace():
                i += 1
            while i < len(self.raw) and self.raw[i].isdigit():
                self.cutter2_number += self.raw[i]
                i += 1
            while i < len(self.raw) and self.raw[i].isspace():
                i += 1

        # cutter 3
        if i < len(self.raw) and self.raw[i].isalpha():
            self.cutter3_letter = self.raw[i]
            i += 1
            while i < len(self.raw) and self.raw[i].isspace():
                i += 1
            while i < len(self.raw) and self.raw[i].isdigit():
                self.cutter3_number += self.raw[i]
                i += 1
            while i < len(self.raw) and self.raw[i].isspace():
                i += 1

    def dump(self):
        print("raw:  |%s| ###########################################" % self.raw)
        print("subject_letters:  |%s|" % self.subject_letters)
        print("subject_number:  |%s|" % self.subject_number)
        if self.cutter1_letter:
            print("cutter1:  |%s%s|" % (self.cutter1_letter, self.cutter1_number))
        if self.cutter2_letter:
            print("cutter2:  |%s%s|" % (self.cutter2_letter, self.cutter2_number))
        if self.cutter3_letter:
            print("cutter3:  |%s%s|" % (self.cutter3_letter, self.cutter3_number))


if __name__ == '__main__':
    cn = CallNumber('ML410.B1 A33 S66')
    cn.dump()

    cn = CallNumber('ML410.5 .B1 A33 S66')
    cn.dump()


class CNTest(unittest.TestCase):
    def test_1(self):
        pass

