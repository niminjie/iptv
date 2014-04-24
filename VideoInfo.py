import myPickle
'''
V0001008060161,2659
V0001008060159,2615
V0001008060162,2688
V0001008060163,2666
V0001008060165,2608
V0001008060166,2672
V0001008100071,2627
V0001008100072,2642
V1401003030026,2767
'''
def main():
    i = 0
    during_dict = {}
    for line in open('VideoInfo.csv', 'r'):
        if i <= 2:
            i += 1
            continue

        if len(line.split(',')) < 26:
            continue

        content_name = line.split(',')[1]
        during = line.split(',')[8]
        during_dict.setdefault(content_name, during)
    during_dict['V0001008060161'] = 2659
    during_dict['V0001008060159'] = 2615
    during_dict['V0001008060162'] = 2688
    during_dict['V0001008060163'] = 2666
    during_dict['V0001008060165'] = 2608
    during_dict['V0001008060166'] = 2672
    during_dict['V0001008100071'] = 2627
    during_dict['V0001008100072'] = 2642
    during_dict['V1401003030026'] = 2767
    myPickle.save(during_dict, 'video.pkl')
    # for key, value in during_dict.items():
    #     print value
    # during_dict = myPickle.load('video.pkl')
    # print during_dict

if __name__ == '__main__':
    main()
