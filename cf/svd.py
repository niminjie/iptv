import recsys.algorithm
recsys.algorithm.VERBOSE = True
from recsys.algorithm.factorize import SVD
from recsys.datamodel.data import Data
from recsys.evaluation.decision import PrecisionRecallF1
from recsys.evaluation.prediction import RMSE, MAE
from recsys.datamodel.item import Item
from recsys.datamodel.user import User
import sys

def main():
    svd = SVD()
    train = Data()
    test = Data()
    train.load('randUser/rate1.csv', force=True, sep=',', format={'col':0, 'row':1, 'value':2, 'ids':int})
    test.load('randUser/rate1.csv', force=True, sep=',', format={'col':0, 'row':1, 'value':2, 'ids':int})
    svd.set_data(train)
    svd.compute(k=100, min_values=0.5, pre_normalize=False, mean_center=True, post_normalize=True)

    # rmse = RMSE()
    # mae = MAE()
    # for rating, item_id, user_id in test.get():
    #     try:
    #         pred_rating = svd.predict(item_id, user_id)
    #         rmse.add(rating, pred_rating)
    #         mae.add(rating, pred_rating)
    #     except KeyError:
    #         continue
    # print 'RMSE=%s' % rmse.compute()
    # print 'MAE=%s' % mae.compute()

    # test = make_test()
    # print precision_and_recall(test, svd)
    # rec_list = svd.recommend(200, n=5, only_unknowns=False, is_row=False)
    print svd.recommend(1, n=5, only_unknowns=False, is_row=False)

    # print svd.recommend(2, n=5, only_unknowns=False, is_row=False)
    # print svd.recommend(3, n=5, only_unknowns=False, is_row=False)
    # print svd.recommend(4, n=5, only_unknowns=False, is_row=False)
    # print svd.recommend(5, n=5, only_unknowns=False, is_row=False)
    # print svd.recommend(6, n=5, only_unknowns=False, is_row=False)
    # print svd.recommend(7, n=5, only_unknowns=False, is_row=False)
    # print svd.recommend(8, n=5, only_unknowns=False, is_row=False)
    # print svd.recommend(9, n=5, only_unknowns=False, is_row=False)

def make_test():
    test = {}
    for line in open('u1.test'):
        user_id, item_id, rate, _ = line.split('\t')
        test.setdefault(user_id, [])
        test[user_id].append(item_id)
    return test

def precision_and_recall(test, svd):
    hit = 0
    n_recall = 0
    n_precision = 0

    for user_id, play in test.items():
        try:
            rec = svd.recommend(int(user_id), n=5, only_unknowns=True, is_row=False)
            if 5 > len(rec):
                n_precision += len(rec)
            else:
                n_precision += 5
            for item in rec:
                if str(item[0]) in play:
                    hit += 1
            n_recall += len(play)
        except KeyError:
            continue
    recall = hit * 1.0 / n_recall
    precision = hit * 1.0 / n_precision
    return precision, recall

if __name__ == '__main__':
    main()
