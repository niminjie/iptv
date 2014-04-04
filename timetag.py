import datetime
import copy
import logging
import matplotlib.pyplot as plt
import numpy as np
import sys
import time
from scipy.interpolate import spline


class Point():
    def __init__(self, point):
        self.point = point

    def __repr__(self):
        pass

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
        if user_seq[i-1] < user_seq[i] >= user_seq[i+1]:
            extreme.append('max')
        elif user_seq[i-1] <= user_seq[i] > user_seq[i+1]:
            extreme.append('max')
        elif user_seq[i-1] > user_seq[i] <= user_seq[i+1]:
            extreme.append('min')
        elif user_seq[i-1] >= user_seq[i] < user_seq[i+1]:
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

def tags(y, extreme, threshold=0):
    logging.info('Calling tags:')
    # Range of y
    interval = []
    #extreme = trans_extreme(extreme)
    #print extreme
    all_max = find_all_max(y, extreme, threshold)
    logging.debug('All max points: %s' % str(all_max))

    #all_max = find_all_max(extreme)
    for i in all_max:
        left = find_min_left(extreme, i)
        right = find_min_right(extreme, i)
        #print 'Left:', left,'Max:',i,'Right:', right
        logging.info('Left: %s\tMax: %s \tRight:%s \t' % (left, i, right))
        logging.debug('Interval appended %s' % str((left, right)))
        interval.append((left, right))
    if interval[0][0] != 0:
        interval.insert(0, (0,interval[0][0]))
    logging.info('Split final: %s' % interval) 
    return interval

def find_min_left(extreme, idx):
    for i in range(idx, -1, -1):
        if extreme[i] == 'min':
            #logging.info('Find left minium point: %d' % i)
            return i
    logging.info('Find left margin minium: 0')
    return 0

def find_min_right(extreme, idx):
    for i in range(idx, len(extreme)):
        if extreme[i] == 'min':
            #logging.info('Find right minium point: %d' % i)
            return i
    logging.info('Find right margin minium: %d' % (len(extreme) - 1))
    return len(extreme) - 1

def find_all_max(y, extreme, threshold):
    logging.info('Calling find_all_max')
    scope = max(y) - min(y)
    tmp = extreme
    for i in range(len(extreme)):
        if tmp[i] == 'max':
            left = find_min_left(tmp, i)
            right = find_min_right(tmp, i)
            #print 'Left:', left,'Max:',i,'Right:', right
            if y[i] - y[left] < threshold * scope or y[i] - y[right] < threshold * scope:
               logging.info('Removing max point: %s' % i)
               tmp[i] = '-'
    return [i for i in range(len(tmp)) if tmp[i] == 'max']

def format_list(l):
    t = copy.copy(l)
    for idx, item in enumerate(t):
        if idx == 0:
            t[idx] = '[' + str(idx) + ',\t'
        elif idx == len(t) - 1:
            t[idx] = str(idx) + ']'
        elif (idx + 1)% 6 == 0:
            t[idx] = str(idx) + '\n'
        else:
            t[idx] = str(idx) + ',\t'
    return ''.join(t)

def main(seq_user):
    # Create x coordinate
    x = [i for i in range(144)] 
    # Smooth curve
    x_s, y_s = smooth(x, seq_user)
    logging.debug('Smooth x and y coordinate')
    logging.debug('Smooth x: %s' % str(x_s))
    logging.debug('Smooth y: %s' % str(y_s))
    plot(x_s, y_s)
    plot(x, seq_user)
    # Get all extreme point
    extreme_point = find_mm(y_s)
    intervals = tags(y_s, extreme_point, threshold=0)
    plot_split(intervals)
    plt.show()

if __name__ == '__main__':
    # Handle log
    #logging.basicConfig(filename='timetag.log', filemode='w', level=logging.DEBUG, format='%(asctime)s %(message)s')
    logging.basicConfig(filename='timetag.log', filemode='w', level=logging.DEBUG)
    logging.info('Start program')
    logging.info('This message should go to the log file')
    #seq_user = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 4, 5, 5, 3, 3, 3, 2, 1, 1, 0, 0, 1, 1, 2, 4, 4, 4, 3, 5, 4, 4, 5, 4, 4, 2, 2, 1, 2, 2, 1, 0, 0, 0, 0, 0, 1, 1, 2, 2, 2, 1, 1, 1, 0, 0, 3, 3, 4, 3, 3, 2, 1, 5, 7, 11, 11, 13, 12, 13, 9, 9, 10, 7, 6, 4, 6, 5, 5, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #seq_user = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 1, 1, 1, 1, 1, 2, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 3, 2, 3, 1, 2, 1, 2, 6, 6, 6, 5, 3, 2, 2, 2, 6, 5, 5, 2, 2, 3, 1, 1, 1, 0, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    seq_user = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 3, 4, 5, 3, 3, 4, 4, 5, 3, 4, 5, 5, 4, 5, 5, 4, 3, 4, 3, 4, 4, 3, 3, 3, 2, 1, 2, 3, 3, 3, 4, 5, 4, 4, 5, 5, 6, 4, 5, 4, 4, 2, 2, 2, 3, 2, 3, 4, 3, 3, 3, 3, 2, 2, 2, 4, 6, 6, 7, 10, 9, 8, 7, 12, 13, 11, 11, 13, 11, 8, 7, 7, 4, 3, 2, 2, 2, 1, 0, 0, 0, 0]
    #s = map(lambda x: str(x).ljust(3), seq_user)
    #print test_format_list(seq_user)
    logging.debug('Seq_user: \t%s' % format_list(seq_user))
    main(seq_user)
