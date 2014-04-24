from DataSet import DataSet
from scipy.interpolate import spline
import MakeDict
import datetime
import matplotlib.pyplot as plt
import numpy as np
import sys
import time

DEBUG = False

class TimeSpliter():
    def __init__(self, data):
        self.data = data

    def split_all_user(self, block=10):
        # Every users' time point (length = 144)
        # {'1':[0,0,1,2,... ,3]}
        user_time = {}
        for user_id, playtime in self.data.items():
            y = self.split_time_range(playtime, block=10)
            user_time[user_id] = y
        return user_time

    def split_time_range(self, user, block=10):
        '''
        Input User info
        block    default=10  10minutes per point
        Return   [0,1,2,2,...,5]
        '''
        num_interval = 60 / block * 24

        # Create y coordinate (stand for play time)
        y = [0 for i in range(num_interval)]

        # Create time intervals
        # [[0,10], [10,20], [20,30],...,[1430,1440]]
        intervals = []
        for i in range(num_interval):
            intervals.append([i * block, (i + 1) * block])

        for t in user:
            start_time = t['start']
            end_time = t['end']
            # Start time and end time in different day
            if start_time.split()[0] < end_time.split()[0]:
                # Split to two time interval
                # Time1
                start_min = self._convert_to_minute(start_time)
                end_min = 23 * 60 + 59

                # Find intervals index between play time
                s_idx, e_idx = self._find_interval_idx(start_min, end_min, intervals)
                self._count_playtime(s_idx, e_idx, y)

                # Time2
                start_min = 0
                end_min = self._convert_to_minute(end_time)
                s_idx, e_idx = self._find_interval_idx(start_min, end_min, intervals)
                self._count_playtime(s_idx, e_idx, y)

            # Start time and end time in one day
            else:
                start_min = self._convert_to_minute(start_time)
                end_min = self._convert_to_minute(end_time)
                s_idx, e_idx = self._find_interval_idx(start_min, end_min, intervals)
                self._count_playtime(s_idx, e_idx, y)
        return y

    def _find_interval_idx(self, start_min, end_min, intervals):
        s_idx = 0
        while(start_min >= intervals[s_idx][1]):
            s_idx += 1
        e_idx = s_idx
        while(end_min > intervals[e_idx][0] and e_idx < len(intervals) - 1):
            e_idx += 1
        return s_idx, e_idx

    def _count_playtime(self, s_idx, e_idx, y):
        for i in range(s_idx, e_idx):
            y[i] += 1

    def _convert_to_minute(self, time):
        hour = int(time.split(' ')[1].split(':')[0])
        minutes = int(time.split(' ')[1].split(':')[1])
        #print hour, minutes
        return hour * 60 + minutes

    def _find_mm(self, user_seq):
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

    def _smooth(self, x, y):
        x_s = [i for i in range(0, 144, 6)]
        y_s = spline(x, y, x_s)
        for i in range(0, len(y_s)):
            if abs(y_s[i]) < 0.1:
                y_s[i] = 0
            else:
                y_s[i] = int(y_s[i])
        return x_s, y_s

    def _tags(self, y, extreme, threshold=0):
        # Range of y
        interval = []
        all_max = self._find_all_max(y, extreme, threshold)

        for i in all_max:
            if DEBUG:
                print >> log, '*' * 100
                print >> log, 'Processing max point: idx: %d' % i
                print >> log, '*' * 100
            left = self._find_min_left(extreme, i)
            right = self._find_min_right(extreme, i)
            if len(interval) > 0 and interval[-1][0] == left and interval[-1][1] == right:
                if DEBUG:
                    print >> log, 'left = left, right = right'
                continue
            if len(interval) > 0 and interval[-1][1] != left:
                interval.append((interval[-1][1], left))
            interval.append((left, right))

        if len(interval) <= 0:
            interval.append((0, 24))
            return interval
        if interval[0][0] != 0:
            interval.insert(0, (0,interval[0][0]))
        if interval[-1][1] != 24:
            interval.append((interval[-1][1], 24))

        if DEBUG:
            print >> log, 'Intervals :'
            print >> log, interval
        return interval

    def _find_min_left(self, extreme, idx):
        for i in range(idx, -1, -1):
            if extreme[i] == 'min':
                if DEBUG:
                    print >> log, 'Find left minium point: %d' % i
                return i
        if DEBUG:
            print >> log, 'Find left margin minium: 0'
        return 0

    def _find_min_right(self, extreme, idx):
        for i in range(idx, len(extreme)):
            if extreme[i] == 'min':
                if DEBUG:
                    print >> log, 'Find right minium point: %d' % i
                return i
        if DEBUG:
            print >> log, 'Find right margin minium: %d' % (len(extreme) - 1)
        return len(extreme) - 1

    def _find_all_max(self, y, extreme, threshold):
        scope = max(y) - min(y)
        tmp = extreme
        for i in range(len(extreme)):
            if tmp[i] == 'max':
                left = self._find_min_left(tmp, i)
                right = self._find_min_right(tmp, i)
                if y[i] - y[left] < threshold * scope or y[i] - y[right] < threshold * scope:
                   tmp[i] = '-'
        return [i for i in range(len(tmp)) if tmp[i] == 'max']

    def tag_all_user(self,block=10):
        seq_user_dict = self.split_all_user(block)
        intervals = {}
        for user_id, seq_user in seq_user_dict.items():
            if DEBUG:
                print >> log, ('Now Processing userid: %s' % user_id)
            intervals[user_id] = self._tag_user(seq_user)
        return intervals

    def _tag_user(self, seq_user):
        # Create x coordinate
        x = [i for i in range(144)] 
        # Smooth curve
        x_s = [i for i in range(0, 144, 6)]
        y_s = spline(x, seq_user, x_s)
        if DEBUG:
            print >> log, ('Input smooth x and y:')
            print >> log , ', '.join([str(i) for i in x_s])
            print >> log , ', '.join([str(i) for i in y_s])
            print >> log, '-' * 100
        extreme_point = self._find_mm(y_s)
        if DEBUG:
            print >> log, 'Find max point:'
            print >> log, ', '.join(extreme_point)
        intervals = self._tags(y_s, extreme_point, threshold=0.5)
        return intervals

'''
def tag():
    # Read from file
    dataset = readfromfile(file)

    # Split 24 hours into intervals which has 10mins
    interval = [0, 10], [10, 20], ..., [1430, 1440]

    # y stands for each interval: 0 -> [0,10], 1 -> [10,20]
    y = [0, 1, 2, 3, 4, 0, 0, 0,...]

    # Calculate every user's program
    for user in users:
        # Calculate program's time span
        for program in user.programs:
            if program.timespan in interval:
                user.y[interval] += 1
        # Find all max point
        all_max_point = find_all_max()
        # Find left and right min point around max point and tag it
        for each_max_point in all_max_point:
            left = find_left_min()
            right = find_right_min()
            # Tag a interval between left and right
            tag = split(user, left, right)
        # Calculate cosine similarity between each tag
        sim_matrix = [sim_cosine(tag) for each tag]
        # Find connected component
        all_connected = find_connection(sim_matrix)

def dfs(p):
    # Node i is not visited
    if not visited[p]:
        # Set i visited
        visited[p] = True
        # Traverse all neighbour nodes
        for i in range(1, n + 1):
            # Filter and not visited
            # Weight(similarity) should be larger than a threshold
            # And node i isn't visited
            if matrix[p][i] >= 0.78 and not visited[i]:
                # Recursion search
                dfs(p)

# Find connected component
def find_connection(matrix):
    # At first all nodes are not visited
    visited = False
    # DFS all nodes
    for i in range(1, n + 1):
        nodes = []
        dfs(matrix, i, n, nodes, visited)
        # Find a connected component
        if len(nodes) > 0:
            connect.append(nodes)
    return connect
'''
# if __name__ == '__main__':
#     start_time = time.clock()
#     train = DataSet('train_all.csv')
#     columns = ['id','content_id','class_name','start','end','timespan','user_id']
#     user_dict = MakeDict.to_dict_byUser(train, columns, -1)
#     timespliter = TimeSpliter(user_dict)
#     time_tag = timespliter.tag_all_user()
# 
#     end_time = time.clock()
#     print 'Finished in: %ds' % (end_time - start_time)
