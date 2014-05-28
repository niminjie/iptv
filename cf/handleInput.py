import random
import myPickle
DEBUG = False

video_info = myPickle.load('../video.pkl')
def transverse(train):
    '''
       {'1':{'class1':5, 'class2':4}}
    '''
    item_user = {}
    for user, item in train:
        print user
        print item

def process_rate(fi, fo):
    '''
        Some users rate same class several times,so we calculate a average score
        User1, tv,  4
        User1, tv,  2
        ---->
        User1, tv,  3
    '''
    # fo = open('train_rate.csv', 'w')
    new_dict = {}
    times = {}
    for line in fi:
        user, class_name, rate = line.split(',')
        user = int(user)
        rate = float(rate.strip())

        new_dict.setdefault(user,{})
        times.setdefault((user, class_name), 0)
        new_dict[user].setdefault(class_name, 0)

        new_dict[user][class_name] += rate
        # User play class_name times
        times[(user, class_name)] += 1

    for user, plays in new_dict.items():
        for class_name, play in plays.items():
            fo.write('%s,%s,%s\n' % (user, class_name, play / times[(user, class_name)]))
            fo.flush()
    fo.close()

def process_mergeuser(prefs, fo, user_remap):
    '''
       Split different tags to different users
       Hash complex userid to number and output to file

       eg.  00034C981F23,tag1  ----->   1
            00034C981F23,tag2  ----->   2
            ...
    '''
    # User index
    user = 0
    for user_id, plays in prefs.items():
        uniq_tag = {}
        for play in plays:
            tag = play['tag']
            class_name = play['class_name']
            rate = play['rate']
            if tag not in uniq_tag.keys():
                user += 1
                uniq_tag.setdefault(tag, user)
                user_remap.write('%s,%s,%s\n' % (user_id, tag, user))
                user_remap.flush()
            fo.write('%s,%s,%s\n' % (uniq_tag[tag], class_name, rate))
            fo.flush()
    fo.close()
    user_remap.close()

def process_mergeuser_content(prefs, fo, user_remap):
    '''
       Split different tags to different users
       Hash complex userid to number and output to file

       eg.  00034C981F23,tag1  ----->   1
            00034C981F23,tag2  ----->   2
            ...
    '''
    # User index
    user = 0
    for user_id, plays in prefs.items():
        uniq_tag = {}
        for play in plays:
            tag = play['tag']
            content_id = play['content_id']
            rate = play['rate']
            if tag not in uniq_tag.keys():
                user += 1
                uniq_tag.setdefault(tag, user)
                user_remap.write('%s,%s,%s\n' % (user_id, tag, user))
                user_remap.flush()
            fo.write('%s,%s,%s\n' % (uniq_tag[tag], content_id, rate))
            fo.flush()
    fo.close()
    user_remap.close()

def modify_tag(prefs, fo, user_remap):
    uniq_tag = {}

def process_input(prefs, f):
    '''
        Convert interval into tag and calculate rate
        eg.  User:00034C981F23
             (0,4),(4,20)  -----> tag1
             (20,24)       -----> tag2
             ...
    '''
    # Handle uniq tag dict
    uniq_tag = {}
    # idx stands for tag number of same user
    idx = {}
    err = []
    for line in open(f, 'r'):
        id, content_id, start, end, timespan, class_name, user_id, interval, interspan = line.split('|')
        idx.setdefault(user_id, 1)
        uniq_tag.setdefault(user_id, {})
        rate = float(timespan) / float(interspan)
        # rate = float(timespan) / float(video_info[content_id])
        # Tag = interval
        if interval not in uniq_tag[user_id].keys():
            # print interval, idx[user_id]
            uniq_tag[user_id][interval] = str(idx[user_id])
            idx[user_id] += 1
        if DEBUG:
            print >>log, 'Add new user:', user_id
        # {user_id:[playlist1, playlist2]}
        prefs.setdefault(user_id, [])
        prefs[user_id].append({'interval':interval, 'id':id, content_id:rate, 'content_id':content_id, 'class_name':class_name, 'rate':rate, 'tag':uniq_tag[user_id][interval]})

def process_input_oneday(prefs, f):
    '''
        Convert interval into tag and calculate rate
        eg.  User:00034C981F23
             (0,4),(4,20)  -----> tag1
             (20,24)       -----> tag1
             ...
    '''
    for line in open(f, 'r'):
        id, content_id, start, end, timespan, class_name, user_id, interval, interspan = line.split('|')
        # rate = float(timespan) / 1440
        rate = float(timespan) / float(video_info[content_id])
        # Tag = interval
        if DEBUG:
            print >>log, 'Add new user:', user_id
        # {user_id:[playlist1, playlist2]}
        prefs.setdefault(user_id, [])
        prefs[user_id].append({'interval':interval, 'id':id, content_id:rate, 'content_id':content_id, 'class_name':class_name, 'rate':rate, 'tag':1})

def get_remap(fi):
    remap = {}
    for line in fi:
        user_id, tag, user = line.split(',')
        # remap.setdefault(user, user_id)
        remap[user.strip()] = user_id
    return remap

def testfile_to_dict(fi):
    user_dict = {}
    for line in open(fi):
        id, content_id, class_name, start, end, timespan, user_id = line.split(',')
        user_id = user_id.strip()
        user_dict.setdefault(user_id, [])
        if class_name not in user_dict[user_id]:
            user_dict[user_id].append(class_name)
    return user_dict

# def extract_train(fi, n, k):
def extract_train(n):
    '''
        Generate K groups which contains n users
    '''
    fi = open('tag_result_origin.csv', 'r')
    fo = open('./randUser2/randUser1.csv', 'w')
    user_dict = {}
    for line in fi:
        user_id = line.split('|')[6]
        user_dict.setdefault(user_id, [])
        user_dict[user_id].append(line)
    for i in range(n):
        rand_key = random.choice(user_dict.keys())
        for l in user_dict[rand_key]:
            fo.write(l)
        user_dict.pop(rand_key)

if __name__ == '__main__':
    # extract_train(100)
    train_pre = {}
    ''' Time tag '''
    # process_input(train_pre, 'randUser/randUser1.csv')
    # process_mergeuser(train_pre, open('randUser/DiffRate/merge1.csv', 'w'), open('randUser/DiffRate/remap1.csv', 'w'))
    # process_rate(open('randUser/DiffRate/merge1.csv'), open('randUser/DiffRate/rate1.csv', 'w'))
    'Test ---------------------------------------------------------------------'
    # process_input(train_pre, 'Test/test_tag_result.csv')
    # process_mergeuser(train_pre, open('Test/test_merge1.csv', 'w'), open('Test/test_remap1.csv', 'w'))
    # process_rate(open('Test/test_merge1.csv'), open('Test/test_rate1.csv', 'w'))
    ''' No Tag '''
    # process_input_oneday(train_pre, 'randUser/randUser2.csv')
    # process_mergeuser(train_pre, open('onedaySet/merge2.csv', 'w'), open('onedaySet/remap2.csv', 'w'))
    # process_rate(open('onedaySet/merge2.csv'), open('onedaySet/rate2.csv', 'w'))
    ''' Content_id based tag '''
    # process_input(train_pre, 'randUser/Content/randUser2.csv')
    # process_mergeuser_content(train_pre, open('randUser/Content/merge2.csv', 'w'), open('randUser/Content/remap2.csv', 'w'))
    # process_rate(open('randUser/Content/merge2.csv'), open('randUser/Content/rate2.csv', 'w'))
    'Test ---------------------------------------------------------------------'
    # process_input(train_pre, 'Test/test_tag_result.csv')
    # process_mergeuser_content(train_pre, open('Test/test_merge1.csv', 'w'), open('Test/test_remap1.csv', 'w'))
    # process_rate(open('Test/test_merge1.csv'), open('Test/test_rate1.csv', 'w'))
    ''' Content_id based no tag '''
    # process_input_oneday(train_pre, 'randUser/randUser2.csv')
    # process_mergeuser_content(train_pre, open('onedaySet/Content/merge2.csv', 'w'), open('onedaySet/Content/remap2.csv', 'w'))
    # process_rate(open('onedaySet/Content/merge2.csv'), open('onedaySet/Content/rate2.csv', 'w'))
