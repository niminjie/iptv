import myPickle
def main():
    # i = 0
    # during_dict = {}
    # for line in open('VideoInfo.csv', 'r'):
    #     if i <= 2:
    #         i += 1
    #         continue

    #     if len(line.split(',')) < 26:
    #         continue

    #     content_name = line.split(',')[1]
    #     during = line.split(',')[8]
    #     during_dict.setdefault(content_name, during)
    # # for key, value in during_dict.items():
    # #     print value
    # myPickle.save(during_dict, 'video.pkl')
    during_dict = myPickle.load('video.pkl')
    print during_dict

if __name__ == '__main__':
    main()
