from DataSet import DataSet
from MakeDict import *
from TimeSpliter import TimeSpliter
import myPickle

def generate_interval():
    train = DataSet('train_all.csv')
    columns = ['id','content_id','class_name','start','end','timespan','user_id']
    user_dict = to_dict_byUser(train, columns, -1)
    timespliter = TimeSpliter(user_dict)
    time_tag = timespliter.tag_all_user()
    myPickle.save(time_tag, 'user_time_all.pkl')

def main():
    time_tag = myPickle.load('user_time_all.pkl')

if __name__ == '__main__':
    main()
