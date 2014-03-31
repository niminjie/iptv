from xlrd import *
import datetime
import sys

def main():
    '''
    Extract colums from *.xls and convert to data type

    Example:
    Input file:
    ------------------------------------------------------------------------
    ID,CONTENT_ID,CLASS_NAME,STARTTIME, ENDTIME,TIMESPAN,RECORD_DATE,USERID
    ------------------------------------------------------------------------

    Output file:
    ------------------------------------------------------------------------
    userid,    starttime,                 endtime
    1,         2011-03-01 14:00:00,       2011-03-04 14:30:00
    ...
    ------------------------------------------------------------------------

    '''
    # Output file
    fo = open(sys.argv[1], 'w')
    #fo.write('userid,starttime,endtime\n')

    # Input file
    book = open_workbook(sys.argv[2])
    sheet = book.sheet_by_index(0)

    # User list to keep uniq user id
    user = []
    idx = 0
    
    # Read data from excel
    for i in range(1, sheet.nrows):
        # Get User id
        user_id = sheet.row_values(i)[7]
        # Filter different user
        if user_id not in user:
            idx += 1
            user.append(user_id)
        # Get start time: year, month, day
        year, month, day = xldate_as_tuple(sheet.row_values(i)[6], 0)[0:3]
        # Get start time: hour, monute, second
        hour, minute = xldate_as_tuple(sheet.row_values(i)[3], 0)[3:5]
        start_time = str(datetime.datetime(year, month, day, hour, minute, 0))

        # Get end time: year, month, day, hour, monute, second
        year, month, day, hour, minute = xldate_as_tuple(sheet.row_values(i)[4], 0)[:5]
        end_time = str(datetime.datetime(year, month, day, hour, minute, 0))

        # Write userid, start time, end time to file
        fo.write('%s,%s,%s\n' % (str(idx), start_time, end_time))
        fo.flush()
    # Finish write file
    fo.close()

if __name__ == '__main__':
   main() 
