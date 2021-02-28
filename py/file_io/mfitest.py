import unittest
from myfileinput import MyFileInput


class MFITest(unittest.TestCase):
    def test_instantiation_1(self):
        o = MyFileInput()

    def test_instantiation_2(self):
        # with one file
        o = MyFileInput(['testfiles/one_liner'])
        self.assertIsNone(o.filename())

    def test_iteration_1(self):
        mfi = MyFileInput(['testfiles/one_liner'])
        for line in mfi:
            print line

    def test_iteration_2(self):
        mfi = MyFileInput(['testfiles/one_liner', 'testfiles/empty', 'testfiles/sonnet_cxxviii'])
        for line in mfi:
            print line.rstrip()

    def test_iteration_3(self):
        mfi = MyFileInput(['testfiles/one_liner', 'testfiles/empty', 'testfiles/sonnet_cxxviii'])
        for line in mfi:
            print line.rstrip()

    def test_filename_1(self):
        mfi = MyFileInput(['testfiles/sonnet_cxxviii', 'testfiles/empty', 'testfiles/one_liner'])

        line = mfi.readline()
        self.assertEqual('testfiles/sonnet_cxxviii', mfi.filename())
        mfi.nextfile()
        self.assertEqual('testfiles/sonnet_cxxviii', mfi.filename())
        line = mfi.readline()
        self.assertEqual('testfiles/one_liner', mfi.filename())
        mfi.nextfile()
        mfi.nextfile()
        self.assertEqual('testfiles/one_liner', mfi.filename())

    def test_readline(self):
        mfi = MyFileInput(['testfiles/one_liner', 'testfiles/empty', 'testfiles/sonnet_cxxviii'])
        line = mfi.readline().strip()
        self.assertEqual('i like cheese', line)
        mfi.nextfile()
        line = mfi.readline().strip()
        self.assertEqual('''How oft, when thou, my music, music play'st,''', line)
        mfi.nextfile()
        line = mfi.readline()
        self.assertIs('', line)
        line = mfi.readline()
        self.assertEqual('', line)

    def test_isfirstline(self):
        mfi = MyFileInput(['testfiles/one_liner', 'testfiles/empty', 'testfiles/sonnet_cxxviii', 'testfiles/sonnet_cxxviii'])
        self.assertFalse(mfi.isfirstline())

        # first line of one_liner
        mfi.readline()
        self.assertTrue(mfi.isfirstline())

        # first line of sonnet
        mfi.readline()
        self.assertTrue(mfi.isfirstline())

        # second line of sonnet
        mfi.readline()
        self.assertFalse(mfi.isfirstline())

        mfi.nextfile()

        # first  line of sonnet again
        mfi.readline()
        self.assertTrue(mfi.isfirstline())

    # other tests:
    #
    # list(fi) and tuple(fi) should work


if __name__ == '__main__':
    unittest.main()
