# starting with my solution to leetcode # 900, run-length iterator.  turn it into a real iterable / iterator.

class RLEIterator(object):
    def __init__(self, encoding):
        self.encoding = encoding
        self.current_run = 0
        self.position_in_current_run = 0  # positions start from 1
        self.still_mo = bool(self.encoding)

    def point_to_next_run(self):
        """
        set the pointer to the beginning of the next nontrivial run.  sets still_mo to False if doing so runs off
        the end of the encoding.  returns the number of places the pointer was moved, or -1 if we couldn't move it.
        """
        advance = self.encoding[self.current_run] - self.position_in_current_run + 1
        self.current_run += 2
        while self.current_run < len(self.encoding) and self.encoding[self.current_run] == 0:
            self.current_run += 2

        if self.current_run >= len(self.encoding):
            self.still_mo = False
            return -1

        self.position_in_current_run = 1

        return advance

    def next(self, n):

        # cases:
        #
        # 1.  incrementing the pointer keeps us in the current run
        # 2.  or puts us into a new run
        # 2a. possibly skipping 1 or more whole runs along the way
        # 3.  incrementing the pointer runs us off the end of the whole encoding
        #     and we have to return -1 for this and future next() invocations.

        # degenerate cases:
        if not self.still_mo:
            return -1

        # case 1:
        if self.position_in_current_run + n <= self.encoding[self.current_run]:
            self.position_in_current_run += n
            return self.encoding[self.current_run + 1]

        # case 2:

        # advance the pointer to the beginning of the next run.
        advance = self.point_to_next_run()
        if advance < 0:
            return -1

        n -= advance

        while self.still_mo and n - self.encoding[self.current_run] > 0:
            n -= self.encoding[self.current_run]
            self.current_run += 2
            if self.current_run >= len(self.encoding):
                self.still_mo = False

        if not self.still_mo:
            return -1

        self.position_in_current_run += n
        return self.encoding[self.current_run + 1]
