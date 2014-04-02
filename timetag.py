import datetime
import matplotlib.pyplot as plt
import numpy as np
import sys
import time
from scipy.interpolate import spline

def find_mm(time):
    # This function return maxium and minium index of time list
    min = []
    max = []
    for i in range(1, len(time) - 1):
        #print 'Working i: ', i
        #if time[i] - time[i+1] >= 0.1 and time[i] - time[i-1] > 0.1:
        #    max.append(i)
        #elif time[i] - time[i+1] > 0.1 and time[i] - time[i-1] >= 0.1:
        #    max.append(i)
        #elif time[i] - time[i+1] < -0.1 and time[i] - time[i-1] <= -0.1:
        #    min.append(i)
        #elif time[i] - time[i+1] <= -0.1 and time[i] - time[i-1] < -0.1:
        #    min.append(i)
        if time[i] >= time[i+1] and time[i] > time[i-1]:
            max.append(i)
        elif time[i] > time[i+1] and time[i] >= time[i-1]:
            max.append(i)
        elif time[i] < time[i+1] and time[i] <= time[i-1]:
            min.append(i)
        elif time[i] <= time[i+1] and time[i] < time[i-1]:
            min.append(i)
    return min, max

def peak(time):
    return [time[i] for i in range(1, len(time) - 1) if time[i - 1] < time[i] and time[i + 1] <= time[i]]

def main(time):
    #print peak(time)
    step = 5
    trend = ['-' for i in range(len(time))]
    for i in range(len(time) - 1):
        if time[i] < time[i + 1]:
            trend[i] = '+'
        elif time[i] == time[i + 1]:
            trend[i] = '='
    i = 1
    line = 1

    #for t in trend:
    #    if i == 1:
    #        sys.stdout.write('No.' + str(line) + '\t')
    #        line += 1
    #    sys.stdout.write(str(i - 1) + ':\t' + t + ", ")
    #    if i % 6 == 0 and i < len(time) - 1:
    #        print ''
    #        sys.stdout.write('No.' + str(line) + '\t')
    #        line += 1
    #    i += 1
    #print ''
    #split_list = search(trend)
    #print time
    #min, max = find_mm(time)
    #for t in min:
    #    print "%s, %s ,%s" % (time[t-1], time[t], time[t+1])
    #print split_list

    # Clear previous line
    plt.cla()
    y = time
    # Define x axis
    ax=plt.gca()  
    #ax.set_xticks(np.linspace(0, 144, 24))  
    ax.set_xticks([i for i in range(0, 144, 6)])  
    ax.set_xticklabels(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'))  
    x = [i for i in range(144)] 

    # Smooth curve
    #x_s = np.linspace(0, 144, 24)
    x_s = [i for i in range(0, 144, 6)]
    #print x_s
    y_s = spline(x, y, x_s)
    for i in range(0, len(y_s)):
        if abs(y_s[i]) < 0.1:
            y_s[i] = 0
        else:
            y_s[i] = int(y_s[i])
    print y_s
    min, max = find_mm(y_s)
    print min, max

    # Define x,y axis label
    plt.xlabel(u'Time')
    plt.ylabel(u'Play time')
    # Plot a line
    plt.plot(x_s, y_s, 'g-')
    plt.plot(x_s, y_s, 'gx')
    #print x_s
    #plt.plot(x, y, 'r-')

    #print x_s
    # Plot split line
    for point in max + min:
        #print point
        plt.plot([point * 6, point * 6],[-1, 14], 'b-')
    plt.show()

def search(trend):
    split_list = []
    start_idx = 0
    end_idx = 0
    #set_trace()
    while start_idx < len(trend):
        start_search = False
        first_des = False
        for i in range(start_idx, len(trend)):
            # Decrease when started
            if trend[i] == '+' and not start_search:
                #print '+ and not start_search'
                start_search = True
            elif trend[i] == '+' and first_des:
                #print i
                end_idx = i
                split_list.append([start_idx, end_idx])
                #print [start_idx, end_idx]
                start_idx = i + 1
                break
            if trend[i] == '-' or trend[i] == '=':
                if not start_search:
                    start_idx = i + 1
                    continue
            if trend[i] == '-' and not first_des and start_search:
                # Start search and firt meet -
                #print '- not first_des and start_search'
                first_des = True
                continue
    return split_list

if __name__ == '__main__':
    #time = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 4, 5, 5, 3, 3, 3, 2, 1, 1, 0, 0, 1, 1, 2, 4, 4, 4, 3, 5, 4, 4, 5, 4, 4, 2, 2, 1, 2, 2, 1, 0, 0, 0, 0, 0, 1, 1, 2, 2, 2, 1, 1, 1, 0, 0, 3, 3, 4, 3, 3, 2, 1, 5, 7, 11, 11, 13, 12, 13, 9, 9, 10, 7, 6, 4, 6, 5, 5, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #time = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 1, 1, 1, 1, 1, 2, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 3, 2, 3, 1, 2, 1, 2, 6, 6, 6, 5, 3, 2, 2, 2, 6, 5, 5, 2, 2, 3, 1, 1, 1, 0, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    time = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 3, 4, 5, 3, 3, 4, 4, 5, 3, 4, 5, 5, 4, 5, 5, 4, 3, 4, 3, 4, 4, 3, 3, 3, 2, 1, 2, 3, 3, 3, 4, 5, 4, 4, 5, 5, 6, 4, 5, 4, 4, 2, 2, 2, 3, 2, 3, 4, 3, 3, 3, 3, 2, 2, 2, 4, 6, 6, 7, 10, 9, 8, 7, 12, 13, 11, 11, 13, 11, 8, 7, 7, 4, 3, 2, 2, 2, 1, 0, 0, 0, 0]
    main(time)
