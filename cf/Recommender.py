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

class Recommender():
    def __init__(self):
        pass

    def precision_recall(self):
        pass

    def recommend(self):
        pass

    def _sim_cosine(prefs, p1, p2):
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

    def _topMatches(prefs, person, n=100):
        scores=[(sim_cosine(prefs, person, other), other) for other in prefs if other != person] 
        scores.sort() 
        scores.reverse() 
        cnt = 0
        return scores[0:n]

    def _itemSim(train):
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
        return W
