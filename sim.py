import cPickle as pickle
from math import sqrt
from userplot import convert_to_minute
from dfs import find_connection

log = open('sim.log', 'w')
DEBUG = False

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
        user_id, start, end, timespan, class_name = line.split(',')
        user_dict.setdefault(user_id, [])
        user_dict[user_id].append({'start':start, 'end':end, 'timespan':timespan, 'class':class_name.strip()})
    return user_dict

def tag(user_dict, user_time):
    tag_dict = {}
    for user_id, play_list in user_dict.items():
        # if user_id != '1':
        #     continue
        if DEBUG:
            print >> log, 'Now tagging user: ',user_id
        tag_list = {}
        tag = 1
        for idx, play in enumerate(play_list):
            start = play['start']
            end = play['end']
            timespan = play['timespan']
            class_name = play['class']

            for t in user_time[user_id]:
                # inter_span = (t[1] - t[0]) * 3600
                if t not in tag_list.keys():
                    tag_list.setdefault(t, 'tag' + str(tag))
                    tag += 1
                if across(t, convert_to_hour(start)):
                    if DEBUG:
                        print >> log, '*' * 100
                        print >> log, 'Across: ', t
                        print >> log, '*' * 100
                    play_list[idx] = {'start':start, 'end':end, 'class':class_name, 'timespan':timespan, 'tag':tag_list[t]}
                    if DEBUG:
                        print >> log, 'Play_list', play_list[idx] 
                        print >> log, 'idx',  idx
                        print >> log, '*' * 100
            #print start, end, class_name
        tag_dict[user_id] = tag_list
    return tag_dict

def rate(tag):
    rate_list = {}
    for key in tag:
        rate_list.setdefault(key[0], 0)
        rate_list[key[0]] += 1

    for key,value in rate_list.items():
        rate_list[key] /= 1.0 * len(tag)
    # print rate_list
    return rate_list

def rate_span(tag, tag_span):
    rate_list = {}
    for key in tag:
        rate_list.setdefault(key[0], 0)
        rate_list[key[0]] += float(key[1])
    for key,value in rate_list.items():
        # print 'key', key
        rate_list[key] = rate_list[key] / 1.0 * tag_span / len(tag) 
    # print rate_list
    return rate_list

def similarity(tags, tag_list, key1, key2):
    try:
        len_tag1 = len(tags[key1])
        len_tag2 = len(tags[key2])
    except:
        return 0
    tag1_span = tag_list[key1]
    tag2_span = tag_list[key2]

    rate1 = rate_span(tags[key1], tag1_span)
    rate2 = rate_span(tags[key2], tag2_span)

    # rate1 = rate(tags[key1])
    # rate2 = rate(tags[key2])

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
    # if r != 1:
    #     print r
    #     print tags[key1]
    #     print tags[key2]
    #     print '-' * 100
    return r
    #print tags[key1], len_tag1, rate1
    #print tags[key2], len_tag2, rate2

def extract_class(user_dict):
    user_tag = {}
    # For every user
    for user_id, play_list in user_dict.items():
        # if user_id != '1':
        #     continue
        # For every play entry
        user_tag.setdefault(user_id, {})
        for idx, play in enumerate(play_list):
            class_name = play['class']
            tag = play['tag']
            timespan = play['timespan']
            user_tag[user_id].setdefault(tag, [])
            user_tag[user_id][tag].append((class_name, timespan))
    # print user_tag
    return user_tag

# {(0,13):'tag1'} to {'tag1':(0,13)}
def reverse(tag_dict):
    new_dict = {}
    for user_id, tag_list in tag_dict.items():
        for key, value in tag_list.items():
            new_dict.setdefault(user_id, {})
            new_dict[user_id][value] = (key[1] - key[0]) * 3600
    return new_dict

def main():
    user_pickle = file('user_time.pkl', 'rb')
    user_time = pickle.load(user_pickle)
    # user_time = {}
    # time = [(0, 7), (7, 12), (12, 18), (18, 23)]
    # for i in range(1, 26146):
    #     user_time[str(i)] = time
    #print user_time
    if DEBUG:
        print >> log, 'Successfully read pickle!'
    user_dict = file_to_dict('train.csv')
    # print user_dict['5633']
    # print '*' * 100
    tag_dict = tag(user_dict, user_time)
    # print user_dict['1']
    # print tag_dict['5633']
    tag_dict = reverse(tag_dict)
    # print tag_dict['5633']
    # print '*' * 100
    user_tag = extract_class(user_dict)
    # print user_tag['5633']
    # print '*' * 100

    one = 0
    multi = 0
    for user_id, tags in user_tag.items():
        # print tags
        # if user_id != '5633':
        #     continue
        tag_list = tag_dict[user_id]
        # print 'Tag_list:'
        # print tag_list
        # print 'Tags:'
        # print tags
        # keys_t = tags.keys()
        # print 'Tags.keys', keys_t
        keys = tag_list.keys()
        # print 'tag_list keys', keys

        matrix = [[0 for col in range(len(keys) + 1)] for row in range(len(keys) + 1)]
        # print matrix
        for i in range(len(keys)):
            for j in range(len(keys)):
                if i != j:
                    # print keys[i], keys[j]
                    # print '-' * 100
                    matrix[i + 1][j + 1] = similarity(tags,tag_list, keys[i], keys[j])
                    # print matrix[i][j]
                    # print '*' * 100

        # print '-' * 100
        # print 'Userid: ', user_id
        # for m in matrix:
        #     print m
        # print '-' * 100

        result = find_connection(matrix)
        if len(result) == 1:
            one += 1
        else:
            multi += 1
    print one, multi


if __name__ == '__main__':
   main()
