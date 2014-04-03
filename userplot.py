import datetime
import time
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import spline

def plot(user, block=10):
    '''
        1. Split 24h to equal blocks
        2. Determin whether the play time across block intervals
           eg. 00:00 --> 01:00 across [0, 10],[10,20]... [50, 60]
        3. Plot a point if play time across block intervals
    '''
    num_interval = 60 / block * 24
    # Create y coordinate (stand for play time)
    y = [0 for i in range(num_interval)]
    # Create time intervals
    # [[0,10], [10,20], [20,30],...]
    intervals = []
    for i in range(num_interval):
        intervals.append([i * block, (i + 1) * block])

    for t in user:
        # Start time and end time in different day
        start_time = t[0]
        end_time = t[1]
        if start_time.split()[0] < end_time.split()[0]:
            # Split to two time interval
            # Time1
            start_min = conver_to_minute(start_time)
            end_min = 23 * 60 + 59

            # Find intervals index between play time
            s_idx, e_idx = find_interval_idx(start_min, end_min, intervals)
            count_playtime(s_idx, e_idx, y)

            # Time2
            start_min = 0
            end_min = conver_to_minute(end_time)
            s_idx, e_idx = find_interval_idx(start_min, end_min, intervals)
            count_playtime(s_idx, e_idx, y)

        # Start time and end time in one day
        else:
            start_min = conver_to_minute(start_time)
            end_min = conver_to_minute(end_time)
            s_idx, e_idx = find_interval_idx(start_min, end_min, intervals)
            count_playtime(s_idx, e_idx, y)

    # Clear previous line
    plt.cla()

    # Define x axis
    ax=plt.gca()  
    ax.set_xticks(np.linspace(0, num_interval, 24))  
    ax.set_xticklabels([str(i) for i in range(24)])
    x = [i for i in range(num_interval)] 

    # Smooth curve
    x_s = np.linspace(min(x),max(x),30)
    y_s = spline(x, y, x_s)

    # Define x,y axis label
    plt.xlabel(u'Time')
    plt.ylabel(u'Play time')
    # Plot a line
    plt.plot(x_s, y_s, 'r-')

def find_interval_idx(start_min, end_min, intervals):
    s_idx = 0
    while(start_min >= intervals[s_idx][1]):
        s_idx += 1
    e_idx = s_idx
    while(end_min > intervals[e_idx][0] and e_idx < len(intervals) - 1):
        e_idx += 1
    return s_idx, e_idx

def count_playtime(s_idx, e_idx, y):
    for i in range(s_idx, e_idx):
        y[i] += 1

def conver_to_minute(time):
    hour = int(time.split(' ')[1].split(':')[0])
    minutes = int(time.split(' ')[1].split(':')[1])
    #print hour, minutes
    return hour * 60 + minutes

def file_to_dict(file):
    # Dictionary to store user play time
    # {'1':['2011-03-01 13:00:00', '2011-03-01 14:00:00'], ...}
    user_info = {}
    # Read dataset from user input
    for line in open(sys.argv[1]):
        user_id, start_time, end_time, _ = line.split(',')
        user_info.setdefault(user_id, [])
        user_info[user_id].append([start_time, end_time.strip()])
    return user_info

def main():
    user_info = file_to_dict(sys.argv[1])    
    # Plot distribution for every user
    for user_id, playtime in user_info.items():
        plot(playtime, block=10)
        plt.savefig('./plot/' + user_id + '.png')
        print user_id + ' plot saved!'

if __name__ == '__main__':
   start_time = time.clock()
   main() 
   end_time = time.clock()
   print 'Finished in: %ds' % (end_time - start_time)
