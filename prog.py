import sys
from os.path import exists
from utils import *

# print(sys.argv)
if (len(sys.argv) not in [4, 5]):
    eprint("Incorrect argument number")
    exit(0)


fname1 = sys.argv[1]
fname2 = sys.argv[2]
column_name = sys.argv[3]
if len(sys.argv) == 4:
    join_mode = "inner"
else:
    join_mode = sys.argv[4]


# check validity of arguments
try:
    a = open(fname1, 'r')
    a.close()
except:
    eprint(fname1, ": file can't be opened")
    exit(1)

try:
    a = open(fname2, 'r')
    a.close()
except:
    eprint(fname2, ": file cant't be opened")
    exit(1)

if join_mode not in ["inner", 'left', 'right']:
    eprint(join_mode, ": bad mode. Try one of 'inner', 'left', 'right'")
    exit(1)

# check if column exists in files
with open(fname1, 'r') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    if column_name in header:
        col1_exists = True

with open(fname2, 'r') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    if column_name in header:
        col2_exists = True

# col1_exists = check_if_column_exist(fname1, column_name)
# col2_exists = check_if_column_exist(fname2, column_name)

if col1_exists:
    if col2_exists:
        # obie istnieją
        sort_file_by_column(fname1, column_name)
        print()
        sort_file_by_column(fname2, column_name)
        merge_sorted_files(fname1, fname2, column_name, join_mode)
    else:
        pass
else:
    pass
    # obie nie istnieją

    # Validity check done

    # posortuj plik 1
    # posortuj plik 2


with open(fname1, 'r') as file:
    csvreader = csv.reader(file)
    csviter = iter(csvreader)
    while True:
        try:
            print(next(csviter))
        except:
            break
