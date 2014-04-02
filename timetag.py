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


def plot(x, y):
    # Clear previous line
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
    plt.plot(x, y, 'gx')


def plot_split(extrem):
    for type, points in extrem.items():
        for point in points:
            plt.plot([point * 6, point * 6],[-1, 14], 'b-')

def smooth(x, y):
    x_s = [i for i in range(0, 144, 6)]
    y_s = spline(x, y, x_s)
    for i in range(0, len(y_s)):
        if abs(y_s[i]) < 0.1:
            y_s[i] = 0
        else:
            y_s[i] = int(y_s[i])
    return x_s, y_s

def main(seq_user):
    # Create x coordinate
    x = [i for i in range(144)] 

    # Smooth curve
    x_s, y_s = smooth(x, seq_user)
    plot(x_s, y_s)

    # Get all extrem point
    extrem_point = find_mm(y_s)
    plot_split(extrem_point)

    #print x_s
    #print y_s
    #print extrem_point

    plt.show()

if __name__ == '__main__':
    #seq_user = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 4, 5, 5, 3, 3, 3, 2, 1, 1, 0, 0, 1, 1, 2, 4, 4, 4, 3, 5, 4, 4, 5, 4, 4, 2, 2, 1, 2, 2, 1, 0, 0, 0, 0, 0, 1, 1, 2, 2, 2, 1, 1, 1, 0, 0, 3, 3, 4, 3, 3, 2, 1, 5, 7, 11, 11, 13, 12, 13, 9, 9, 10, 7, 6, 4, 6, 5, 5, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #seq_user = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 1, 1, 1, 1, 1, 2, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 3, 2, 3, 1, 2, 1, 2, 6, 6, 6, 5, 3, 2, 2, 2, 6, 5, 5, 2, 2, 3, 1, 1, 1, 0, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    seq_user = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 3, 4, 5, 3, 3, 4, 4, 5, 3, 4, 5, 5, 4, 5, 5, 4, 3, 4, 3, 4, 4, 3, 3, 3, 2, 1, 2, 3, 3, 3, 4, 5, 4, 4, 5, 5, 6, 4, 5, 4, 4, 2, 2, 2, 3, 2, 3, 4, 3, 3, 3, 3, 2, 2, 2, 4, 6, 6, 7, 10, 9, 8, 7, 12, 13, 11, 11, 13, 11, 8, 7, 7, 4, 3, 2, 2, 2, 1, 0, 0, 0, 0]
    main(seq_user)
