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
    train.load('./randUser/rate1.csv', force=True, sep=',', format={'col':0, 'row':1, 'value':2, 'ids':str})
    svd.set_data(train)
    svd.compute(k=5, min_values=0, pre_normalize=None, mean_center=False, post_normalize=True)
    rec_list = svd.recommend(200, n=5, only_unknowns=False, is_row=False)
    print svd.recommend(1, n=5, only_unknowns=False, is_row=False)
    print svd.recommend(2, n=5, only_unknowns=False, is_row=False)
    print svd.recommend(3, n=5, only_unknowns=False, is_row=False)
    print svd.recommend(4, n=5, only_unknowns=False, is_row=False)
    print svd.recommend(5, n=5, only_unknowns=False, is_row=False)
    print svd.recommend(6, n=5, only_unknowns=False, is_row=False)
    print svd.recommend(7, n=5, only_unknowns=False, is_row=False)
    print svd.recommend(8, n=5, only_unknowns=False, is_row=False)
    print svd.recommend(9, n=5, only_unknowns=False, is_row=False)

if __name__ == '__main__':
    main()
