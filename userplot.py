import datetime
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import spline

def main():
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
        intervals.append([i * span, (i + 1) * span])
    print intervals

    for t in user:
        # End day > start day
        if t[0].split()[0] < t[1].split()[0]:
            print 'End day > start day'
            start_min = conver_to_minute(t[0])
            end_min = 23 * 60 + 59
            s_idx, e_idx = find_interval_idx(start_min, end_min, intervals)
            #print s_idx, e_idx
            sum_point(s_idx, e_idx, y)

            start_min = 0
            end_min = conver_to_minute(t[1])
            s_idx, e_idx = find_interval_idx(start_min, end_min, intervals)
            #print s_idx, e_idx
            sum_point(s_idx, e_idx, y)
        else:
            start_min = conver_to_minute(t[0])
            end_min = conver_to_minute(t[1])
            s_idx, e_idx = find_interval_idx(start_min, end_min, intervals)
            sum_point(s_idx, e_idx, y)
    #i = 0    
    #for p in y:
    #    if i % 6 == 0:
    #        print ''
    #    sys.stdout.write(str(p) + ' ')
    #    i += 1
    plt.cla()
    ax=plt.gca()  
    ax.set_xticks(np.linspace(0,144,24))  
    ax.set_xticklabels( ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'))  
    x = [i for i in range(60 / span * 24)] 
    x_s = np.linspace(min(x),max(x),30)
    y_s = spline(x, y, x_s)
    plt.xlabel(u'x')
    plt.ylabel(u'y')
    #plt.plot(x, y)
    #plt.plot(x, np.polyval(y,x), 'r-')
    plt.plot(x_s, y_s, 'r-')
    #plt.show()


def find_interval_idx(start_min, end_min, intervals):
    s_idx = 0
    while(start_min >= intervals[s_idx][1]):
        s_idx += 1
    e_idx = s_idx
    while(end_min > intervals[e_idx][0] and e_idx < len(intervals) - 1):
        e_idx += 1
    return s_idx, e_idx

def sum_point(s_idx, e_idx, y):
    for i in range(s_idx, e_idx):
        y[i] += 1

def conver_to_minute(time):
    hour = int(time.split(' ')[1].split(':')[0])
    minutes = int(time.split(' ')[1].split(':')[1])
    #print hour, minutes
    return hour * 60 + minutes

def test():
    # Read user1
    user_info = {}
    # {'1':[]}
    for line in open('train.csv'):
        #if line.split(',')[0].strip() == '2' or line.split(',')[0].strip() == '1' :
        user_id, start_time, end_time, time_span = line.split(',')
        user_info.setdefault(user_id,[])
        user_info[user_id].append([start_time, end_time, time_span.strip()])
    
    for user_id, info in user_info.items():
        #print user_id
        plot(info)
        #plt.savefig('./plot/' + user_id + '.png')
        print 'Finish:',user_id

    # user_info['1'] can get all the infomation
    plot(user_info['1'])
    plot(user_info['2'])
    plt.savefig('testplot2.png')

if __name__ == '__main__':
   main() 
