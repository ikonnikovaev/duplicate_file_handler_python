import os
import sys

def reverse_order():
    sorting = 0
    while not sorting in [1, 2]:
        print('Size sorting options:\n1. Descending\n2. Ascending')
        sorting = int(input())
        if not sorting in [1, 2]:
            print('Wrong option')
    if sorting == 1:
        return True
    return False

def walk_through(path, extension):
    size_dict = {}
    for root, dirs, files in os.walk(path, topdown=False):
       for fname in files:
            fpath = os.path.join(root, fname)
            if extension == '' or extension == os.path.split(fpath)[1]:
                size = os.path.getsize(fpath)
                if size in size_dict:
                    size_dict[size].append(fpath)
                else:
                    size_dict[size] = [fpath]
    return size_dict


args = sys.argv
if len(args) <= 1:
    print('Directory is not specified')
else:
    path = args[1]
    print('Enter file format:')
    extension = input().strip()
    reverse = reverse_order()
    size_dict = walk_through(path, extension)

    for size in sorted(size_dict.keys(), reverse=reverse):
        print(size, ' bytes')
        for fpath in size_dict[size]:
            print(fpath)







