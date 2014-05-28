from DataSet import DataSet
from MakeDict import *
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
recsys.algorithm.VERBOSE = False
import sys

class Recommender():
    def __init__(self, train, test, remap, svd_train):
        self.train_set = train
        self.test_set = test
        self.remap = self._get_remap(remap)
        self.W = self._reverse_user_item()

        self.svd = SVD()
        self.svd.set_data(svd_train)
        self.svd.compute(k=10, min_values=0, pre_normalize=None, mean_center=False, post_normalize=True)

    def _reverse_user_item(self):
        train_pre_verse = self._reverse()
        return self._itemSim(train_pre_verse)

    def _reverse(self):
        '''
           {'1':{'class1':5, 'class2':4}}
        '''
        item_user = {}
        for user, item in self.train_set.items():
            for i in item:
                item_user.setdefault(i, [])
                if user not in item_user[i]:
                    # item_user[i].append({user:self.train_set[user][i]})
                    item_user[i].append(user)
        # cPickle.dump(item_user, tranverse_pickle, True)
        return item_user

    def _sim_cosine(self, prefs, p1, p2):
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

    def _topMatches(self, prefs, person, n=5):
        scores=[(self._sim_cosine(prefs, person, other), other) for other in prefs if other != person]
        scores.sort() 
        scores.reverse() 
        return scores[0:n]

    def _itemSim(self, train):
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
        self.W = {}
        for i, related_items in C.items():
            self.W.setdefault(i, {})
            for j, cij in related_items.items():
                self.W[i].setdefault(j, 0)
                self.W[i][j] = cij * 1.0 / sqrt(N[i] * N[j])
                # print self.W[i][j]
        items = self.W.keys()
        return self.W

    def _get_remap(self, fi):
        remap = {}
        for line in open(fi):
            user_id, tag, user = line.split(',')
            remap[user.strip()] = user_id
        merge_remap = {}
        for user, user_id in remap.items():
            merge_remap.setdefault(user_id, [])
            for user2, user_id2 in remap.items():
                if user_id == user_id2 and user2 not in merge_remap[user_id]:
                    merge_remap[user_id].append(user2)
        return merge_remap

    def ucf_recommend(self, person, n=5, k=5):
        totals = {}
        simSums = {}

        sims = self._topMatches(self.train_set, person, n) 
        #print("Neigh: " +str(sims) + "Person: " + person)
        for item in sims:
            other = item[1]
            for i in self.train_set[other]:
                # if i not in self.train_set[person] or self.train_set[person][i] == 0 :
                totals.setdefault(i,0)
                #totals[i] = Decimal('0')
                totals[i] += self.train_set[other][i] * item[0]
                simSums.setdefault(i,0)
                simSums[i] += item[0]
        rankings = []
        for item,total in totals.items():
            if simSums[item] == 0 : continue
            rankings.append([total / simSums[item], item])
        rankings.sort()
        rankings.reverse()
        if k == 0:
            return rankings
        return rankings[0:k]

    def icf_recommend(self, user_id, n=5, k=5):
        rank = {}
        ru = self.train_set[user_id]
        for i, pi in ru.items():
            sorted_sim = sorted(self.W[i].items(), key=itemgetter(1), reverse=True)[0:k]
            for j, wj in sorted_sim:
                rank.setdefault(j, 0.0)
                rank[j] += pi * wj
        rank = sorted(rank.items(), key=itemgetter(1), reverse=True)
        rank_reverse = [(i[1], i[0]) for i in rank]
        return rank_reverse[0:k]

    def svd_recommend(self, person, n=5, k=5):
        rank = self.svd.recommend(int(person), k, only_unknowns=False, is_row=False)
        rank_reverse = [(i[1], i[0].encode('utf-8')) for i in rank]
        return rank_reverse

    def precision_recall(self, n=5, k=5, rec_algorithm=ucf_recommend):
        # print("n = %d, k = %d" %(n, k))
        hit = 0
        n_recall = 0
        n_precision = 0
        for person in self.remap:
            # Exclude new user in test dastaset
            if person not in self.test_set:
                continue
            # Get different tag of one user '03EF1230124124' --->  [123,124,125]
            person2id_list = self.remap[person]
            # Handle each tag recommend list
            all_rec_result = []
            tu = self.test_set[person]
            for each_tag in person2id_list:
                result = rec_algorithm(self, each_tag, n, k)
                for item in result:
                    all_rec_result.append(item[1])        
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

        recall = hit * 1.0 / n_recall
        precision = hit * 1.0 / n_precision
        # print 'Precision:\t', hit * 1.0 / n_precision
        # print 'Recall: \t', hit * 1.0 / n_recall
        return round(precision, 3), round(recall, 3)

if __name__ == '__main__':
    # Prepare train and test data
    test_file = DataSet('test_all.csv')
    svd_train_con = Data()
    svd_train_con.load('cf/onedaySet/Content/rate2.csv', force=True, sep=',', format={'col':0, 'row':1, 'value':2, 'ids':str})
    remap_con = 'cf/onedaySet/Content/remap2.csv'
    train_file_con = 'cf/onedaySet/Content/rate2.csv'
    train_prefs_con = prepare_train(train_file_con)
    test_con = make_test_dict(test_file, -1, 1)
    rec_con = Recommender(train_prefs_con, test_con, remap_con, svd_train_con)

    svd_train = Data()
    svd_train.load('cf/onedaySet/rate2.csv', force=True, sep=',', format={'col':0, 'row':1, 'value':2, 'ids':str})
    remap = 'cf/onedaySet/remap2.csv'
    train_file = 'cf/onedaySet/rate2.csv'
    train_prefs = prepare_train(train_file)
    test = make_test_dict(test_file, -1, 2)
    rec = Recommender(train_prefs, test, remap, svd_train)

    for i in range(1, 6):
        # Calculate precision recall
        a = []
        # print 'SVD CONTENT'
        pre, recall = rec_con.precision_recall(n=5, k = i, rec_algorithm=Recommender.svd_recommend)
        a.append(str(pre))
        a.append(str(recall))
        # print 'ICF CONTENT'
        pre, recall = rec_con.precision_recall(n=5, k = i, rec_algorithm=Recommender.icf_recommend)
        a.append(str(pre))
        a.append(str(recall))
        # print 'UCF CONTENT'
        pre, recall = rec_con.precision_recall(n=5, k = i, rec_algorithm=Recommender.ucf_recommend)
        a.append(str(pre))
        a.append(str(recall))
        # print 'SVD'
        pre, recall = rec.precision_recall(n=5, k = i, rec_algorithm=Recommender.svd_recommend)
        a.append(str(pre))
        a.append(str(recall))
        # print 'ICF'
        pre, recall = rec.precision_recall(n=5, k = i, rec_algorithm=Recommender.icf_recommend)
        a.append(str(pre))
        a.append(str(recall))
        # print 'UCF'
        pre, recall = rec.precision_recall(n=5, k = i, rec_algorithm=Recommender.ucf_recommend)
        a.append(str(pre))
        a.append(str(recall))

        print str(i) + ',', ','.join(a)
