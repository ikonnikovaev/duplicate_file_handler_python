import hashlib
import os
import sys

def calc_hash(fpath):
    BUF_SIZE = 65536
    md5 = hashlib.md5()
    with open(fpath, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
    h = md5.hexdigest()
    return h

def ask_if_desc_order():
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

def find_duplicates(size_dict):
    i = 1
    for size in sorted(size_dict.keys(), reverse=desc):
        hash_dict = {}
        for fpath in size_dict[size]:
            h = calc_hash(fpath)
            if h in hash_dict:
                hash_dict[h].append(fpath)
            else:
                hash_dict[h] = [fpath]
        no_duplicates = True
        for h in hash_dict:
            if len(hash_dict[h]) >= 2:
                no_duplicates = False
        if no_duplicates:
            pass
        else:
            print(size, ' bytes')
            for h in hash_dict:
                if len(hash_dict[h]) >= 2:
                    print(f'Hash: {h}')
                    for fpath in hash_dict[h]:
                        print(f'{i}. {fpath}')
                        i += 1



args = sys.argv
if len(args) <= 1:
    print('Directory is not specified')
else:
    path = args[1]
    print('Enter file format:')
    extension = input().strip()
    desc = ask_if_desc_order()
    size_dict = walk_through(path, extension)

    for size in sorted(size_dict.keys(), reverse=desc):
        print(size, ' bytes')
        for fpath in size_dict[size]:
            print(fpath)

    while True:
        print('Check for duplicates?')
        check = input().strip()
        if check not in ['yes', 'no']:
            continue
        if check == 'yes':
            find_duplicates(size_dict)
            break
        elif check == 'no':
            break









