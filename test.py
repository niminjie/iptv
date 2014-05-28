from DataSet import DataSet
from MakeDict import *
from TimeSpliter import TimeSpliter
import myPickle

def generate_interval():
    train = DataSet('cf/Test/test_rand1.csv')
    columns = ['id','content_id','class_name','start','end','timespan','user_id']
    user_dict = to_dict_byUser(train, columns, -1)
    timespliter = TimeSpliter(user_dict)
    time_tag = timespliter.tag_all_user()
    myPickle.save(time_tag, 'test_user_time_all.pkl')

def main():
    # generate_interval()
    time_tag = myPickle.load('test_user_time_all.pkl')
    print time_tag

if __name__ == '__main__':

    main()
