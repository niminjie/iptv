import re
import datetime
from decimal import Decimal
from math import sqrt

#filename = raw_input("Please input a file path\n").strip()
#filename = r"/Users/niminjie/recomWorkspace/utest.base"
#testFile = r"/Users/niminjie/recomWorkspace/utest.test"

# filename = r"train_rate.csv"
# testFile = r"u1.test"
# 
# outputFileName_cosine = r"similarity_cosine.txt"
# outputFileName_distance = r"similarity_distance.txt"
# outputFileName_pearson = r"similarity_pearson.txt"
# 
# outputRAndP_cosine = r"RandP_cosine.txt"
# outputRAndP_distance = r"RandP_distance.txt"
# outputRAndP_pearson = r"RandP_pearson.txt"
# 
# inputSimFile_cosine = r"similarity_cosine.txt"
# inputSimFile_distance = r"similarity_distance.txt"
# inputSimFile_pearson = r"similarity_pearson.txt"

#testFile = r"/Users/niminjie/recomWorkspace/sample.txt"
#filename = r"/Users/niminjie/recomWorkspace/sampletest.txt"

# f = open(filename, 'r')
# f2 = open(testFile, 'r')
# fRAndP_cosine = open(outputRAndP_cosine,'w')
# fRAndP_distance = open(outputRAndP_distance,'w')
# fRAndP_pearson = open(outputRAndP_pearson,'w')

allWords = []
prefs = {}
transPrefs = {}
filterKeys = {}
testPrefs = {}
sims = {}
userSims_cosine = {}
userSims_distance = {}
userSims_pearson = {}

def prepareData(prefs, f) :
    line = f.readline().strip()
    while 1:
        if not line:
            break
        line_split = line.split(',')
        if not line_split[0] in prefs:
            prefs[line_split[0]] = {line_split[1]:float(line_split[2])}
        else: 
            prefs[line_split[0]][line_split[1]] = float(line_split[2])
        line = f.readline().strip()

def transformPrefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})
            result[item][person] = prefs[person][item]
    return result

def filterKey():
    for item in transPrefs:
        if len(transPrefs[item]) <= 50:
            filterKeys[item] = 1

def sim_distance(prefs, p1, p2):
    si = {} 
    for item in prefs[p1]:
        if item in prefs[p2]: si[item] = 1 
    if len(si) == 0: return 0
    sum_of_squares = sum([pow(prefs[p1][item] - prefs[p2][item], 2) 
                        for item in prefs[p1] if item in prefs[p2]]) 
    return 1 / (1 + sqrt(sum_of_squares))

def sim_pearson(prefs, p1, p2):
    si = {} 
    for item in prefs[p1]:
        if item in prefs[p2]: si[item] = 1 
    if len(si) == 0: return 0

    n = len(si) 
    sum1 = float(sum([prefs[p1][it] for it in si]))
    sum2 = float(sum([prefs[p2][it] for it in si]))
    sum1Sq = float(sum([pow(prefs[p1][it], 2) for it in si]))
    sum2Sq = float(sum([pow(prefs[p2][it], 2) for it in si]))
    pSum = float(sum([prefs[p1][it] * prefs[p2][it] for it in si]))
    num = float(pSum - (sum1 * sum2 / n))
    den = float(sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n)))
    if den == 0: return 0 
    r = num / den
    return r


def sim_cosine(prefs, p1, p2):
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

def calSimilarity(prefs,fileName,similarity = sim_cosine):
    myfile = open(fileName,'w') 
    for person in prefs:
        for other in prefs:
            if person == other: continue
            myfile.write('%s,%s,%f\r\n'%(person,other,float(similarity(prefs,person,other))))
            myfile.flush()
    myfile.close()

def getSimFromFile(f,userSims):
    line = f.readline().strip()
    while 1:
        if not line:
            break
        line_split = line.split(',')
        userSims.setdefault(line_split[0],{})
        userSims[line_split[0]][line_split[1]] = float(line_split[2])
        line = f.readline().strip()

def topMatches_online(prefs, person, n = 100):
    scores=[(sim_cosine(prefs, person, other), other) for other in prefs if other != person] 
    scores.sort() 
    scores.reverse() 
    cnt = 0
    return scores[0:n]

def topMatches(prefs, person, n = 5, similarity = sim_cosine):
    if similarity == sim_cosine :
        scores=[(userSims_cosine[person][other], other) for other in prefs if other != person] 
    elif similarity == sim_distance:
        scores=[(userSims_distance[person][other], other) for other in prefs if other != person] 
    else:
        scores=[(userSims_pearson[person][other], other) for other in prefs if other != person] 
    scores.sort() 
    scores.reverse() 
    return scores[0:n]

def getRecommendations(prefs, person, n = 100, k = 5, similarity = sim_cosine):
    totals = {}
    simSums = {}

    sims = topMatches_online(prefs, person, n) 
    #print("Neigh: " +str(sims) + "Person: " + person)
    for item in sims:
        other = item[1]
        for i in prefs[other]:
            if i not in filterKeys:
                # if i not in prefs[person] or prefs[person][i] == 0 :
                totals.setdefault(i,0)
                #totals[i] = Decimal('0')
                totals[i] += prefs[other][i] * item[0]
                simSums.setdefault(i,0)
                simSums[i] += item[0]

    rankings = []
    for item,total in totals.items():
        if simSums[item] == 0 : continue
        #print("Person: %s, Total :%f , simSum :%f, Item: %s" %(person, total, simSums[item], item))
        #rankings.append((Decimal(str(total)) / Decimal(str(simSums[item])), item))
        rankings.append([total / simSums[item], item])
    rankings.sort()
    rankings.reverse()
    #print(rankings[0:k])
    if k == 0:
        return rankings
    # return rankings[0:k]
    return rankings

def calRecallandPrecision(foutput,prefs, n = 100,k = 50, similarity = sim_cosine):
    print("n = %d,k = %d" %(n, k))
    idx = 0
    hit = 0
    n_recall = 0
    n_precision = 0
    for person in prefs.keys():
        if idx > 100:
            break
        print 'Now Processing person:', person
        if person not in testPrefs:
            continue
        idx += 1
        tu = testPrefs[person]
        for item in tu:
            print item
        result = getRecommendations(prefs, person, n, k, similarity)
        print '-' * 100
        for pui, item in result:
            print item
            if item in tu:
                hit += 1
        n_recall += len(tu)
        if k > len(result):
            n_precision += len(result)
        else:
            n_precision += k
        print '*' * 100
    print "Hit : ", str(hit)
    print n_recall, n_precision
    # foutput.write('%d,%d,%d,%f,%f,%f,%f \r\n' %(hit,n,k,hit / (n_recall * 1.0),hit / (n_precision * 1.0),calRMSE(prefs,n,k,similarity),calMAE(prefs,n,k,similarity)))
    # foutput.flush()
    # print( "Cosine " + "Recall is :" + str(hit / (n_recall * 1.0)) + "  Precision is :" + str(hit / (n_precision * 1.0)))
    #return [hit / (n_recall * 1.0),hit / (n_precision * 1.0)]

def calRMSE(prefs,n,k,similarity = sim_cosine):
    result = []
    N = 0
    sums = 0
    for person in prefs.keys():
        if person not in testPrefs:
            continue
        tu = testPrefs[person]
        result = getRecommendations(prefs, person,n ,0, similarity)
        for pui, item in result:
            if item in tu:
                sums += (pui - tu[item]) * (pui - tu[item])
                N += 1
    return (sqrt(sums) / N)

def calMAE(prefs,n,k, similarity = sim_cosine):
    result = []
    sums = 0
    N = 0
    for person in testPrefs:
        if person not in prefs:
            continue
        tu = prefs[person]
        result = getRecommendations(prefs, person,n ,0, similarity)
        for pui, item in result:
            sums += abs(pui - tu[item])
            N += len(testPrefs[person])
    return (sums / N)

#    for person in prefs.keys():
#        if person not in testPrefs:
#            continue
#        tu = testPrefs[person]
#        result = getRecommendations(prefs, person,n ,0, similarity)
#        for pui, item in result:
#            if item in tu:
#                sums += abs(pui - tu[item]) 
#                N += 1
#    return (sums / N)

#def calRMSE(prefs,n,k,similarity = sim_cosine):
#    return 1
#
#def calMAE(prefs,n,k, similarity = sim_cosine):
#    return 1


prepareData(prefs,open('train_rate.csv'))
prepareData(testPrefs, open('train_rate.csv'))
# print getRecommendations(prefs, '1', n=10)
# calRecallandPrecision(open('pre.out', 'w'), prefs,n=10,k=2)
# for item in  getRecommendations(prefs, '1', n=10):
#     print item[1]

# transPrefs = transformPrefs(prefs)
# filterKey()
#calRecallandPrecision(prefs, 80, 10, sim_pearson)

# for n in range(80,100):
#     for k in range(80,100):
#         calRecallandPrecision(fRAndP_cosine,prefs, n, k, sim_cosine)
# fRAndP_cosine.close()
# 
# for n in range(1,100):
#     for k in range(1,100):
#         calRecallandPrecision(fRAndP_pearson,prefs, n, k, sim_pearson)
# fRAndP_pearson.close()
# 
# for n in range(1,100):
#     for k in range(1,100):
#         calRecallandPrecision(fRAndP_distance,prefs, n, k, sim_distance)
# fRAndP_distance.close()

#calRecallandPrecision(prefs, 80, 10 ,sim_cosine)
#calRecallandPrecision(prefs, 2, 2, sim_distance)

#print(calRMSE(prefs,10,90,sim_pearson))
#print(calMAE(prefs,10 ,90,sim_pearson))

#print(sims)
#print(sims['1']['100'])

#rankins = getRecommendations(prefs,'1',50,sim_cosine)
#print(rankins)
#print("-----------------------------------------------------")

#scores_cosine = topMatches(prefs, '1', 10, sim_cosine)

# print(prefs['1']['270'])
