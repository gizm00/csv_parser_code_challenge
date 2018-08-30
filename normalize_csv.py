
# read in csv file on stdin, write out csv file on stdout
# input: UTF-8
# output: UTF-8
import sys
from csv import reader, writer
from pytz import timezone
from datetime import datetime, timedelta

# assume the order of the columns is fixed, so we can assume the first column
# has timestamp, the second address, etc
# also assume that the first line is the header

def parse_timestamp(timestamp_in):
    """
    convert timestamp_in to US/Eastern time and ISO-8601 format
    returns: parsed timestamp string or None if a date cannot be converted because of a unicode issue.
    returned timestamp will reflect daylight savings
    param: timestamp_in: string timestamp of m/dd/yy hh:mm:ss pm/am format representing
    a date in US/Pacific timezone.
    """
    if u'\ufffd' in timestamp_in:
        return None
    if timestamp_in == '':
        return ''

    try:
        timestamp_dt_notz = datetime.strptime(timestamp_in, '%m/%d/%y %I:%M:%S %p')
    except:
        return None

    timestamp_dt = timezone('US/Pacific').localize(timestamp_dt_notz)
    timestamp_td_eastern = timestamp_dt.astimezone(timezone('US/Eastern'))
    return timestamp_td_eastern.isoformat(' ')

def parse_duration(duration_in):
    """
    convert duration_in to floating point seconds format
    returns: string representing converted duration_in or none if unicode replacement
    character is present
    param: duration_in: string time druation in HH:MM:SS.MS format
    """
    if u'\ufffd' in duration_in :
        return None
    if duration_in == '' :
        return ''

    return duration_in
    # check to see if there is a python function to convert to fp seconds
    # a millisecond is a floating point second... hm..
    # time_split = duration_in.split('.')
    # fps = int(time_split[1])/1000
    # return time_split[0] + str(fps)

def parse_zipcode(zipcode_in):
    """
    convert zipcode_in to 5 digit zip
    returns: string zipcode 0 padded to create 5 digit zip or none if unicode
    replacement character is found
    """
    if len(zipcode_in) == 5:
        return zipcode_in
    else:
        zero_pad = '0' * (5-len(zipcode_in))
        return zero_pad + zipcode_in

def sum_durations(duration_one, duration_two):
    # convert hhhh:mm:ss.ss format to be able to add. note that its a duration, not a datetime
    if (duration_one == None or duration_one == '') and \
    (duration_two == None or duration_two == '') :
        return ''
    if duration_one == None or duration_one == '' :
        return duration_two
    if duration_two == None or duration_two == '' :
        return duration_one

    sum = timedelta()
    durations = [duration_one, duration_two]
    for entry in durations:
        (hour, min, sec) = entry.split(":")
        sum += timedelta(hours=int(hour), minutes=int(min), seconds=float(sec))
    return str(sum)

csv_writer = writer(sys.stdout)
header = None
for line in sys.stdin.buffer:
    line_data = line.decode('utf_8', 'replace')
    if header is None:
        header = line_data
        print(header.strip())
    else:
        fields = list(reader([line_data]))[0]
        if len(fields) == 8:
            timestamp = parse_timestamp(fields[0])
            address = fields[1]
            zip = parse_zipcode(fields[2])
            fullname = fields[3].upper()
            fooduration = parse_duration(fields[4])
            barduration = parse_duration(fields[5])
            totalduration = sum_durations(fooduration,barduration)
            notes = fields[7]
            if (timestamp != None and zip != None and fooduration != None and barduration != None):
                csv_writer.writerow([timestamp, address, zip, fullname, fooduration, barduration, totalduration, notes])
