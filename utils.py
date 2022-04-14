import re
from sys import stderr
import csv
import tempfile


def eprint(*args, **kwargs):
    print(*args, file=stderr, **kwargs)


# def record_line_to_list(record):
#     pattern = r"(\"([\x20\x21\x23-\x2b\x2d-\x7e\x2c\x0d\x0a]|(\"\"))*\")|([\x20\x21\x23-\x2b\x2d-\x7e])*"
#     record_list = re.findall(pattern, record)
#     record_list = [record_list[i][0]
#                    for i in range(len(record_list)) if i % 2 == 0]
#     print(record_list)


# def check_if_column_exist(fname, column):
#     pattern = r"(\"([\x20\x21\x23-\x2b\x2d-\x7e\x2c\x0d\x0a]|(\"\"))*\")|([\x20\x21\x23-\x2b\x2d-\x7e])*"

#     with open(fname, 'r') as file:
#         headers1 = re.findall(pattern, file.readline())
#         headers1 = [headers1[i][0]
#                     for i in range(len(headers1)) if headers1[i][0] != '']
#         headers = []
#         for header in headers1:
#             if header[0] == '"' and header[-1] == '"':
#                 headers.append(header[1:len(header)-1])
#             else:
#                 headers.append(header)
#         if column not in headers:
#             eprint("Error: column", column, "does not exist in file", fname)
#             return False
#     return True


def sort_file_by_column(fname, column_name):
    fin = open(fname, 'r')
    ftmp1 = open("tmp1", "w")
    ftmp2 = open("tmp2", "w")

    csvreader = csv.reader(fin)
    prev_row = next(csvreader)
    print("header: ", prev_row)
    for row in csvreader:

        pass


def merge_sorted_files(fname1, fname2, column_name, join_mode):
    pass
