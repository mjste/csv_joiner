import sys
from os.path import exists
from utils import *

# print(sys.argv)
if (len(sys.argv) not in [4, 5]):
    eprint("Incorrect argument number, correct: 3, 4")
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

# Validity check done

if col1_exists:
    if col2_exists:
        fout1 = "out1"
        fout2 = "out2"
        column_index1 = sort_file_by_column(fname1, fout1, column_name)
        column_index2 = sort_file_by_column(fname2, fout2, column_name)

        merge(fname1, fname2, fout1, fout2,
              "out", column_index1, column_index2, join_mode)
    else:
        pass
else:
    pass
