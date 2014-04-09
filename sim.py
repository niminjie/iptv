import cPickle as pickle
from math import sqrt
from userplot import convert_to_minute
from dfs import find_connection

log = open('sim.log', 'w')
DEBUG = True

def across(interval, time):
    if interval[0] <= time < interval[1] or (time == 23 and interval[1] == 23):
        return True
    else:
        return False

def convert_to_hour(time):
    hour = int(time.split(' ')[1].split(':')[0])
    return hour

def file_to_dict(train):
    user_dict = {}
    for line in open(train, 'r'):
        user_id, start, end, class_name = line.split(',')
        user_dict.setdefault(user_id, [])
        user_dict[user_id].append({'start':start, 'end':end, 'class':class_name.strip()})
    return user_dict

def tag(user_dict, user_time):
    for user_id, play_list in user_dict.items():
        if DEBUG:
            print >> log, 'Now tagging user: ',user_id
        tag_list = {}
        tag = 1
        #if user_id != '3':
        #    continue
        for idx, play in enumerate (play_list):
            start = play['start']
            end = play['end']
            class_name = play['class']

            for t in user_time[user_id]:
                if across(t, convert_to_hour(start)):
                    if t not in tag_list.keys():
                        tag_list.setdefault(t, 'tag' + str(tag))
                        tag += 1
                    if DEBUG:
                        print >> log, '*' * 100
                        print >> log, 'Across: ', t
                        print >> log, '*' * 100
                    play_list[idx] = {'start':start, 'end':end, 'class':class_name, 'tag':tag_list[t]}
                    if DEBUG:
                        print >> log, 'Play_list', play_list[idx] 
                        print >> log, 'idx',  idx
                        print >> log, '*' * 100
            #print start, end, class_name

def rate(tag):
    rate_list = {}
    for key in tag:
        rate_list.setdefault(key, 0)
        rate_list[key] += 1
    
    for key,value in rate_list.items():
        rate_list[key] /= 1.0 * len(tag)
    return rate_list

def similarity(tags, key1, key2):
    len_tag1 = len(tags[key1])
    len_tag2 = len(tags[key2])
    rate1 = rate(tags[key1])
    rate2 = rate(tags[key2])
    mod1 = 0.0
    mod2 = 0.0
    metrix = 0.0

    for key,value in rate1.items():
        if key in rate2:
            metrix = metrix + value * rate2[key] 
    for key,value in rate1.items():
        mod1 = mod1 + value * value
    for key,value in rate2.items():
        mod2 = mod2 + value * value
    mod1 = sqrt(mod1) 
    mod2 = sqrt(mod2) 
    r = metrix / (mod1 * mod2)
    #print rate1
    #print rate2
    #print r
    #print '-' * 100
    #if r != 1:
    #    print tags[key1]
    #    print tags[key2]
    #    print '-' * 100
    return r
    #print tags[key1], len_tag1, rate1
    #print tags[key2], len_tag2, rate2

def extract_class(user_dict):
    user_tag = {}
    # For every user
    for user_id, play_list in user_dict.items():
        # For every play entry
        user_tag.setdefault(user_id, {})
        for idx, play in enumerate(play_list):
            class_name = play['class']
            tag = play['tag']
            user_tag[user_id].setdefault(tag, [])
            user_tag[user_id][tag].append(class_name)
    return user_tag

def main():
    user_pickle = file('user_time.pkl', 'rb')
    user_time = pickle.load(user_pickle)

    if DEBUG:
        print >> log, 'Successfully read pickle!'
    user_dict = file_to_dict('train.csv')
    tag(user_dict, user_time)
    user_tag = extract_class(user_dict)

    for user_id, tags in user_tag.items():
        # if user_id != '1':
        #     continue
        keys = tags.keys()
        # totals = 0
        # for key in keys:
        #     totals += len(tags[key])
        matrix = [[0 for col in range(len(keys))] for row in range(len(keys))]
        # print matrix
        for i in range(len(keys)):
            for j in range(len(keys)):
                if i != j:
                    matrix[i][j] = similarity(tags, keys[i], keys[j])
        print matrix
        # print find_connection(matrix)

if __name__ == '__main__':
   main()
