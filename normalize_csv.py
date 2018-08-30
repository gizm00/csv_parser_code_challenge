"""
normalize_csv.py
This script reads csv content from stdin, transforms that content, and prints the
resulting csv back to stdout.
The script assumes the content on stdin will follow the format of sample.csv
In the case of unicode decoding issues the in timestamp, zipcode, fooduration,
barduration, name, or address the row will be dropped and an error message printed
to stderr
"""
import sys
from csv import reader, writer
from pytz import timezone
from datetime import datetime, timedelta

def validate_unicode(string_input, field_name):
    """
    if unicode replacement character is found in string_input return False
    otherwise return true
    """
    if u'\ufffd' in string_input:
        print("unicode issue in", field_name, file=sys.stderr)
        return False
    else:
        return True

def parse_timestamp(timestamp_in):
    """
    convert timestamp_in to US/Eastern time and ISO-8601 format
    :param timestamp_in: string timestamp of m/dd/yy hh:mm:ss pm/am format representing
    a date in US/Pacific timezone.
    returns: string timestamp in US/Eastern time and ISO-8601 format or None if a date
    cannot be converted, either because of a malformed date or a unicode issue.
    returned timestamp will reflect daylight savings
    """
    if not validate_unicode(timestamp_in, "Timestamp"):
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

def parse_duration(duration_in, duration_name):
    """
    convert duration_in to floating point seconds format
    :param duration_in: string time duration in HH:MM:SS.MS format
    :param duration_name: string identifier for duration_in
    returns: string representing duration_in in floating point seconds isoformat
    or none if unicode replacement character is present or if the duration is malformed
    """
    if not validate_unicode(duration_in, duration_name):
            return None
    if duration_in == '' :
        return ''

    try:
        (hour, min, sec) = duration_in.split(":")
    except:
        return None

    return timedelta(hours=int(hour), minutes=int(min), seconds=float(sec)).total_seconds()


def parse_zipcode(zipcode_in):
    """
    convert zipcode_in to 5 digit zip
    :param zipcode_in: string representation of a zipcode with 1 to 5 digits
    returns: string zipcode 0 padded to create 5 digit zip or none if unicode
    replacement character is found
    """
    if not validate_unicode(zipcode_in, 'zipcode'):
            return None

    if len(zipcode_in) == 5 or zipcode_in == '':
        return zipcode_in
    else:
        zero_pad = '0' * (5-len(zipcode_in))
        return zero_pad + zipcode_in

def sum_durations(duration_one, duration_two):
    """
    Add the values in duration_one and duration_two. If either value is empty or None
    return the other value as the sum. If both values are None or empty return empty
    :param duration_one, duration_two: string containing decimal number
    returns: string representation of floating point sum or empty
    """
    if (duration_one == None or duration_one == '') and \
    (duration_two == None or duration_two == '') :
        return ''
    if duration_one == None or duration_one == '' :
        return duration_two
    if duration_two == None or duration_two == '' :
        return duration_one

    return str(float(duration_one) + float(duration_two))


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
            zip = parse_zipcode(fields[2])
            fooduration = parse_duration(fields[4], 'fooduration')
            barduration = parse_duration(fields[5], 'barduration')
            totalduration = sum_durations(fooduration,barduration)
            notes = fields[7]
            address = fields[1]
            if validate_unicode(fields[3], "fullname"):
                fullname = fields[3].upper()
            else:
                fullname = None

            if (timestamp != None and zip != None and fooduration != None and barduration != None \
            and validate_unicode(address, "address") and fullname != None):
                csv_writer.writerow([timestamp, address, zip, fullname, fooduration, barduration, totalduration, notes])
