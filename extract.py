from xlrd import *
import datetime
import sys

def main():
    '''
    Extract colums from *.xls and convert to data type

    Example:
    Input file:
    ------------------------------------------------------------------------------
    ID, CONTENT_ID, CLASS_NAME1, STARTTIME, ENDTIME, TIMESPAN, RECORD_DATE, USERID
    ------------------------------------------------------------------------------

    Output file:
    ------------------------------------------------------------------------------
    userid,    starttime,                 endtime,              CLASS_NAME1
    1,         2011-03-01 14:00:00,       2011-03-04 14:30:00,  TV
    ...
    ------------------------------------------------------------------------------
    '''
    # Output file
    fo = open(sys.argv[2], 'w')
    fo_user = open(sys.argv[3], 'w')
    fo_class = open(sys.argv[4], 'w')
    #fo.write('userid,starttime,endtime\n')
    # Input file
    book = open_workbook(sys.argv[1])
    sheet = book.sheet_by_index(0)
    # User list to keep uniq user id
    user = []
    cls = []
    idx_user = 0
    idx_class = 0
    
    # Read data from excel
    for i in range(1, sheet.nrows):
        # Get User id
        user_id = sheet.row_values(i)[7]
        timespan = sheet.row_values(i)[5]
        # Filter different user
        if user_id not in user:
            idx_user += 1
            user.append(user_id)
            fo_user.write('%s,%s\n' % (str(idx_user), user_id))
        class_name = sheet.row_values(i)[2].encode('utf-8')
        if class_name not in cls:
            idx_class += 1
            cls.append(class_name)
            fo_class.write('%s,%s\n' % (str(idx_class), class_name))
        # Get start time: year, month, day
        year, month, day = xldate_as_tuple(sheet.row_values(i)[6], 0)[0:3]
        # Get start time: hour, monute, second
        hour, minute = xldate_as_tuple(sheet.row_values(i)[3], 0)[3:5]
        #year, month, day, hour, minute = xldate_as_tuple(sheet.row_values(i)[3], 0)[:5]
        start_time = str(datetime.datetime(year, month, day, hour, minute, 0))
        # Get end time: year, month, day, hour, monute, second
        year, month, day, hour, minute = xldate_as_tuple(sheet.row_values(i)[4], 0)[:5]
        end_time = str(datetime.datetime(year, month, day, hour, minute, 0))
        # Write userid, start time, end time to file
        fo.write('%s,%s,%s,%s,%s\n' % (str(idx_user), start_time, end_time, str(timespan), str(idx_class)))
        fo.flush()
    # Finish write file
    fo.close()

if __name__ == '__main__':
   main() 
