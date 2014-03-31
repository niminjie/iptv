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
    ''' 
    user : [starttime,endtime,timespan]
    '''
    # Generate y axis
    span = 10
    y = [0 for i in range(60 / span * 24)]

    # [[0,10], [10,20], [20,30],...]
    intervals = []
    for i in range(60 / span * 24):
        intervals.append([i * 10, (i + 1) * 10])

    for t in user:
        start_min = conver_to_minute(t[0])
        end_min = conver_to_minute(t[1])

        s_idx = 0
        while(start_min >= intervals[s_idx][1]):
            s_idx += 1

        e_idx = s_idx
        while(end_min >= intervals[e_idx][0]):
            e_idx += 1

        for i in range(s_idx, e_idx):
            y[i] += 1
    print y


def conver_to_minute(time):
    hour = int(time.split(' ')[1].split(':')[0])
    minutes = int(time.split(' ')[1].split(':')[1])
    #print hour, minutes
    return hour * 60 + minutes


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
    plot(user_info['1'])

if __name__ == '__main__':
   main() 
