# my implementation of the FileInput class

# processing will stop if a file can't be opened for any reason
# this is an iterable

import sys

_state = None

class MyFileInput():
    def __init__(self, files=[]):
        files_to_read = files
        if not files_to_read:
            if len(sys.argv) > 1:
                files_to_read = sys.argv[1:]
        if not files_to_read:
            files_to_read = ['-']
        self.__filenameiter = iter(files_to_read)
        self.__currentfilename = None
        self.__currentfilehandle = None
        self.__isfirstline = False
        self.__lineno = 0
        self.__filelineno = 0

    def filename(self):
        """
        Return the name of the file currently being read. Before the first line has been read, returns None.

        if the file being read is empty, this will never return the name of that file.  we will skip over it.
        :return:
        """
        if self.__currentfilename == '-':
            return '<stdin>'
        return self.__currentfilename

    def readline(self):
        try:
            return next(self)
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
        return self.__lineno

    def filelineno(self):
        return self.__filelineno

    def isfirstline(self):
        return self.__isfirstline

    def isstdin(self):
        pass

    def nextfile(self):
        if self.__currentfilehandle:
            if self.__currentfilename != '-':
                self.__currentfilehandle.close()
            self.__currentfilehandle = None

    def close(self):
        pass

    def __iter__(self):
        return self

    def __nextfile(self):
        self.__currentfilename = next(self.__filenameiter)
        if self.__currentfilename == '-':
            self.__currentfilehandle = sys.stdin
        else:
            self.__currentfilehandle = open(self.__currentfilename, 'r')

    def __next__(self):
        # has to raise StopIteration when there are no more items
        if self.__isfirstline:
            self.__isfirstline = False

        if self.__currentfilehandle is None:
            self.__nextfile()
            self.__isfirstline = True

        line = self.__currentfilehandle.readline()
        while not line:
            if self.__currentfilename != '-':
                self.__currentfilehandle.close()

            self.__nextfile()

            line = self.__currentfilehandle.readline()
            self.__isfirstline = True
            self.__filelineno = 0

        self.__lineno += 1
        self.__filelineno += 1
        return line

    def next(self):
        return self.__next__()

def input(files=None):
    global _state

    if not _state:
        _state = MyFileInput(files)

    return _state
