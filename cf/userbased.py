from math import sqrt
from operator import itemgetter
import cPickle

# fo_pickle = file('remap.pkl', 'wb')
fi_pickle = file('remap.pkl', 'rb')
# tranverse_pickle = file('item_user.pkl', 'wb')
DEBUG = False
if DEBUG:
    log = open('userbased.log', 'w')
# user_remap = open('user_remap.csv', 'w')

def get_remap(fi):
    remap = {}
    for line in fi:
        user_id, tag, user = line.split(',')
        # remap.setdefault(user, user_id)
        remap[user.strip()] = user_id
    return remap

def test_file2dict(fi):
    user_dict = {}
    for line in open(fi):
        id, content_id, class_name, start, end, timespan, user_id = line.split(',')
        user_id = user_id.strip()
        user_dict.setdefault(user_id, [])
        if class_name not in user_dict[user_id]:
            user_dict[user_id].append(class_name)
    return user_dict

def prepareData(prefs, f) :
    for line in f:
        line_split = line.split(',')
        if not line_split[0] in prefs:
            prefs[line_split[0]] = {line_split[1]:float(line_split[2].strip())}
        else: 
            prefs[line_split[0]][line_split[1]] = float(line_split[2].strip())

def sim_cosine(prefs, p1, p2):
    mod1 = 0.0
    mod2 = 0.0
    metrix = 0.0
    for key,value in prefs[p1].items():
        if key in prefs[p2]:
            metrix = metrix + value * prefs[p2][key] 

    for key,value in prefs[p1].items():
        mod1 = mod1 + value * value
    for key,value in prefs[p2].items():
        mod2 = mod2 + value * value

    mod1 = sqrt(mod1) 
    mod2 = sqrt(mod2) 
    r = metrix / (mod1 * mod2)
    #print("Person1 : %3s,Person2 : %3s Similarity:%3f" %(p1, p2, round(r, 2)))
    return r

def topMatches(prefs, person, n=100):
    scores=[(sim_cosine(prefs, person, other), other) for other in prefs if other != person] 
    scores.sort() 
    scores.reverse() 
    cnt = 0
    return scores[0:n]

def getRecommendations(prefs, person, n=100, k=5):
    totals = {}
    simSums = {}

    sims = topMatches(prefs, person, n) 
    #print("Neigh: " +str(sims) + "Person: " + person)
    for item in sims:
        other = item[1]
        for i in prefs[other]:
            # if i not in prefs[person] or prefs[person][i] == 0 :
            totals.setdefault(i,0)
            #totals[i] = Decimal('0')
            totals[i] += prefs[other][i] * item[0]
            simSums.setdefault(i,0)
            simSums[i] += item[0]
    rankings = []
    for item,total in totals.items():
        if simSums[item] == 0 : continue
        #print("Person: %s, Total :%f , simSum :%f, Item: %s" %(person, total, simSums[item], item))
        #rankings.append((Decimal(str(total)) / Decimal(str(simSums[item])), item))
        rankings.append([total / simSums[item], item])
    rankings.sort()
    rankings.reverse()
    if k == 0:
        return rankings
    return rankings[0:k]

def calRecallandPrecision(prefs, test_dict, remap, n=100,k=5):
    print("n = %d,k = %d" %(n, k))
    # idx = 0
    hit = 0
    n_recall = 0
    n_precision = 0
    for person in prefs.keys():
        # if idx > 100:
        #     break
        print 'Now Processing person:', person
        if person not in test_dict:
            continue
        # idx += 1
        tu = test_dict[person]
        for item in tu:
            print item
        result = getRecommendations(prefs, person, n, k, similarity)
        print '-' * 100
        for pui, item in result:
            print item
            if item in tu:
                hit += 1
        n_recall += len(tu)
        if k > len(result):
            n_precision += len(result)
        else:
            n_precision += k
        # print '*' * 100
    print "Hit : ", str(hit)
    print n_recall, n_precision
    # foutput.write('%d,%d,%d,%f,%f,%f,%f \r\n' %(hit,n,k,hit / (n_recall * 1.0),hit / (n_precision * 1.0),calRMSE(prefs,n,k,similarity),calMAE(prefs,n,k,similarity)))
    # foutput.flush()
    # print( "Cosine " + "Recall is :" + str(hit / (n_recall * 1.0)) + "  Precision is :" + str(hit / (n_precision * 1.0)))
    #return [hit / (n_recall * 1.0),hit / (n_precision * 1.0)]

def calRecallandPrecision_2(prefs, test_dict, remap, W, n=100,k=5):
    print("n = %d,k = %d" %(n, k))
    idx = 0
    hit = 0
    n_recall = 0
    n_precision = 0
    for person in remap:
        # Exclude new user in test dastaset
        if idx > 100:
            continue
        if person not in test_dict:
            continue
        idx += 1
        # Get different tag of one user '03EF1230124124' --->  [123,124,125]
        person2id_list = remap[person]
        # Handle each tag recommend list
        all_rec_result = []
        tu = test_dict[person]
        for each_tag in person2id_list:
            print 'Now Processing person:', person,'\nAnd id:', each_tag
            # Program which test user watched
            # result = getRecommendations(prefs, each_tag, n, k)
            result = recommend(prefs, each_tag, W, k)
            print result
            for item in result:
                all_rec_result.append(item[0])        
        # Distinct same program 
        all_rec_result = set(all_rec_result)
        for item in all_rec_result:
            if item in tu:
                hit += 1
        n_recall += len(tu)
        if k > len(all_rec_result):
            n_precision += len(all_rec_result)
        else:
            n_precision += k
        # print '*' * 100
    print "Hit : ", str(hit)
    print n_recall, n_precision
    print hit * 1.0 / n_recall
    print hit * 1.0 / n_precision

def process_input(prefs, f):
    uniq_tag = {}
    idx = {}
    for line in open(f, 'r'):
        id, content_id, start, end, timespan, class_name, user_id, interval, interspan = line.split('|')
        idx.setdefault(user_id, 1)
        uniq_tag.setdefault(user_id, {})
        rate = float(timespan) / float(interspan)
        if interval not in uniq_tag[user_id].keys():
            # print interval, idx[user_id]
            uniq_tag[user_id][interval] = str(idx[user_id])
            idx[user_id] += 1
        if DEBUG:
            print >>log, 'Add new user:', user_id
        # {user_id:[playlist1, playlist2]}
        prefs.setdefault(user_id, [])
        prefs[user_id].append({'interval':interval, 'id':id, content_id:rate, 'content_id':content_id, 'class_name':class_name, 'rate':rate, 'tag':uniq_tag[user_id][interval]})

def process_mergeuser(prefs, fo):
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

def process_rate(fi):
    fo = open('train_rate.csv', 'w')
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
        times[(user, class_name)] += 1

    for user, plays in new_dict.items():
        for key, play in plays.items():
            fo.write('%s,%s,%s\n' % (user, key, play / times[(user, key)]))
            fo.flush()
    fo.close()

def tranverse(train):
    '''
       {'1':{'class1':5, 'class2':4}}
    '''
    item_user = {}
    for user, item in train.items():
        for i in item:
            item_user.setdefault(i, [])
            if user not in item_user[i]:
                # item_user[i].append({user:train[user][i]})
                item_user[i].append(user)
                # print item_user[i]
    cPickle.dump(item_user, tranverse_pickle, True)
    # print item_user

def itemSim(train):
    # Input :{'class1':[user1, user2]} 
    C = {}
    N = {}
    items = train.keys()
    for i in items:
        N.setdefault(i, len(train[i]))
        C.setdefault(i, {})
        for j in items:
            if i == j:
                continue
            N.setdefault(j, len(train[j]))
            C.setdefault(j, {})
            C[i][j] = len(list(set(train[i]).intersection(set(train[j]))))
            # print C[i][j]
    W = {}
    for i, related_items in C.items():
        W.setdefault(i, {})
        for j, cij in related_items.items():
            W[i].setdefault(j, 0)
            W[i][j] = cij * 1.0 / sqrt(N[i] * N[j])
            # print W[i][j]
    items = W.keys()
    # for i in items:
    #     for j in items:
    #         if i == j:
    #             continue
    #         if W[i][j] > 0.3:
    #             # print W[i][j],
    return W

def recommend(train, user_id, W, k=5):
    rank = {}
    ru = train[user_id]
    # print ru
    # print '*' * 100
    for i, pi in ru.items():
        sorted_sim = sorted(W[i].items(), key=itemgetter(1), reverse=True)[0:k]
        # sorted_sim = sorted(W[i].items(), key=itemgetter(1), reverse=True)
        # for item in sorted_sim:
        #     print item[0]
        # print '-' * 100
        for j, wj in sorted_sim:
            # if j in ru:
            #     continue
            # print j
            rank.setdefault(j, 0.0)
            rank[j] += pi * wj
    rank = sorted(rank.items(), key=itemgetter(1), reverse=True)
    # rec_list = [item[0] for item in rank]
    return rank[0:k]

def main():
    train_pre = {}
    test_path = '../test_all.csv'
    remap = get_remap(open('user_remap.csv', 'r'))
    # merge_remap = {}
    # for user, user_id in remap.items():
    #     merge_remap.setdefault(user_id, [])
    #     for user2, user_id2 in remap.items():
    #         if user_id == user_id2 and user2 not in merge_remap[user_id]:
    #             merge_remap[user_id].append(user2)
    #             print user_id,merge_remap[user_id]
    # print merge_remap
    # Pickle.dump(merge_remap, fo_pickle, True)
    # print merge_remap['00034C968355']
    merge_remap = cPickle.load(fi_pickle)
    test_dict = test_file2dict(test_path)
    # print test_dict
    prepareData(train_pre, open('train_rate.csv'))
    # tranverse(train_pre)
    train_pre_verse = cPickle.load(file('item_user.pkl', 'rb'))
    W = itemSim(train_pre_verse)
    # rec = recommend(train_pre, '1', W, k=5)
    # for item in rec:
    #     print item
    calRecallandPrecision_2(train_pre, test_dict, merge_remap, W, n=4, k=5)
    # rec = getRecommendations(train_pre, '1', n=100, k=5)
    # for r in rec:
    #     print r[1]

if __name__ == '__main__':
    # train_pre = {}
    # process_input(train_pre, 'tag_result_origin.csv')
    # process_mergeuser(train_pre, open('tmp', 'w'))
    main()
    if DEBUG:
        log.close()
