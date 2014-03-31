import datetime
import sys

def main():
    '''
    Extract colums and convert date type

    Example:
    userid,starttime,endtime,timespan
    1,2011-03-01 14:00:00,2011-03-04 14:30:00,1800

    '''

    # Test user1
    test()

def plot(user):
    # user : [starttime,endtime,timespan]
    pass


def test():
    # Read user1
    user_info = {}
    # {'1':{1:{'starttime':'2011-03-01', 'endtime':'2011-03-01'...}}, ...}
    # {'1':[]}
    for line in open('train.csv'):
        if line.split(',')[0].strip() == '1':
            user_id, start_time, end_time, time_span = line.split(',')
            user_info.setdefault(user_id,[])
            user_info[user_id].append([start_time, end_time, time_span.strip()])
    # user_info['1'] can get all the infomation

if __name__ == '__main__':
   main() 
