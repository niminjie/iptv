
def main():
    fo = open('test_rand1.csv', 'w')
    user_list = []
    for line in open('randUser/remap1.csv'):
        user_id = line.split(',')[0]
        if user_id not in user_list:
            user_list.append(user_id)

    for line in open('../test_all.csv'):
        user_id = line.split(',')[-1].strip()
        if user_id in user_list:
            fo.write(line)

if __name__ == '__main__':
    main()
