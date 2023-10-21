#!/usr/bin/env python

import unittest
import sys

# call number parser

# TODO:  first cutter number might have more than one letter
# TODO:  opus number follows first cutter
# TODO:  consecutive cutter numbers may have no spaces between them


class CallNumber:
    """
    when  a parse_<whatever> method returns, the pointer will be on the first char after the token.
    """

    def die(self):
        print("choking on char |%s|" % self.raw[self.pointer])
        print("raw:  |%s|" % self.raw)
        print("pointer:  %d" % self.pointer)
        sys.exit()

    def skip_white_space(self):
        while self.pointer < len(self.raw) and (self.raw[self.pointer].isspace() or self.raw[self.pointer] == ','):
            self.pointer += 1

    def parse_subject_number(self):
        self.skip_white_space()
        while self.pointer < len(self.raw) and self.raw[self.pointer].isalpha():
            self.subject_letters += self.raw[self.pointer]
            self.pointer += 1

        while self.pointer < len(self.raw) and not self.raw[self.pointer].isdigit():
            self.die()

        while self.pointer < len(self.raw) and self.raw[self.pointer].isdigit():
            self.subject_number += self.raw[self.pointer]
            self.pointer += 1

        # did we stop at a dot?
        if self.pointer < len(self.raw) and self.raw[self.pointer] == '.':
            dot_position = self.pointer
            self.pointer += 1
            if self.pointer < len(self.raw) and self.raw[self.pointer].isdigit():
                self.subject_number += '.'
                while self.pointer < len(self.raw) and self.raw[self.pointer].isdigit():
                    self.subject_number += self.raw[self.pointer]
                    self.pointer += 1
            else:
                self.pointer = dot_position

    def parse_cutter1(self):
        self.skip_white_space()
        if self.pointer < len(self.raw) and not self.raw[self.pointer].isalpha():
            self.die()

        while self.pointer < len(self.raw) and self.raw[self.pointer].isalpha():
            self.cutter1_letters += self.raw[self.pointer]
            self.pointer += 1

        if self.pointer < len(self.raw) and not self.raw[self.pointer].isdigit():
            self.die()

        while self.pointer < len(self.raw) and self.raw[self.pointer].isdigit():
            self.cutter1_number += self.raw[self.pointer]
            self.pointer += 1

    def parse_cutter2(self):
        self.skip_white_space()
        if self.pointer < len(self.raw) and not self.raw[self.pointer].isalpha():
            self.die()

        self.cutter2_letter += self.raw[self.pointer]
        self.pointer += 1

        if self.pointer < len(self.raw) and not self.raw[self.pointer].isdigit():
            self.die()

        while self.pointer < len(self.raw) and self.raw[self.pointer].isdigit():
            self.cutter2_number += self.raw[self.pointer]
            self.pointer += 1

    def parse_cutter3(self):
        self.skip_white_space()
        if self.pointer < len(self.raw) and not self.raw[self.pointer].isalpha():
            self.die()

        self.cutter3_letter += self.raw[self.pointer]
        self.pointer += 1

        if self.pointer < len(self.raw) and not self.raw[self.pointer].isdigit():
            self.die()

        while self.pointer < len(self.raw) and self.raw[self.pointer].isdigit():
            self.cutter3_number += self.raw[self.pointer]
            self.pointer += 1

    def parse_woo(self):
        self.pointer += len('woo')
        self.skip_white_space()

        if self.pointer < len(self.raw) and not self.raw[self.pointer].isdigit():
            self.die()

        while self.pointer < len(self.raw) and self.raw[self.pointer].isdigit():
            self.opus += self.raw[self.pointer]
            self.pointer += 1

        self.opus_type = 'WoO'

    def parse_opus_number(self):
        self.pointer += len('op.')
        self.skip_white_space()

        if self.pointer < len(self.raw) and not self.raw[self.pointer].isdigit():
            self.die()

        while self.pointer < len(self.raw) and self.raw[self.pointer].isdigit():
            self.opus += self.raw[self.pointer]
            self.pointer += 1

        self.skip_white_space()

        if self.raw[self.pointer:].tolower().startswith('no.'):
            self.pointer += len('no.')

            self.skip_white_space()

            if self.pointer < len(self.raw) and not self.raw[self.pointer].isdigit():
                self.die()

            while self.pointer < len(self.raw) and self.raw[self.pointer].isdigit():
                self.number += self.raw[self.pointer]
                self.pointer += 1

        self.opus_type = 'op.'

    def parse_year(self):
        self.skip_white_space()
        marker = self.pointer

        if self.pointer < len(self.raw) and self.raw[self.pointer].isdigit():
            self.year += self.raw[self.pointer]
            self.pointer += 1
        else:
            self.pointer = marker
            self.year = ''
            return

        if self.pointer < len(self.raw) and self.raw[self.pointer].isdigit():
            self.year += self.raw[self.pointer]
            self.pointer += 1
        else:
            self.pointer = marker
            self.year = ''
            return

        if self.pointer < len(self.raw) and self.raw[self.pointer].isdigit():
            self.year += self.raw[self.pointer]
            self.pointer += 1
        else:
            self.pointer = marker
            self.year = ''
            return

        if self.pointer < len(self.raw) and self.raw[self.pointer].isdigit():
            self.year += self.raw[self.pointer]
            self.pointer += 1
        else:
            self.pointer = marker
            self.year = ''
            return

        # if we have more than 4 digits in a row, consider it extra text.
        if self.pointer < len(self.raw) and self.raw[self.pointer].isdigit():
            self.pointer = marker
            self.year = ''
            return

        while self.pointer < len(self.raw) and not self.raw[self.pointer].isspace():
            self.year += self.raw[self.pointer]
            self.pointer += 1

    def parse_extra(self):
        self.skip_white_space()
        if self.pointer < len(self.raw):
            self.extra = self.raw[self.pointer:]

    def parse_rest(self):
        self.parse_cutter1()
        self.skip_white_space()
        if self.raw[self.pointer:].tolower().startswith('op.'):
            self.parse_opus_number()
        elif self.raw[self.pointer:].tolower().startswith('woo'):
            self.parse_woo()

        self.parse_cutter2()
        if self.cutter2_letter:
            self.parse_cutter3()

        self.parse_year()
        self.parse_extra()

    def parse_call_number(self):
        self.parse_subject_number()

        self.skip_white_space()

        if self.raw[self.pointer] != '.':
            self.die()
        else:
            self.pointer += 1

        self.parse_rest()

    def __init__(self, raw):
        # all fields are strings

        self.raw = raw
        self.pointer = 0
        self.subject_letters = ''
        self.subject_number = ''
        self.cutter1_letters = ''
        self.cutter1_number = ''
        self.cutter2_letter = ''
        self.cutter2_number = ''
        self.cutter3_letter = ''
        self.cutter3_number = ''
        self.opus_type = ''  # op, WoO, etc.
        self.opus = ''
        self.number = ''  # e.g. op. 18 no. 4
        self.year = ''  # year but might be followed by a single letter, e.g. 1921a
        self.extra = ''  # used to indicate volume number, copy number, etc.

        self.raw = self.raw.strip()

        self.parse_call_number()

    def dump(self):
        print("raw:  |%s| ###########################################" % self.raw)
        print("subject_letters:  |%s|" % self.subject_letters)
        print("subject_number:  |%s|" % self.subject_number)
        if self.cutter1_letters:
            print("cutter1:  |%s%s|" % (self.cutter1_letters, self.cutter1_number))
        if self.cutter2_letter:
            print("cutter2:  |%s%s|" % (self.cutter2_letter, self.cutter2_number))
        if self.cutter3_letter:
            print("cutter3:  |%s%s|" % (self.cutter3_letter, self.cutter3_number))
        if self.year:
            print("year:  |%s|" % self.year)


if __name__ == '__main__':
    cn = CallNumber('ML410.B1 A33 S66')
    cn.dump()

    cn = CallNumber('ML410.5 .B1 A33 S66')
    cn.dump()

    cn = CallNumber('ML410.5 .B1 A33 S66')
    cn.dump()

    cn = CallNumber('ML410.B2,1925')
    cn.dump()

    cn = CallNumber('ML410.B2 M53, K32,1925a')
    cn.dump()

class CNTest(unittest.TestCase):
    def test_1(self):
        pass

