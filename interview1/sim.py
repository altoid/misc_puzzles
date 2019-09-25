#!/usr/bin/env python

import sys

def sim(s):

    total = 0
    v = [ True ] * len(s)
    for i in xrange(len(s)):
#        print ' ' * i + s[i:]
        for j in xrange(0, len(s) - i):
            if v[j] and s[i] != s[i:][j]:
                v[j] = False

        for k in xrange(len(s) - i, len(s)):
            v[k] = False
#        print v
        total += sum(1 for x in v if x)
    return total

def _sim(s):
#    print ">>>>>>>>>>>>>> %s" % s

    # take no more than CHUNK suffixes at a time to sip memory
    CHUNK = 5000

    l = len(s)

    start = 0
    total = 0
    while True:
        suffixes = []
        end = min(start + CHUNK, len(s))
        mem = 0
        for i in xrange(start, end):
            if s[i] == s[0]:
                suffixes.append(s[i:])
                mem += len(s[i:])
        print "mem needed: %s" % mem

    
    #    print list(s)
        filtered = suffixes
        # throw out all the suffixes that don't start with the ith char
        for i in xrange(len(s)):
            filtered = [x for x in filtered if len(x) > i and x[i] == s[i]]
            d = len(filtered)
            total += d

        if end == len(s):
            break

        start += CHUNK

#    print "<<<<<<<<<<<<<<< %s" % total
    return total

def stringSimilarity(inputs):
    # an array of strings
    answers = []
    for s in inputs:
        answers.append(sim(s))

    return answers

if __name__ == '__main__':
    text = sys.stdin.read()
    lines = text.split('\n')

    ntests = int(lines[0].strip())
    inputs = []
    for i in xrange(ntests):
        inputs.append(lines[i + 1])

    answers = stringSimilarity(inputs)
    for a in answers:
        print a


