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

def create_hash_dict(files_list):
    hash_dict = {}
    for fpath in files_list:
        h = calc_hash(fpath)
        if h in hash_dict:
            hash_dict[h].append(fpath)
        else:
            hash_dict[h] = [fpath]
    return hash_dict

def ask(question, valid_answers, error_message):
    print(question)
    ans = input().strip()
    while not ans in valid_answers:
        print(error_message)
        print(question)
        ans = input()
    return ans

def create_file_tree(start_path, file_format):
    file_tree = {}
    for root, dirs, files in os.walk(start_path, topdown=False):
       for fname in files:
            fpath = os.path.join(root, fname)
            if fname.endswith(file_format):
                size = os.path.getsize(fpath)
                hash = calc_hash(fpath)
                if size not in file_tree:
                    file_tree[size] = {}
                if hash not in file_tree[size]:
                    file_tree[size][hash] = [fpath]
                else:
                    file_tree[size][hash].append(fpath)
    return file_tree

def list_duplicates(file_tree, sorting_option):
    duplicates_list = []
    i = 1
    for size in sorted(file_tree.keys(), reverse=(sorting_option=='1')):
        hash_dict = file_tree[size]
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
                        duplicates_list.append(fpath)
                        i += 1
    return duplicates_list

def check_deletion_list(deletion_list, m):
    if len(deletion_list) == 0:
        return False
    for s in deletion_list:
        if not s.isdigit():
            return False
    deletion_list = [int(d) for d in deletion_list]
    if min(deletion_list) <= 0 or max(deletion_list) > m:
        return False
    return True

def delete_files(duplicates_list):
    m = len(duplicates_list)
    print('Enter file numbers to delete:')
    deletion_list = input().split()
    while not check_deletion_list(deletion_list, m):
        print('Wrong format')
        print('Enter file numbers to delete:')
        deletion_list = input().split()
    freed_space = 0
    for d in deletion_list:
        fpath = duplicates_dict[int(d) - 1]
        freed_space += os.path.getsize(fpath)
        os.remove(fpath)
    print(f'Total freed up space: {freed_space} bytes')


args = sys.argv
if len(args) <= 1:
    print('Directory is not specified')
else:
    path = args[1]
    print('Enter file format:')
    file_format = input().strip()
    file_tree = create_file_tree(path, file_format)
    question = 'Size sorting options:\n1. Descending\n2. Ascending'
    sorting_option = ask(question, ['1', '2'], 'Wrong option')

    for size in sorted(file_tree.keys(), reverse=(sorting_option=='1')):
        print(size, ' bytes')
        for hash in file_tree[size]:
            for fpath in file_tree[size][hash]:
                print(fpath)

    exit = False
    duplicates_dict = None

    while not exit:
        check = ask('Check for duplicates?', ['yes', 'no'], 'Wrong option')
        if check == 'yes':
            duplicates_dict = list_duplicates(file_tree, sorting_option)
            break
        elif check == 'no':
            exit = True
    
    while not exit:
        delete = ask('Delete files?', ['yes', 'no'], 'Wrong option')
        if delete == 'yes':
            delete_files(duplicates_dict)
            break
        elif delete == 'no':
            exit = True




