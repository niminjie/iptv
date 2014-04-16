import sys

def file2dict(fi):
    user_dict = {}
    for line in open(fi):
        id, content_id, class_name, start, end, timespan, user_id = line.split(',')
        user_id = user_id.strip()
        user_dict.setdefault(user_id, [])
        if class_name not in user_dict[user_id]:
            user_dict[user_id].append(class_name)
    return user_dict

if __name__ == '__main__':
    user_dict = file2dict(sys.argv[1])
    for item in user_dict['00034C847ADC']:
        print item
