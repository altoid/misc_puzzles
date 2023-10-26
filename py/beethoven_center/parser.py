#!/usr/bin/env python

import unittest
import sys

# call number parser


class CallNumber:
    """
    when  a parse_<whatever> method returns, the pointer will be on the first char after the token.
    """

    def die(self):
        print("choking on char |%s|" % self.raw[self.pointer])
        print("raw:  |%s|" % self.raw)
        print("pointer:  %d" % self.pointer)
        raise RuntimeError

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
            self.cutter1_number_str += self.raw[self.pointer]
            self.pointer += 1

        if self.cutter1_number_str:
            self.cutter1_number = float('.' + self.cutter1_number_str)

    def parse_cutter2(self):
        self.skip_white_space()
        marker = self.pointer
        if self.pointer < len(self.raw):
            if not self.raw[self.pointer].isalpha():
                return
        else:
            return

        self.cutter2_letter += self.raw[self.pointer]
        self.pointer += 1

        if self.pointer < len(self.raw) and not self.raw[self.pointer].isdigit():
            self.pointer = marker
            self.cutter2_letter = ''

        while self.pointer < len(self.raw) and self.raw[self.pointer].isdigit():
            self.cutter2_number_str += self.raw[self.pointer]
            self.pointer += 1

        if self.cutter2_number_str:
            self.cutter2_number = float('.' + self.cutter2_number_str)

    def parse_cutter3(self):
        self.skip_white_space()
        marker = self.pointer
        if self.pointer < len(self.raw):
            if not self.raw[self.pointer].isalpha():
                return
        else:
            return

        self.cutter3_letter += self.raw[self.pointer]
        self.pointer += 1

        if self.pointer < len(self.raw) and not self.raw[self.pointer].isdigit():
            self.pointer = marker
            self.cutter3_letter = ''

        while self.pointer < len(self.raw) and self.raw[self.pointer].isdigit():
            self.cutter3_number_str += self.raw[self.pointer]
            self.pointer += 1

        if self.cutter3_number_str:
            self.cutter3_number = float('.' + self.cutter3_number_str)

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

        opus_str = ''

        if self.pointer < len(self.raw) and not self.raw[self.pointer].isdigit():
            self.die()

        while self.pointer < len(self.raw) and self.raw[self.pointer].isdigit():
            opus_str += self.raw[self.pointer]
            self.pointer += 1

        if opus_str:
            self.opus = int(opus_str)

        self.skip_white_space()

        if self.raw[self.pointer:].lower().startswith('no.'):
            no_str = ''
            self.pointer += len('no.')

            self.skip_white_space()

            if self.pointer < len(self.raw) and not self.raw[self.pointer].isdigit():
                self.die()

            while self.pointer < len(self.raw) and self.raw[self.pointer].isdigit():
                no_str += self.raw[self.pointer]
                self.pointer += 1

            if no_str:
                self.number = int(no_str)

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
            self.year_tag += self.raw[self.pointer]
            self.pointer += 1

    def parse_extra(self):
        self.skip_white_space()
        if self.pointer < len(self.raw):
            self.extra = self.raw[self.pointer:]

    def parse_rest(self):
        self.parse_cutter1()
        self.skip_white_space()
        if self.raw[self.pointer:].lower().startswith('op.'):
            self.parse_opus_number()
        elif self.raw[self.pointer:].lower().startswith('woo'):
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

    def __eq__(self, other):
        if not isinstance(other, CallNumber):
            return NotImplemented

        if self.subject_letters != other.subject_letters:
            return False
        
        if self.subject_number != other.subject_number:
            return False
        
        if self.cutter1_letters != other.cutter1_letters:
            return False
        
        if self.cutter1_number != other.cutter1_number:
            return False
        
        if self.cutter2_letter != other.cutter2_letter:
            return False
        
        if self.cutter2_number != other.cutter2_number:
            return False
        
        if self.cutter3_letter != other.cutter3_letter:
            return False
        
        if self.cutter3_number != other.cutter3_number:
            return False
        
        if self.opus_type != other.opus_type:
            return False
        
        if self.opus != other.opus:
            return False
        
        if self.number != other.number:
            return False
        
        if self.year != other.year:
            return False
        
        if self.year_tag != other.year_tag:
            return False
        
        if self.extra != other.extra:
            return False
        
        return True
    
    def __lt__(self, other):
        if not isinstance(other, CallNumber):
            return NotImplemented

        if self.subject_letters < other.subject_letters:
            return True

        if self.subject_letters > other.subject_letters:
            return False

        if self.subject_number < other.subject_number:
            return True

        if self.subject_number > other.subject_number:
            return False

        if self.cutter1_letters < other.cutter1_letters:
            return True

        if self.cutter1_letters > other.cutter1_letters:
            return False

        if self.cutter1_number < other.cutter1_number:
            return True

        if self.cutter1_number > other.cutter1_number:
            return False

        if self.opus_type < other.opus_type:
            return True

        if self.opus_type > other.opus_type:
            return False

        if self.opus < other.opus:
            return True

        if self.opus > other.opus:
            return False

        if self.number < other.number:
            return True

        if self.number > other.number:
            return False

        if self.cutter2_letter < other.cutter2_letter:
            return True

        if self.cutter2_letter > other.cutter2_letter:
            return False

        if self.cutter2_number < other.cutter2_number:
            return True

        if self.cutter2_number > other.cutter2_number:
            return False

        if self.cutter3_letter < other.cutter3_letter:
            return True

        if self.cutter3_letter > other.cutter3_letter:
            return False

        if self.cutter3_number < other.cutter3_number:
            return True

        if self.cutter3_number > other.cutter3_number:
            return False

        if self.year < other.year:
            return True

        if self.year > other.year:
            return False

        if self.year_tag < other.year_tag:
            return True

        if self.year_tag > other.year_tag:
            return False

        if self.extra < other.extra:
            return True

        if self.extra > other.extra:
            return False

        # did we make it all the way here?  then the two operands must be equal.
        return False

    def __init__(self, raw):
        # all fields are strings

        self.raw = raw
        self.pointer = 0
        self.subject_letters = ''
        self.subject_number = ''
        self.cutter1_letters = ''
        self.cutter1_number_str = ''
        self.cutter1_number = 0.0  # float representation of number_str
        self.cutter2_letter = ''
        self.cutter2_number_str = ''
        self.cutter2_number = 0.0
        self.cutter3_letter = ''
        self.cutter3_number_str = ''
        self.cutter3_number = 0.0
        self.opus_type = ''  # op, WoO, etc.
        self.opus = 0
        self.number = 0  # e.g. op. 18 no. 4
        self.year = ''
        self.year_tag = ''  # whatever comes after the year, e.g. 'a' in 1921a
        self.extra = ''  # used to indicate volume number, copy number, etc.

        self.raw = self.raw.strip()

        self.parse_call_number()

    def dump(self):
        print("raw:  |%s| ###########################################" % self.raw)
        print("subject_letters:  |%s|" % self.subject_letters)
        print("subject_number:  |%s|" % self.subject_number)
        if self.cutter1_letters:
            print("cutter1:  |%s%s|" % (self.cutter1_letters, self.cutter1_number_str))
        if self.opus and self.number:
            print("opus:  %s %s no. %s" % (self.opus_type, self.opus, self.number))
        elif self.opus:
            print("opus:  %s %s" % (self.opus_type, self.opus))
        if self.cutter2_letter:
            print("cutter2:  |%s%s|" % (self.cutter2_letter, self.cutter2_number_str))
        if self.cutter3_letter:
            print("cutter3:  |%s%s|" % (self.cutter3_letter, self.cutter3_number_str))
        if self.year:
            print("year:  |%s|" % self.year)
        if self.extra:
            print("extra:  |%s|" % self.extra)


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

    cn = CallNumber('ML457 .Ex77 v.1')
    cn.dump()

    cn = CallNumber('ML672.8.V53K8 2003')
    cn.dump()

    cn = CallNumber('ML410.B421 op.60, C58, 1977a')
    cn.dump()

    cn = CallNumber('ML410.B421 op.60 no. 4, C58, 1977a')
    cn.dump()

    cn = CallNumber('ML410.B421 WoO60, C58, 1977a')
    cn.dump()


class CNTestParser(unittest.TestCase):
    """
        state before parsing

        self.assertEqual('', cn1.subject_letters)
        self.assertEqual('', cn1.subject_number)

        self.assertEqual('', cn1.cutter1_letters)
        self.assertEqual('', cn1.cutter1_number_str)
        self.assertEqual(0.0, cn1.cutter1_number)

        self.assertEqual('', cn1.cutter2_letter)
        self.assertEqual('', cn1.cutter2_number_str)
        self.assertEqual(0.0, cn1.cutter2_number)

        self.assertEqual('', cn1.cutter3_letter)
        self.assertEqual('', cn1.cutter3_number_str)
        self.assertEqual(0.0, cn1.cutter3_number)

        self.assertEqual('', cn1.opus_type)
        self.assertEqual(0, cn1.opus)
        self.assertEqual(0, cn1.number)

        self.assertEqual('', cn1.year)
        self.assertEqual('', cn1.year_tag)
        self.assertEqual('', cn1.extra)

    """
    def test_1(self):
        cn1 = CallNumber('A1.B2')

        self.assertEqual('A', cn1.subject_letters)
        self.assertEqual('1', cn1.subject_number)

        self.assertEqual('B', cn1.cutter1_letters)
        self.assertEqual('2', cn1.cutter1_number_str)
        self.assertEqual(0.2, cn1.cutter1_number)

        self.assertEqual('', cn1.cutter2_letter)
        self.assertEqual('', cn1.cutter2_number_str)
        self.assertEqual(0.0, cn1.cutter2_number)

        self.assertEqual('', cn1.cutter3_letter)
        self.assertEqual('', cn1.cutter3_number_str)
        self.assertEqual(0.0, cn1.cutter3_number)

        self.assertEqual('', cn1.opus_type)
        self.assertEqual(0, cn1.opus)
        self.assertEqual(0, cn1.number)

        self.assertEqual('', cn1.year)
        self.assertEqual('', cn1.year_tag)
        self.assertEqual('', cn1.extra)

    def test_2(self):
        cn1 = CallNumber('A1.B2 C3')

        self.assertEqual('A', cn1.subject_letters)
        self.assertEqual('1', cn1.subject_number)

        self.assertEqual('B', cn1.cutter1_letters)
        self.assertEqual('2', cn1.cutter1_number_str)
        self.assertEqual(0.2, cn1.cutter1_number)

        self.assertEqual('C', cn1.cutter2_letter)
        self.assertEqual('3', cn1.cutter2_number_str)
        self.assertEqual(0.3, cn1.cutter2_number)

        self.assertEqual('', cn1.cutter3_letter)
        self.assertEqual('', cn1.cutter3_number_str)
        self.assertEqual(0.0, cn1.cutter3_number)

        self.assertEqual('', cn1.opus_type)
        self.assertEqual(0, cn1.opus)
        self.assertEqual(0, cn1.number)

        self.assertEqual('', cn1.year)
        self.assertEqual('', cn1.year_tag)
        self.assertEqual('', cn1.extra)

    def test_3(self):
        cn1 = CallNumber('A1.B2 C3 D4')

        self.assertEqual('A', cn1.subject_letters)
        self.assertEqual('1', cn1.subject_number)

        self.assertEqual('B', cn1.cutter1_letters)
        self.assertEqual('2', cn1.cutter1_number_str)
        self.assertEqual(0.2, cn1.cutter1_number)

        self.assertEqual('C', cn1.cutter2_letter)
        self.assertEqual('3', cn1.cutter2_number_str)
        self.assertEqual(0.3, cn1.cutter2_number)

        self.assertEqual('D', cn1.cutter3_letter)
        self.assertEqual('4', cn1.cutter3_number_str)
        self.assertEqual(0.4, cn1.cutter3_number)

        self.assertEqual('', cn1.opus_type)
        self.assertEqual(0, cn1.opus)
        self.assertEqual(0, cn1.number)

        self.assertEqual('', cn1.year)
        self.assertEqual('', cn1.year_tag)
        self.assertEqual('', cn1.extra)

    def test_4(self):
        cn1 = CallNumber('A1.B2 C3 D4 1770')

        self.assertEqual('A', cn1.subject_letters)
        self.assertEqual('1', cn1.subject_number)

        self.assertEqual('B', cn1.cutter1_letters)
        self.assertEqual('2', cn1.cutter1_number_str)
        self.assertEqual(0.2, cn1.cutter1_number)

        self.assertEqual('C', cn1.cutter2_letter)
        self.assertEqual('3', cn1.cutter2_number_str)
        self.assertEqual(0.3, cn1.cutter2_number)

        self.assertEqual('D', cn1.cutter3_letter)
        self.assertEqual('4', cn1.cutter3_number_str)
        self.assertEqual(0.4, cn1.cutter3_number)

        self.assertEqual('', cn1.opus_type)
        self.assertEqual(0, cn1.opus)
        self.assertEqual(0, cn1.number)

        self.assertEqual('1770', cn1.year)
        self.assertEqual('', cn1.year_tag)
        self.assertEqual('', cn1.extra)

    def test_5(self):
        cn1 = CallNumber('A1.B2 C3 D4 1770x')

        self.assertEqual('A', cn1.subject_letters)
        self.assertEqual('1', cn1.subject_number)

        self.assertEqual('B', cn1.cutter1_letters)
        self.assertEqual('2', cn1.cutter1_number_str)
        self.assertEqual(0.2, cn1.cutter1_number)

        self.assertEqual('C', cn1.cutter2_letter)
        self.assertEqual('3', cn1.cutter2_number_str)
        self.assertEqual(0.3, cn1.cutter2_number)

        self.assertEqual('D', cn1.cutter3_letter)
        self.assertEqual('4', cn1.cutter3_number_str)
        self.assertEqual(0.4, cn1.cutter3_number)

        self.assertEqual('', cn1.opus_type)
        self.assertEqual(0, cn1.opus)
        self.assertEqual(0, cn1.number)

        self.assertEqual('1770', cn1.year)
        self.assertEqual('x', cn1.year_tag)
        self.assertEqual('', cn1.extra)

    def test_6(self):
        cn1 = CallNumber('A1.B2 C3 D4 1770 v. 2')

        self.assertEqual('A', cn1.subject_letters)
        self.assertEqual('1', cn1.subject_number)

        self.assertEqual('B', cn1.cutter1_letters)
        self.assertEqual('2', cn1.cutter1_number_str)
        self.assertEqual(0.2, cn1.cutter1_number)

        self.assertEqual('C', cn1.cutter2_letter)
        self.assertEqual('3', cn1.cutter2_number_str)
        self.assertEqual(0.3, cn1.cutter2_number)

        self.assertEqual('D', cn1.cutter3_letter)
        self.assertEqual('4', cn1.cutter3_number_str)
        self.assertEqual(0.4, cn1.cutter3_number)

        self.assertEqual('', cn1.opus_type)
        self.assertEqual(0, cn1.opus)
        self.assertEqual(0, cn1.number)

        self.assertEqual('1770', cn1.year)
        self.assertEqual('', cn1.year_tag)
        self.assertEqual('v. 2', cn1.extra)

    def test_no_cutter2(self):
        cn1 = CallNumber('A1.B2 1770')

        self.assertEqual('A', cn1.subject_letters)
        self.assertEqual('1', cn1.subject_number)

        self.assertEqual('B', cn1.cutter1_letters)
        self.assertEqual('2', cn1.cutter1_number_str)
        self.assertEqual(0.2, cn1.cutter1_number)

        self.assertEqual('', cn1.cutter2_letter)
        self.assertEqual('', cn1.cutter2_number_str)
        self.assertEqual(0.0, cn1.cutter2_number)

        self.assertEqual('', cn1.cutter3_letter)
        self.assertEqual('', cn1.cutter3_number_str)
        self.assertEqual(0.0, cn1.cutter3_number)

        self.assertEqual('', cn1.opus_type)
        self.assertEqual(0, cn1.opus)
        self.assertEqual(0, cn1.number)

        self.assertEqual('1770', cn1.year)
        self.assertEqual('', cn1.year_tag)
        self.assertEqual('', cn1.extra)

    def test_just_extra(self):
        cn1 = CallNumber('A1.B2 v. 3')

        self.assertEqual('A', cn1.subject_letters)
        self.assertEqual('1', cn1.subject_number)

        self.assertEqual('B', cn1.cutter1_letters)
        self.assertEqual('2', cn1.cutter1_number_str)
        self.assertEqual(0.2, cn1.cutter1_number)

        self.assertEqual('', cn1.cutter2_letter)
        self.assertEqual('', cn1.cutter2_number_str)
        self.assertEqual(0.0, cn1.cutter2_number)

        self.assertEqual('', cn1.cutter3_letter)
        self.assertEqual('', cn1.cutter3_number_str)
        self.assertEqual(0.0, cn1.cutter3_number)

        self.assertEqual('', cn1.opus_type)
        self.assertEqual(0, cn1.opus)
        self.assertEqual(0, cn1.number)

        self.assertEqual('', cn1.year)
        self.assertEqual('', cn1.year_tag)
        self.assertEqual('v. 3', cn1.extra)

    def test_no_year(self):
        cn1 = CallNumber('A1.B2 C3 D4 v. 3')

        self.assertEqual('A', cn1.subject_letters)
        self.assertEqual('1', cn1.subject_number)

        self.assertEqual('B', cn1.cutter1_letters)
        self.assertEqual('2', cn1.cutter1_number_str)
        self.assertEqual(0.2, cn1.cutter1_number)

        self.assertEqual('C', cn1.cutter2_letter)
        self.assertEqual('3', cn1.cutter2_number_str)
        self.assertEqual(0.3, cn1.cutter2_number)

        self.assertEqual('D', cn1.cutter3_letter)
        self.assertEqual('4', cn1.cutter3_number_str)
        self.assertEqual(0.4, cn1.cutter3_number)

        self.assertEqual('', cn1.opus_type)
        self.assertEqual(0, cn1.opus)
        self.assertEqual(0, cn1.number)

        self.assertEqual('', cn1.year)
        self.assertEqual('', cn1.year_tag)
        self.assertEqual('v. 3', cn1.extra)

    def test_op_1(self):
        cn1 = CallNumber('A1.B2 op. 127')

        self.assertEqual('A', cn1.subject_letters)
        self.assertEqual('1', cn1.subject_number)

        self.assertEqual('B', cn1.cutter1_letters)
        self.assertEqual('2', cn1.cutter1_number_str)
        self.assertEqual(0.2, cn1.cutter1_number)

        self.assertEqual('', cn1.cutter2_letter)
        self.assertEqual('', cn1.cutter2_number_str)
        self.assertEqual(0.0, cn1.cutter2_number)

        self.assertEqual('', cn1.cutter3_letter)
        self.assertEqual('', cn1.cutter3_number_str)
        self.assertEqual(0.0, cn1.cutter3_number)

        self.assertEqual('op.', cn1.opus_type)
        self.assertEqual(127, cn1.opus)
        self.assertEqual(0, cn1.number)

        self.assertEqual('', cn1.year)
        self.assertEqual('', cn1.year_tag)
        self.assertEqual('', cn1.extra)


class CNTestLT(unittest.TestCase):
    def test_1(self):
        cn1 = CallNumber('A1.B2')
        cn2 = CallNumber('B1.B2')
        self.assertTrue(cn1 < cn2)

    def test_2(self):
        cn1 = CallNumber('A1.B2')
        cn2 = CallNumber('A2.B2')
        self.assertTrue(cn1 < cn2)

    def test_3(self):
        cn1 = CallNumber('A1.B2')
        cn2 = CallNumber('B1.B2')
        self.assertTrue(cn1 < cn2)

    def test_4(self):
        cn1 = CallNumber('A1.A2')
        cn2 = CallNumber('A1.B2')
        self.assertTrue(cn1 < cn2)

    def test_5(self):
        cn1 = CallNumber('A1.A2')
        cn2 = CallNumber('A1.A3')
        self.assertTrue(cn1 < cn2)

    def test_6(self):
        cn1 = CallNumber('A1.B2 C1')
        cn2 = CallNumber('A1.B2 D1')
        self.assertTrue(cn1 < cn2)

    def test_7(self):
        cn1 = CallNumber('A1.B2 C1')
        cn2 = CallNumber('B1.B2 C2')
        self.assertTrue(cn1 < cn2)

    def test_8(self):
        cn1 = CallNumber('A1.B2 C1 D1')
        cn2 = CallNumber('A1.B2 C1 E1')
        self.assertTrue(cn1 < cn2)

    def test_9(self):
        cn1 = CallNumber('A1.B2 C1 D1')
        cn2 = CallNumber('B1.B2 C1 D2')
        self.assertTrue(cn1 < cn2)

    def test_10(self):
        cn1 = CallNumber('A1.B2 C1 D1 1770')
        cn2 = CallNumber('B1.B2 C1 D1 1771')
        self.assertTrue(cn1 < cn2)

    def test_11(self):
        cn1 = CallNumber('A1.B2 C1 D1 1770')
        cn2 = CallNumber('B1.B2 C1 D1 1770a')
        self.assertTrue(cn1 < cn2)

    def test_12(self):
        cn1 = CallNumber('A1.B2 C1 D1 1770')
        cn2 = CallNumber('B1.B2 C1 D1 1770 c. 2')
        self.assertTrue(cn1 < cn2)

    def test_13(self):
        cn1 = CallNumber('A1.A2')
        cn2 = CallNumber('A1.A2 op. 127')
        self.assertTrue(cn1 < cn2)

    def test_14(self):
        cn1 = CallNumber('A1.A2 op. 125')
        cn2 = CallNumber('A1.A2 op. 127')
        self.assertTrue(cn1 < cn2)

    def test_15(self):
        cn1 = CallNumber('A1.A2 op. 59 no. 2')
        cn2 = CallNumber('A1.A2 op. 59 no. 3')
        self.assertTrue(cn1 < cn2)


