#!/usr/bin/env python

import sys

def spiral(rows, columns, matrix):
    ccounter = columns
    rcounter = rows

    cdir = 1
    rdir = 1
    r, c = 0, 0
    unwound = []
    while True:
        print ccounter
        for i in xrange(0, ccounter):
            print "[%s %s]" % (r, c)
            unwound.append(matrix[r][c])
            c += cdir
        c -= cdir

        rcounter -= 1
        cdir = -cdir
        print rcounter

        r += rdir
        for i in xrange(0, rcounter):
            print "[%s %s]" % (r, c)
            unwound.append(matrix[r][c])
            r += rdir
        r -= rdir

        ccounter -= 1
        c += cdir

        rdir = -rdir

        if rcounter == 0 or ccounter == 0:
            break

    print unwound

if __name__ == '__main__':
    text = sys.stdin.read()
    lines = text.split('\n')
    rows, columns = (int(x) for x in lines[0].split(','))
    matrix = []
    for i in range(int(rows)):
        row = lines[i + 1].split(',')
        matrix.append(row)

    spiral(rows, columns, matrix)





