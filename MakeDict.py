from DataSet import DataSet

def to_dict_byUser(data, columns, user_id_idx):
    '''
    Args:
        data:     contains many tuple ('user_id','content_id', ...)
        colums:   ['id', 'content_id', 'start_time', 'endtime', 'user_id', ...]
    Returns:
        UserDict: {'1':[{'class_name':'1',...},{'class_name':'2',...}]}
    '''
    arr_idx = {}
    user_dict = {}
    for idx, value in enumerate(columns):
        arr_idx[value] = idx
    for line in data.getData():
        user_id = line[user_id_idx]
        user_dict.setdefault(user_id, [])
        arr = {}
        for key in arr_idx:
            if key == 'user_id':
                continue
            arr[key] = line[arr_idx[key]]
        user_dict[user_id].append(arr)
    return user_dict

def make_test_dict(data, user_idx, class_idx):
    '''
    Args:
        data:      Contains many tuple ('user_id','content_id', ...)
        user_idx:  User index in column(tuple)
        class_idx: Class name index in column(tuple)
    Returns:
        TestDict:  {'1':['class1','class2',...],...}
    '''
    user_dict = {}
    for line in data.getData():
        user_id = line[user_idx]
        user_dict.setdefault(user_id, [])
        class_name = line[class_idx]
        if class_name not in user_dict[user_id]:
            user_dict[user_id].append(class_name)
    return user_dict

# train = DataSet('train_all.csv')
# columns = ['id','content_id','class_name','start','end','timespan','user_id']
# user_dict = to_dict_byUser(train, columns, -1)
# 
# test = DataSet('test_all.csv')
# test_dict = make_test_dict(test, -1, 2)
# print test_dict['00034C975729']
