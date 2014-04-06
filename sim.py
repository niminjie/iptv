import cPickle as pickle
from userplot import convert_to_minute

def across(interval, time):
    if interval[0] < time <= interval[1]:
        return True
    else:
        return False

def main():
    user_pickle = file('user_time.pkl', 'rb')
    user_time = pickle.load(user_pickle)
    #for user_id, intervals in user_time.items():
    #    user_time[user_id] = map(lambda x: [x[0] * 60, x[1] * 60], intervals)
    print user_time['1']
    for line in open('train.csv', 'r'):
        user_id, start, end, class_name = line.split(',')
        if user_id != '1':
            continue
        # for t in user_time[user_id]:
        #     if across(t, convert_to_minute(start)) and across(t, convert_to_minute(end)):
        #         print t, convert_to_minute(start), convert_to_minute(end)

if __name__ == '__main__':
   main() 
