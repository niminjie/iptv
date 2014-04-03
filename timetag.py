import datetime
import matplotlib.pyplot as plt
import numpy as np
import sys
import time
from scipy.interpolate import spline

def find_mm(user_seq):
    '''
    Find minium and maxium index of user_seq list
    ---------------------------------------------------
    Return:  {'min':[0, 6], 'max':1, 'lmin':2, 'rmin':3, 'lmax':4, 'rmax':5}
    min   :  p[i - 1] >  p[i] <  p[i + 1]
    max   :  p[i - 1] <  p[i] >  p[i + 1]
    '''
    extreme = []
    extreme.append('-')
    for i in range(1, len(user_seq) - 1):
        if user_seq[i] >= user_seq[i+1] and user_seq[i] > user_seq[i-1]:
            extreme.append('max')
        elif user_seq[i] > user_seq[i+1] and user_seq[i] >= user_seq[i-1]:
            extreme.append('max')
        elif user_seq[i] <= user_seq[i+1] and user_seq[i] < user_seq[i-1]:
            extreme.append('min')
        elif user_seq[i] < user_seq[i+1] and user_seq[i] <= user_seq[i-1]:
            extreme.append('min')
        else:
            extreme.append('-')
    extreme.append('-')
    return extreme

def plot(x, y, clear = False):
    # Clear previous line
    if clear:
        plt.cla()
    # Define x axis
    ax=plt.gca()  
    ax.set_xticks([i for i in range(0, 144, 6)])  
    ax.set_xticklabels([str(i) for i in range(24)])
    # Define x,y axis label
    plt.xlabel(u'Time')
    plt.ylabel(u'Play time')
    # Plot a line
    plt.plot(x, y, 'g-')
    #plt.plot(x, y, 'ro')

def plot_split_line(extreme):
    for type, points in extreme.items():
        if type == 'max':
            style = 'b-'
        elif type == 'rmax':
            style = 'b-'
        elif type == 'lmax':
            style = 'b-'
        elif type == 'min':
            style = 'g-'
        elif type == 'rmin':
            style = 'g-'
        elif type == 'lmin':
            style = 'g-'
        for point in points:
            plt.plot([point * 6, point * 6],[-1, 14], style, linewidth=2)

def plot_split(intervals):
    for point in intervals:
        plt.plot([point[0] * 6, point[0] * 6],[-1, 14], 'b-', linewidth=2)
        plt.plot([point[1] * 6, point[1] * 6],[-1, 14], 'b-', linewidth=2)

def smooth(x, y):
    x_s = [i for i in range(0, 144, 6)]
    y_s = spline(x, y, x_s)
    for i in range(0, len(y_s)):
        if abs(y_s[i]) < 0.1:
            y_s[i] = 0
        else:
            y_s[i] = int(y_s[i])
    return x_s, y_s

def tags(x, y, extreme, threshold=1):
    extreme = trans_extreme(extreme)
    print extreme

    interval = []
    start = 0
    end = 0
    while start < len(extreme):
        started = False
        find_max = False
        for i in range(start, len(extreme)):
            # find min
            if extreme[i] == 'min' and not started and not find_max:
                start = i
                started = True
            # find after max
            if extreme[i] == 'max' and started and not find_max:
                find_max = True 
            # find after min
            if extreme[i] == 'min' and started and find_max:
                end = i
                interval.append((start, end))
                print interval
                start = end + 1
                break
    print interval

def tags2(y, extreme, threshold=0):
    # Range of y
    interval = []
    #extreme = trans_extreme(extreme)
    #print extreme
    all_max = find_all_max(y, extreme, threshold)
    print all_max

    #all_max = find_all_max(extreme)
    for i in all_max:
        left = find_min_left(extreme, i)
        right = find_min_right(extreme, i)
        print 'Left:', left,'Max:',i,'Right:', right
        interval.append((left, right))
    if interval[0][0] != 0:
        interval.insert(0, (0,interval[0][0]))
    print interval
    return interval

def find_min_left(extreme, idx):
    for i in range(idx, -1, -1):
        if extreme[i] == 'min':
            return i
    return 0

def find_min_right(extreme, idx):
    for i in range(idx, len(extreme)):
        if extreme[i] == 'min':
            return i
    return len(extreme) - 1

def find_all_max(y, extreme, threshold):
    scope = max(y) - min(y)
    tmp = extreme
    for i in range(len(extreme)):
        if tmp[i] == 'max':
            left = find_min_left(tmp, i)
            right = find_min_right(tmp, i)
            #print 'Left:', left,'Max:',i,'Right:', right
            if y[i] - y[left] < threshold * scope or y[i] - y[right] < threshold * scope:
               tmp[i] = '-'
    return [i for i in range(len(tmp)) if tmp[i] == 'max']

def main(seq_user):
    # Create x coordinate
    x = [i for i in range(144)] 
    # Smooth curve
    x_s, y_s = smooth(x, seq_user)
    plot(x_s, y_s)
    plot(x, seq_user)
    # Get all extreme point
    extreme_point = find_mm(y_s)
    intervals = tags2(y_s, extreme_point, threshold=0)
    plot_split(intervals)
    plt.show()

if __name__ == '__main__':
    #seq_user = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 4, 5, 5, 3, 3, 3, 2, 1, 1, 0, 0, 1, 1, 2, 4, 4, 4, 3, 5, 4, 4, 5, 4, 4, 2, 2, 1, 2, 2, 1, 0, 0, 0, 0, 0, 1, 1, 2, 2, 2, 1, 1, 1, 0, 0, 3, 3, 4, 3, 3, 2, 1, 5, 7, 11, 11, 13, 12, 13, 9, 9, 10, 7, 6, 4, 6, 5, 5, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #seq_user = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 1, 1, 1, 1, 1, 2, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 3, 2, 3, 1, 2, 1, 2, 6, 6, 6, 5, 3, 2, 2, 2, 6, 5, 5, 2, 2, 3, 1, 1, 1, 0, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    seq_user = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 3, 4, 5, 3, 3, 4, 4, 5, 3, 4, 5, 5, 4, 5, 5, 4, 3, 4, 3, 4, 4, 3, 3, 3, 2, 1, 2, 3, 3, 3, 4, 5, 4, 4, 5, 5, 6, 4, 5, 4, 4, 2, 2, 2, 3, 2, 3, 4, 3, 3, 3, 3, 2, 2, 2, 4, 6, 6, 7, 10, 9, 8, 7, 12, 13, 11, 11, 13, 11, 8, 7, 7, 4, 3, 2, 2, 2, 1, 0, 0, 0, 0]
    main(seq_user)
