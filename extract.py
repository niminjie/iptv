# codeing:gbk
from xlrd import *
import datetime

def main():
    ''' Extract colums and convert date type
    Example:
    userid,starttime,endtime,timespan
    1,2011-03-01 14:00:00,2011-03-04 14:30:00,1800
    '''
    fo = open('train', 'w')
    fo.write('userid,starttime,endtime,timespan\n')
    book = open_workbook('trainingset1.xlsx')
    #print book.sheet_names()
    sheet = book.sheet_by_index(0)
    #print sheet.nrows, sheet.ncols

    # User list to hash
    user = []
    idx = 0
    for i in range(1, sheet.nrows):
        # Get User id and time span
        user_id = sheet.row_values(i)[0]
        # Different user
        if user_id not in user:
            idx += 1
            user.append(user_id)
        time_span = sheet.row_values(i)[3]
        # Get start time: year, month, day
        year, month, day = xldate_as_tuple(sheet.row_values(i)[4], 0)[0:3]
        # Get start time: hour, monute, second
        hour, minute = xldate_as_tuple(sheet.row_values(i)[1], 0)[3:5]
        start_date = str(datetime.datetime(year, month, day, hour, minute, 0))

        # Get end time: year, month, day, hour, monute, second
        year, month, day, hour, minute = xldate_as_tuple(sheet.row_values(i)[2], 0)[:5]
        end_date = str(datetime.datetime(year, month, day, hour, minute, 0))
        fo.write('%s,%s,%s,%s\n' % (str(idx), start_date, end_date, time_span))
        fo.flush()
    fo.close()

if __name__ == '__main__':
   main() 
