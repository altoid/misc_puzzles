#!/usr/bin/env python

from functools import reduce

def enc_helper(acc, value):
    if acc[-1][0] == value:
        acc[-1][1] += 1
    else:
        acc.append([value, 1])

    return acc

def encode(s):
    if not s:
        return []

    acc = [[s[0], 1]]
    result = reduce(enc_helper, s[1:], acc)

    return result

def decode(enc):
    return ''.join(list(map(lambda x: x[0] * x[1], enc)))
    
if __name__ == '__main__':
    encode_me = '88888!))*&&%%%%%%%%%%%'
    result = encode(encode_me)

    print(result)

    result = decode_2(result)

    print(result)
    
