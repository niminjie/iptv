import datetime
from DataSet import DataSet
import MakeDict
import time
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import spline

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
            # start_time = t[0]
            # end_time = t[1]
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

if __name__ == '__main__':
    start_time = time.clock()
    train = DataSet('train_all.csv')
    columns = ['id','content_id','class_name','start','end','timespan','user_id']
    user_dict = MakeDict.to_dict_byUser(train, columns, -1)
    timespliter = TimeSpliter(user_dict)
    time_tag = timespliter.split_all_user()
    print time_tag
    end_time = time.clock()
    print 'Finished in: %ds' % (end_time - start_time)
