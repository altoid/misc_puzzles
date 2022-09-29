#!/usr/bin/env python

def generate(k, arr, level):
    global nswaps
    if k == 1:
        # print('....' * level, end=' ')
        print(arr)
        pass
    else:
        for i in range(k):
            # print('----' * level, end=' ')
            # print(arr)
            generate(k - 1, arr, level + 1)
            if i < k - 1:
                if k % 2 == 0:
                    arr[i], arr[k - 1] = arr[k - 1], arr[i]
                else:
                    arr[0], arr[k - 1] = arr[k - 1], arr[0]
                nswaps += 1

        # print('====' * level, end=' ')
        # print(arr)


if __name__ == '__main__':
    nswaps = 0
    arr = [1, 2, 3]
    generate(len(arr), arr, 0)
    print("nswaps = %s" % nswaps)