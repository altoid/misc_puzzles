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

    # other tests:
    #
    # list(fi) and tuple(fi) should work


if __name__ == '__main__':
    unittest.main()
