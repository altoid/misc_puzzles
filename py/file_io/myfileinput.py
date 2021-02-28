# my implementation of the FileInput class

# processing will stop if a file can't be opened for any reason
# this is an iterable

import unittest


class MyFileInput():
    def __init__(self, files=[]):
        self.filenameiter = iter(files)
        self.currentfilename = None
        self.currentfilehandle = None

    def filename(self):
        """
        Return the name of the file currently being read. Before the first line has been read, returns None.

        if the file being read is empty, this will never return the name of that file.  we will skip over it.
        :return:
        """
        return self.currentfilename

    def readline(self):
        try:
            return self.next()
        except StopIteration:
            return ''

    def fileno(self):
        pass

    def lineno(self):
        """
        returns the number of lines that have been read, not the total lines in all files up to here.  for example,
        if we read the first line of a file with 100 lines, and lineno returns 1, then call nextfile(), lineno()
        will return 2.
        :return:
        """
        pass

    def filelineno(self):
        pass

    def isfirstline(self):
        pass

    def isstdin(self):
        pass

    def nextfile(self):
        if self.currentfilehandle:
            self.currentfilehandle.close()
            self.currentfilehandle = None

    def close(self):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        # has to raise StopIteration when there are no more items
        if self.currentfilehandle is None:
            self.currentfilename = self.filenameiter.next()
            self.currentfilehandle = open(self.currentfilename, 'r')

        line = self.currentfilehandle.readline()
        while not line:
            self.currentfilehandle.close()
            self.currentfilename = self.filenameiter.next()
            self.currentfilehandle = open(self.currentfilename, 'r')
            line = self.currentfilehandle.readline()

        return line

    def next(self):
        return self.__next__()

