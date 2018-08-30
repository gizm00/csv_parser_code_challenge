
# read in csv file on stdin, write out csv file on stdout
# input: UTF-8
# output: UTF-8
import sys
from csv import reader
from pytz import timezone
from datetime import  datetime

# assume the order of the columns is fixed, so we can assume the first column
# has timestamp, the second address, etc
# also assume that the first line is the header

def parse_timestamp(timestamp_in):
    """
    convert timestamp_in to US/Eastern time and ISO-8601 format
    returns: parsed timestamp string or None if a date cannot be converted because of a unicode issue
    param: timestamp_in: string timestamp of m/dd/yy hh:mm:ss pm/am format representing
    a date in US/Pacific timezone
    """
    # seems redundant
    if u'\ufffd' in timestamp_in:
        return None

    try:
        timestamp_dt_notz = datetime.strptime(timestamp_in, '%m/%d/%y %I:%M:%S %p')
    except:
        return None


    # add timezone offset
    timestamp_dt = timezone('US/Pacific').localize(timestamp_dt_notz)
    timestamp_td_eastern = timestamp_dt.astimezone(timezone('US/Eastern'))
    return timestamp_td_eastern.isoformat(' ')



header = None
for line in sys.stdin.buffer:
    line_data = line.decode('utf_8', 'replace')
    if header is None:
        header = line_data
        print(header)
    else:
        fields = list(reader([line_data]))[0]
        timestamp = parse_timestamp(fields[0])
        address = fields[1]
        zip = fields[2]
        fullname = fields[3]
        fooduration = fields[4]
        barduration = fields[5]
        notes = fields[7]
        print("timestamp: ", timestamp)
