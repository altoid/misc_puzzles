#!/usr/bin/env python3

"""
read from a file and produce a string consisting of characters
that appear exactly once in the file.  characters are in the order
they appear in the text.
"""

if __name__ == '__main__':
    char_to_count = {}
    char_to_first_location = {}
    char_counter = 0

    with open('quotation.txt') as f:
        for input_line in f:
            for c in input_line:
                if c not in char_to_first_location:
                    char_to_first_location[c] = char_counter
                if c not in char_to_count:
                    char_to_count[c] = 0
                char_to_count[c] += 1
                char_counter += 1

    solo_chars = [k for k, v in char_to_count.items() if v == 1]

    result = ''.join(sorted(solo_chars, key=lambda x: char_to_first_location[x])).strip()
    print(result)
