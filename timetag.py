import datetime
import matplotlib.pyplot as plt
import numpy as np
import sys
import time
from scipy.interpolate import spline

def find_mm_exact(user_seq):
    '''
    Find minium and maxium index of user_seq list
    ---------------------------------------------------
    Return:  {'min':[0, 6], 'max':1, 'lmin':2, 'rmin':3, 'lmax':4, 'rmax':5}
    min   :  p[i - 1] >  p[i] <  p[i + 1]
    lmin  :  p[i - 1] == p[i] <  p[i + 1]
    rmin  :  p[i - 1] >  p[i] == p[i + 1]
    max   :  p[i - 1] <  p[i] >  p[i + 1]
    lmax  :  p[i - 1] == p[i] >  p[i + 1]
    lmax  :  p[i - 1] <  p[i] ==  p[i + 1]
    '''
    extrem = {}
    for i in range(1, len(user_seq) - 1):
        if user_seq[i] > user_seq[i+1] and user_seq[i] > user_seq[i-1]:
            extrem.setdefault('max', [])
            extrem['max'].append(i)
        elif user_seq[i] == user_seq[i+1] and user_seq[i] > user_seq[i-1]:
            extrem.setdefault('rmax', [])
            extrem['rmax'].append(i)
        elif user_seq[i] > user_seq[i+1] and user_seq[i] == user_seq[i-1]:
            extrem.setdefault('lmax', [])
            extrem['lmax'].append(i)
        elif user_seq[i] < user_seq[i+1] and user_seq[i] < user_seq[i-1]:
            extrem.setdefault('min', [])
            extrem['min'].append(i)
        elif user_seq[i] == user_seq[i+1] and user_seq[i] < user_seq[i-1]:
            extrem.setdefault('lmin', [])
            extrem['lmin'].append(i)
        elif user_seq[i] < user_seq[i+1] and user_seq[i] == user_seq[i-1]:
            extrem.setdefault('rmin', [])
            extrem['rmin'].append(i)
    return extrem

def find_mm(user_seq):
    '''
    Find minium and maxium index of user_seq list
    ---------------------------------------------------
    Return:  {'min':[0, 6], 'max':1, 'lmin':2, 'rmin':3, 'lmax':4, 'rmax':5}
    min   :  p[i - 1] >  p[i] <  p[i + 1]
    max   :  p[i - 1] <  p[i] >  p[i + 1]
    '''
    extrem = {}
    for i in range(1, len(user_seq) - 1):
        if user_seq[i] >= user_seq[i+1] and user_seq[i] > user_seq[i-1]:
            extrem.setdefault('max', [])
            extrem['max'].append(i)
        elif user_seq[i] > user_seq[i+1] and user_seq[i] >= user_seq[i-1]:
            extrem['max'].append(i)
        elif user_seq[i] <= user_seq[i+1] and user_seq[i] < user_seq[i-1]:
            extrem.setdefault('min', [])
            extrem['min'].append(i)
        elif user_seq[i] < user_seq[i+1] and user_seq[i] <= user_seq[i-1]:
            extrem.setdefault('min', [])
            extrem['min'].append(i)
    return extrem

def plot(x, y, clear = False):
    # Clear previous line
    if clear:
        plt.cla()

    # Define x axis
    ax=plt.gca()  
    ax.set_xticks([i for i in range(0, 144, 6)])  
    ax.set_xticklabels(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'))  

    # Define x,y axis label
    plt.xlabel(u'Time')
    plt.ylabel(u'Play time')

    # Plot a line
    plt.plot(x, y, 'g-')
    #plt.plot(x, y, 'ro')


def plot_split_line(extrem):
    for type, points in extrem.items():
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

def tags(x, y, extrem, threshhold=1):
    # All point * 6
    # for key in extrem.keys():
    #     extrem[key] = map(lambda x : x * 6, extrem[key])

    # ['-', 'min', 'max', ...] 
    seq_extrem = trans_extrem(extrem)
    print seq_extrem

    interval = []
    start = 0
    end = 0
    while start < len(seq_extrem):
        started = False
        find_max = False
        for i in range(start, len(seq_extrem)):
            # find min
            if seq_extrem[i] == 'min' and not started and not find_max:
                start = i
                started = True
            # find after max
            if seq_extrem[i] == 'max' and started and not find_max:
                find_max = True 
            # find after min
            if seq_extrem[i] == 'min' and started and find_max:
                end = i
                interval.append((start, end))
                print interval
                start = end + 1
                break
    print interval

def tags2(y, extrem, threshhold=0.1):
    # Range of y
    range = max(y) - min(y)
    interval = []
    seq_extrem = trans_extrem(extrem)
    print seq_extrem
    all_max = find_all_max(seq_extrem)
    print all_max

    for i in all_max:
        left = find_min_left(seq_extrem, i)
        right = find_min_right(seq_extrem, i)
        #print 'Left:', left,'Max:',i,'Right:', right
        if y[i] - y[left] < threshhold * range or y[i] - y[right] < threshhold * range:
           seq_extrem[i] = '-'

    all_max = find_all_max(seq_extrem)
    for i in all_max:
        left = find_min_left(seq_extrem, i)
        right = find_min_right(seq_extrem, i)
        print 'Left:', left,'Max:',i,'Right:', right
        interval.append((left, right))

    if interval[0][0] != 0:
        interval.insert(0, (0,interval[0][0]))

    print interval
    return interval

def find_min_left(extrem, idx):
    for i in range(idx, -1, -1):
        if extrem[i] == 'min':
            return i
    return 0

def find_min_right(extrem, idx):
    for i in range(idx, len(extrem)):
        if extrem[i] == 'min':
            return i
    return len(extrem) - 1

def find_all_max(extrem):
    return [i for i in range(len(extrem)) if extrem[i] == 'max']

def trans_extrem(extrem):
    x = ['-' for i in range(24)]
    for key, item in extrem.items():
        if key == 'max':
            for i in item:
                x[i] = 'max'
        if key == 'min':
            for i in item:
                x[i] = 'min'
    return x

def main(seq_user):
    # Create x coordinate
    x = [i for i in range(144)] 

    # Smooth curve
    x_s, y_s = smooth(x, seq_user)
    plot(x_s, y_s)
    plot(x, seq_user)

    # Get all extrem point
    extrem_point_exact = find_mm_exact(y_s)
    extrem_point = find_mm(y_s)
    intervals = tags2(y_s, extrem_point, threshhold=0.15)

    #print extrem_point_exact
    #print extrem_point
    #plot_split_line(extrem_point)
    plot_split(intervals)

    #print x_s
    #print y_s
    #print extrem_point
    plt.show()

if __name__ == '__main__':
    #seq_user = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 4, 5, 5, 3, 3, 3, 2, 1, 1, 0, 0, 1, 1, 2, 4, 4, 4, 3, 5, 4, 4, 5, 4, 4, 2, 2, 1, 2, 2, 1, 0, 0, 0, 0, 0, 1, 1, 2, 2, 2, 1, 1, 1, 0, 0, 3, 3, 4, 3, 3, 2, 1, 5, 7, 11, 11, 13, 12, 13, 9, 9, 10, 7, 6, 4, 6, 5, 5, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #seq_user = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 1, 1, 1, 1, 1, 2, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 3, 2, 3, 1, 2, 1, 2, 6, 6, 6, 5, 3, 2, 2, 2, 6, 5, 5, 2, 2, 3, 1, 1, 1, 0, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    seq_user = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 3, 4, 5, 3, 3, 4, 4, 5, 3, 4, 5, 5, 4, 5, 5, 4, 3, 4, 3, 4, 4, 3, 3, 3, 2, 1, 2, 3, 3, 3, 4, 5, 4, 4, 5, 5, 6, 4, 5, 4, 4, 2, 2, 2, 3, 2, 3, 4, 3, 3, 3, 3, 2, 2, 2, 4, 6, 6, 7, 10, 9, 8, 7, 12, 13, 11, 11, 13, 11, 8, 7, 7, 4, 3, 2, 2, 2, 1, 0, 0, 0, 0]
    main(seq_user)
