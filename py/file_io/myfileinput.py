# my implementation of the FileInput class

# processing will stop if a file can't be opened for any reason
# this is an iterable

import unittest


class MyFileInput():
    def __init__(self, files):
        self.filenameiter = iter(files)
        self.currentfilename = None
        self.currentfilehandle = None

    def filename(self):
        """
        Return the name of the file currently being read. Before the first line has been read, returns None.

        if the file being read is empty, this will never return the name of that file.  we will skip over it.
        :return:
        """
        pass

    def fileno(self):
        pass

    def lineno(self):
        pass

    def filelineno(self):
        pass

    def isfirstline(self):
        pass

    def isstdin(self):
        pass

    def nextfile(self):
        pass

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

