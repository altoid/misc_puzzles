import unittest
from myfileinput import MyFileInput


class MFITest(unittest.TestCase):
    def test_instantiation_1(self):
        o = MyFileInput()

    def test_instantiation_2(self):
        # with one file
        o = MyFileInput(['testfiles/sometext'])
        self.assertIsNone(o.filename())

    def test_iteration_1(self):
        mfi = MyFileInput(['testfiles/sometext'])
        for line in mfi:
            print line

    def test_iteration_2(self):
        mfi = MyFileInput(['testfiles/sometext', 'testfiles/empty', 'testfiles/sonnet_cxxviii'])
        for line in mfi:
            print line.rstrip()

    def test_iteration_3(self):
        mfi = MyFileInput(['testfiles/sometext', 'testfiles/empty', 'testfiles/sonnet_cxxviii'])
        for line in mfi:
            print line.rstrip()

    def test_filename_1(self):
        mfi = MyFileInput(['testfiles/sonnet_cxxviii', 'testfiles/empty', 'testfiles/sometext'])

        line = mfi.readline()
        self.assertEqual('testfiles/sonnet_cxxviii', mfi.filename())
        mfi.nextfile()
        self.assertEqual('testfiles/sonnet_cxxviii', mfi.filename())
        line = mfi.readline()
        self.assertEqual('testfiles/sometext', mfi.filename())
        mfi.nextfile()
        mfi.nextfile()
        self.assertEqual('testfiles/sometext', mfi.filename())

    def test_readline(self):
        mfi = MyFileInput(['testfiles/sometext', 'testfiles/empty', 'testfiles/sonnet_cxxviii'])
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

    # other tests:
    #
    # list(fi) and tuple(fi) should work


if __name__ == '__main__':
    unittest.main()
