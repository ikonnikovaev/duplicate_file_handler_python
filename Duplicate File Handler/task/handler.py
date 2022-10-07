import os
import sys

args = sys.argv
if len(args) <= 1:
    print('Directory is not specified')
else:
    path = args[1]
    os.chdir(path)
    for root, dirs, files in os.walk('.', topdown=False):
       for name in files:
          print(os.path.join(root, name))



