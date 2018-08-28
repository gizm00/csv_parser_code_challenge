# read in csv file on stdin, write out csv file on stdout
# input: UTF-8
# output: UTF-8
import sys
import pandas as pd

lines = []
for line in sys.stdin.buffer:
    line_data = line.decode('utf_8', 'replace')
    lines.append(line_data)
        
with open('tmp_out.csv', 'w', encoding='utf_8') as w:
    w.writelines(lines)

df = pd.read_csv('tmp_out.csv', encoding='utf_8')
print(df)

