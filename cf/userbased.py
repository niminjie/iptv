from math import sqrt
from operator import itemgetter
from recsys.algorithm.factorize import SVD
from recsys.datamodel.data import Data
from recsys.datamodel.item import Item
from recsys.datamodel.user import User
from recsys.evaluation.decision import PrecisionRecallF1
from recsys.evaluation.prediction import RMSE, MAE
import cPickle
import recsys.algorithm
recsys.algorithm.VERBOSE = True
import sys

# fo_pickle = file('remap.pkl', 'wb')
# fi_pickle = file('remap.pkl', 'rb')
# tranverse_pickle = file('item_user.pkl', 'wb')
# user_remap = open('user_remap.csv', 'w')

DEBUG = False
if DEBUG:
    log = open('userbased.log', 'w')

def get_remap(fi):
    remap = {}
    for line in fi:
        user_id, tag, user = line.split(',')
        # remap.setdefault(user, user_id)
        remap[user.strip()] = user_id
    return remap

def test_file2dict(fi):
    user_dict = {}
    for line in fi:
        id, content_id, class_name, start, end, timespan, user_id = line.split(',')
        user_id = user_id.strip()
        user_dict.setdefault(user_id, [])
        if class_name not in user_dict[user_id]:
            user_dict[user_id].append(class_name)
        # if content_id not in user_dict[user_id]:
        #     user_dict[user_id].append(content_id)
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

def svd_rec(person, n):
    svd = SVD()
    train = Data()
    train.load('./randUser/rate1.csv', force=True, sep=',', format={'col':0, 'row':1, 'value':2, 'ids':str})
    svd.set_data(train)
    svd.compute(k=5, min_values=0, pre_normalize=None, mean_center=False, post_normalize=True)
    rec_list = svd.recommend(person, n, only_unknowns=False, is_row=False)
    return rec_list

def calRecallandPrecision(prefs, test_dict, remap, W, n=100, k=5, itemcf=False):
    print("n = %d, k = %d" %(n, k))
    hit = 0
    n_recall = 0
    n_precision = 0
    for person in remap:
        # Exclude new user in test dastaset
        if person not in test_dict:
            continue
        # Get different tag of one user '03EF1230124124' --->  [123,124,125]
        person2id_list = remap[person]
        # Handle each tag recommend list
        all_rec_result = []
        tu = test_dict[person]
        for each_tag in person2id_list:
            # print 'Now Processing person:', person,'\nAnd id:', each_tag
            # Program which test user watched
            if itemcf:
                result = recommend(prefs, each_tag, W, k)
            else:
                result = svd_rec(int(each_tag), k)
                # result = getRecommendations(prefs, each_tag, n, k)
                # print result
                # print '-' * 100
            for item in result:
                if itemcf:
                    all_rec_result.append(item[0])        
                else:
                    all_rec_result.append(item[0].encode('utf-8'))        
        # Distinct same program 
        all_rec_result = set(all_rec_result)
        # print '-' * 100
        # print all_rec_result
        # print tu
        # print '-' * 100
        for item in all_rec_result:
            if item in tu:
                hit += 1
        n_recall += len(tu)
        if k > len(all_rec_result):
            n_precision += len(all_rec_result)
        else:
            n_precision += k
        # print '*' * 100
    # print "Hit : ", str(hit)
    # print n_recall, n_precision
    print 'Recall: \t', hit * 1.0 / n_recall
    print 'Precision:\t', hit * 1.0 / n_precision
    print '-' * 30

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
    # cPickle.dump(item_user, tranverse_pickle, True)
    return item_user

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
    for i, pi in ru.items():
        sorted_sim = sorted(W[i].items(), key=itemgetter(1), reverse=True)[0:k]
        for j, wj in sorted_sim:
            rank.setdefault(j, 0.0)
            rank[j] += pi * wj
    rank = sorted(rank.items(), key=itemgetter(1), reverse=True)
    return rank[0:k]

def recommend_notag(train, user_id, W, k=5):
    rank = {}
    ru = train[user_id]
    print ru
    for i, pi in ru.items():
        sorted_sim = sorted(W[i].items(), key=itemgetter(1), reverse=True)[0:k]
        for j, wj in sorted_sim:
            rank.setdefault(j, 0.0)
            rank[j] += pi * wj
    rank = sorted(rank.items(), key=itemgetter(1), reverse=True)
    return rank[0:k]

def test100_UserCF(f_train, f_test, f_remap, n, k):
    train_pre = {}
    remap = get_remap(f_remap)
    merge_remap = {}
    for user, user_id in remap.items():
        merge_remap.setdefault(user_id, [])
        for user2, user_id2 in remap.items():
            if user_id == user_id2 and user2 not in merge_remap[user_id]:
                merge_remap[user_id].append(user2)
    test_dict = test_file2dict(f_test)
    prepareData(train_pre, f_train)
    train_pre_verse = tranverse(train_pre)
    W = itemSim(train_pre_verse)
    for i in range(1, n + 1):
        for j in range(1, k + 1):
            calRecallandPrecision(train_pre, test_dict, merge_remap, W, i, j, itemcf=False)

def test100_ItemCF(f_train, f_test, f_remap,n, k):
    train_pre = {}
    remap = get_remap(f_remap)
    merge_remap = {}
    for user, user_id in remap.items():
        merge_remap.setdefault(user_id, [])
        for user2, user_id2 in remap.items():
            if user_id == user_id2 and user2 not in merge_remap[user_id]:
                merge_remap[user_id].append(user2)
    test_dict = test_file2dict(f_test)
    prepareData(train_pre, f_train)
    train_pre_verse = tranverse(train_pre)
    W = itemSim(train_pre_verse)
    for i in range(1, n + 1):
        for j in range(1, k + 1):
            calRecallandPrecision(train_pre, test_dict, merge_remap, W, i, j, itemcf=True)

if __name__ == '__main__':
    test = open('../test_all.csv')
    remap1 = open('randUser/remap1.csv')
    train1 = open('randUser/rate1.csv')
    test100_UserCF(train1, test, remap1, 20, 5)
    # test100_ItemCF(train1, test, remap1, 20, 5)
    if DEBUG:
        log.close()
