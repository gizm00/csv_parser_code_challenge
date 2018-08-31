normalize_csv.py  
This script reads csv content from stdin, transforms that content, and prints the
resulting csv back to stdout.  
The script assumes the content on stdin will follow the format of sample.csv.  
In the case of unicode decoding issues in timestamp, zipcode, fooduration,
barduration, name, or address the row will be dropped and an error message printed
to stderr

To run:  
using python 3.6, install packages from requirements.txt  

usage:  
$ python normalize_csv.py < sample.csv
