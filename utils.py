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

    csvreader = csv.reader(fin)
    header = next(csvreader)
    column_index = header.index(column_name)

    sorted = sfbc(csvreader, column_index)
    merge_semisorted_files("out", column_index)

    i = 0
    while not sorted:
        print(i)
        with open("out", 'r') as file:
            csvr = csv.reader(file)
            sorted = sfbc(csvr, column_index)
        merge_semisorted_files("out", column_index)

# sort file by column without header


def sfbc(csvr: csv.reader, index: int):
    f1 = open("tmp1", 'w')
    f2 = open("tmp2", 'w')
    prev_row = next(csvr)
    f1.write(list_to_csvstr(prev_row))

    sorted = True
    for row in csvr:
        if row[index] < prev_row[index]:
            sorted = False
            f1, f2, = f2, f1
        f1.write(list_to_csvstr(row))
        prev_row = row
    f1.close()
    f2.close()
    return sorted


def list_to_csvstr(row):
    nrow = []
    for i in range(len(row)):
        nrow.append('"'+row[i]+'"')
    return ','.join(nrow)+'\n'


def merge_semisorted_files(fname, index):
    f1 = open("tmp1", 'r')
    f2 = open("tmp2", 'r')
    fout = open(fname, 'w')
    csvr1 = csv.reader(f1)
    csvr2 = csv.reader(f2)

    try:
        row1 = next(csvr1)
    except StopIteration:
        for row in csvr2:
            fout.write(list_to_csvstr(row))
        f1.close()
        f2.close()
        return

    try:
        row2 = next(csvr2)
    except StopIteration:
        fout.write(list_to_csvstr(row1))
        for row in csvr1:
            fout.write(list_to_csvstr(row))
        f1.close()
        f2.close()
        return

    while True:
        print(row1[index], row2[index])
        if row1[index] < row2[index]:
            fout.write(list_to_csvstr(row1))
            try:
                row1 = next(csvr1)
            except StopIteration:
                fout.write(list_to_csvstr(row2))
                for row in csvr2:
                    fout.write(list_to_csvstr(row))
                f1.close()
                f2.close()
                return
        else:
            fout.write(list_to_csvstr(row2))
            try:
                row2 = next(csvr2)
            except StopIteration:
                fout.write(list_to_csvstr(row1))
                for row in csvr1:
                    fout.write(list_to_csvstr(row))
                f1.close()
                f2.close()
                return
