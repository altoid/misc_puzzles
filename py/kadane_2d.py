#!/usr/bin/env python

import unittest
import random
from pprint import pprint


def max_subarray(arr):
    # just give the max sum without determining indices.  in case of a tie, earlier subarray wins.
    assert len(arr) > 0

    max_ending_here = max_so_far = arr[0]
    for a in arr[1:]:
        max_ending_here = max(a, max_ending_here + a)
        max_so_far = max(max_ending_here, max_so_far)

    return max_so_far


def max_subarray_indices(arr):
    assert len(arr) > 0

    max_ending_here = max_so_far = arr[0]
    l = r = 0
    maxl = maxr = 0

    i = 1
    for a in arr[1:]:
        if a > max_ending_here + a:
            max_ending_here = a
            l = r = i
        else:
            max_ending_here += a
            r = i

        if max_ending_here > max_so_far:
            max_so_far = max_ending_here
            maxl = l
            maxr = r

        i += 1

    return maxl, maxr + 1


def add_rows(r1, r2):
    assert len(r1) == len(r2)
    assert len(r1) > 0

    return [r1[x] + r2[x] for x in range(len(r1))]


def max_matrix_sum(matrix):
    """
    return the largest submatrix sum in <matrix>
    """

    # maps tuple (i, j) to the sums of rows [i..j] (i <= j)
    row_range_sums = {}

    for i in range(len(matrix)):
        total = matrix[i]
        row_range_sums[(i, i + 1)] = total
        for j in range(i + 1, len(matrix)):
            total = add_rows(total, matrix[j])
            row_range_sums[(i, j + 1)] = total

    pprint(row_range_sums)

    max_row_range = (0, 1)
    max_row = row_range_sums[max_row_range]
    max_indices = max_subarray_indices(max_row)
    max_sum = sum(max_row[max_indices[0]:max_indices[1]])

    for k, v in row_range_sums.items():
        indices = max_subarray_indices(v)
        this_sum = sum(v[indices[0]:indices[1]])
        if this_sum > max_sum:
            max_sum = this_sum
            max_indices = indices
            max_row_range = k

    pprint(max_indices)
    pprint(max_row_range)

    return max_sum


class MyTest(unittest.TestCase):
    def test_subarray_1(self):
        arr = [-5, -1, -9, -3, -7, -6]
        self.assertEqual(-1, max_subarray(arr))

    def test_subarray_2(self):
        arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.assertEqual(45, max_subarray(arr))

    def test_subarray_3(self):
        arr = [1]
        self.assertEqual(1, max_subarray(arr))

    def test_subarray_4(self):
        arr = [10, 4, 1, 1, 3, -10, 8, 0, 1, 1, -9, 3, -10, -10, -5]
        self.assertEqual(19, max_subarray(arr))

    def test_indices_1(self):
        arr = [-5, -1, -9, -3, -7, -6]
        expected_max = -1
        expected_range = 1, 2

        max_sum = max_subarray(arr)
        l, r = max_subarray_indices(arr)
        self.assertEqual(expected_max, max_sum)
        self.assertEqual(expected_range, (l, r))
        self.assertEqual(expected_max, sum(arr[l:r]))

    def test_indices_2(self):
        arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        expected_max = 45
        expected_range = 0, 9

        max_sum = max_subarray(arr)
        l, r = max_subarray_indices(arr)
        self.assertEqual(expected_max, max_sum)
        self.assertEqual(expected_range, (l, r))
        self.assertEqual(expected_max, sum(arr[l:r]))

    def test_indices_3(self):
        arr = [1]
        expected_max = 1
        expected_range = 0, 1

        max_sum = max_subarray(arr)
        l, r = max_subarray_indices(arr)
        self.assertEqual(expected_max, max_sum)
        self.assertEqual(expected_range, (l, r))
        self.assertEqual(expected_max, sum(arr[l:r]))

    def test_indices_4(self):
        arr = [10, 4, 1, 1, 3, -10, 8, 0, 1, 1, -9, 3, -10, -10, -5]
        expected_max = 19
        expected_range = 0, 5

        max_sum = max_subarray(arr)
        l, r = max_subarray_indices(arr)
        self.assertEqual(expected_max, max_sum)
        self.assertEqual(expected_range, (l, r))
        self.assertEqual(expected_max, sum(arr[l:r]))

    def test_indices_5(self):
        arr = [0, 0, 0, 0, 5, 0, 0, 0]
        expected_max = 5
        expected_range = 0, 5

        max_sum = max_subarray(arr)
        l, r = max_subarray_indices(arr)
        self.assertEqual(expected_max, max_sum)
        self.assertEqual(expected_range, (l, r))
        self.assertEqual(expected_max, sum(arr[l:r]))

    def test_indices_6(self):
        arr = [5, 0, 0, 0]
        expected_max = 5
        expected_range = 0, 1

        max_sum = max_subarray(arr)
        l, r = max_subarray_indices(arr)
        self.assertEqual(expected_max, max_sum)
        self.assertEqual(expected_range, (l, r))
        self.assertEqual(expected_max, sum(arr[l:r]))

    def test_add_rows_1(self):
        r1 = [1, 2, -1, -4, -20]
        r2 = [-8, -3, 4, 2, 1]

        expecting = [-7, -1, 3, -2, -19]
        self.assertEqual(expecting, add_rows(r1, r2))

    def test_submatrix_1(self):
        matrix = [
            [1, 2, -1, -4, -20],
            [-8, -3, 4, 2, 1],
            [3, 8, 10, 1, 3],
            [-4, -1, 1, 7, -6]
        ]

        expecting = sum([-3, 4, 2, 8, 10, 1, -1, 1, 7])
        self.assertEqual(expecting, max_matrix_sum(matrix))

    def test_submatrix_2(self):
        matrix = [[1]]
        expecting = 1

        self.assertEqual(expecting, max_matrix_sum(matrix))
