from sys import stderr
import csv


def eprint(*args, **kwargs):
    print(*args, file=stderr, **kwargs)


def sort_file_by_column(fin, fout, column_name):
    with open(fin, 'r') as fin:
        csvreader = csv.reader(fin)
        header = next(csvreader)
        column_index = header.index(column_name)

        sorted = sfbc(csvreader, column_index)
        merge_semisorted_tmp_files(fout, column_index)

    while not sorted:
        with open(fout, 'r') as file:
            csvr = csv.reader(file)
            sorted = sfbc(csvr, column_index)
        merge_semisorted_tmp_files(fout, column_index)

    return column_index


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


def list_to_csvstr(row, newline=True):
    nrow = []
    for i in range(len(row)):
        nrow.append('"'+row[i]+'"')
    if newline:
        return ','.join(nrow)+'\r\n'
    else:
        return ','.join(nrow)


# merges two headerless tmp file into one output file
def merge_semisorted_tmp_files(fname, index):
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

# checks line equality with given fiels


def line_equals(string1, string2, index1, index2):
    r1 = next(csv.reader(string1))
    r2 = next(csv.reader(string2))
    try:
        return r1[index1] == r2[index2]
    except:
        return False

# compares lines with respect to given field


def line_cmp(string1, string2, index1, index2):
    r1 = next(csv.reader([string1]))
    r2 = next(csv.reader([string2]))
    try:
        a = r1[index1]
        b = r2[index2]
    except:
        eprint('error in line_cmp')
        exit(1)
    if a < b:
        return -1
    elif a == b:
        return 0
    else:
        return 1

# does final merging (actually this time join)
# on two sorted files


def merge(fname1, fname2, fin1, fin2, fout, column_index1, column_index2, join_mode):
    with open(fname1) as f:
        r = csv.reader(f)
        header1 = next(r)
    with open(fname2) as f:
        r = csv.reader(f)
        header2 = next(r)
    fout = open(fout, 'w')
    f1 = open(fin1, 'r')
    f2 = open(fin2, 'r')

    # only handled cases: left, inner
    # because right is reverse left
    if join_mode == 'right':
        join_mode = 'left'
        f1, f2 = f2, f1
        header1, header2 = header2, header1
        column_index1, column_index2 = column_index2, column_index1

    # print header
    fout.write(list_to_csvstr(header1, newline=False)+",")
    fout.write(list_to_csvstr(header2))
    h2len = len(header2)

    prevpos2 = 0
    prevstate = "not_found"
    prevline1 = ''
    # TODO try except
    line1 = f1.readline()
    line2 = f2.readline()
    while True:
        cmp = line_cmp(line1, line2, column_index1, column_index2)
        if cmp < 0:
            # fout.write('-1\n')
            if prevstate == 'found':
                line1 = f1.readline()
                f2.seek(prevpos2)
                line2 = f2.readline()
                if prevline1 != line1:
                    prevstate = 'not_found'

                continue
            prevstate = 'not_found'
            # fout.write("ppos: "+str(prevpos2)+'->')
            # fout.write(str(prevpos2)+'\n')

            # print(1, line1, end='')
            if join_mode == 'left':
                fout.write(line1[:-1])
                fout.write(','*h2len+'\n')
            line1 = f1.readline()
            if line1 == '':
                break
        elif cmp > 0:
            prevpos2 = f2.tell()
            line2 = f2.readline()
            if line2 == '':
                if join_mode == 'left':
                    # print(line1)
                    fout.write(line1)
                    for line in f1:
                        fout.write(line)
                        # print(line)
                break
        else:
            # fout.write('0\n')
            prevline1 = line1
            prevstate = 'found'
            fout.write(line1[:-1])
            fout.write(",")
            fout.write(line2)
            line2 = f2.readline()
            if line2 == '':
                if join_mode == 'left':
                    # print(line1)
                    # fout.write(line1)
                    for line in f1:
                        fout.write(line)
                break

    fout.close()
    f1.close()
    f2.close()
