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
        for _ in xrange(0, ccounter):
            unwound.append(matrix[r][c])
            c += cdir
        c -= cdir

        cdir = -cdir

        rcounter -= 1
        r += rdir

        for _ in xrange(0, rcounter):
            unwound.append(matrix[r][c])
            r += rdir
        r -= rdir

        rdir = -rdir

        ccounter -= 1
        c += cdir

        if rcounter == 0 or ccounter == 0:
            break

    print ','.join(unwound)

if __name__ == '__main__':
    text = sys.stdin.read()
    lines = text.split('\n')
    rows, columns = (int(x) for x in lines[0].split(','))
    matrix = []
    for i in range(int(rows)):
        row = lines[i + 1].split(',')
        matrix.append(row)

    spiral(rows, columns, matrix)





