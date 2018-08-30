
# read in csv file on stdin, write out csv file on stdout
# input: UTF-8
# output: UTF-8
import sys
import pandas as pd
from csv import reader, writer

lines = []
# assume the order of the columns is fixed, so we can assume the first column
# has timestamp, the second address, etc
# also assume that the first line is the header

header = None
for line in sys.stdin.buffer:
    line_data = line.decode('utf_8', 'replace')
    if header is None:
        header = line_data
        print(header)
    else:
        fields = list(reader([line_data]))[0]
        timestamp = fields[0]
        address = fields[1]
        zip = fields[2]
        fullname = fields[3]
        fooduration = fields[4]
        barduration = fields[5]
        notes = fields[7]
