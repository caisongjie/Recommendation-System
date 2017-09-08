import numpy
import math
import heapq
def calc_avg(rating):# user is an array of ratings
     return numpy.mean([int(x) for x in rating if x != '0'])

def calc_weight(train, rating,movies, avgtrainrating,avgrating,):# train is[][], rating is[]- size of 5,10,or 20
    weight=[]
    for i in range(len(train)):
        numerater =0.0
        denoa=0.0
        denob=0.0
        co_rated=0
        for j in range(len(rating)):
            if int(train[i][int(rating[j])-1])==0:
                continue
            numerater+= (int(rating[j])-avgrating) * (int(train[i][int(movies[j])-1])-avgtrainrating[i])
            denoa+=(int(rating[j])-avgrating)**(2)
            denob+=(int(train[i][int(rating[j])-1])-avgtrainrating[i])**(2)
            co_rated+=1
        if denob==0.0 or denoa==0.0 or co_rated==1:
            weight.append(0)
        else:
            weight.append(numerater/(math.sqrt(denoa)*math.sqrt(denob)))
    return weight

def calc_weight_iuf(train, rating,movies, avgtrainrating,avgrating,):# train is[][], rating is[]- size of 5,10,or 20
    weight=[]
    m=0
    iuf=[]
    for i in range(1000):
        for j in range(200):
            if int(train[j][i]) !=0:
                m+=1
    if m==0:
        iuf.append(0)
    else:
        iuf.append(math.log(200/m,10))
    for i in range(len(train)):
        numerater =0.0
        denoa=0.0
        denob=0.0
        train_rating=[]
        co_rated=0
        for j in range(len(rating)):
            if int(train[i][int(rating[j])-1])==0:
                continue
            numerater+= (int(rating[j])-avgrating) * (int(train[i][int(movies[j])-1])*iuf[int(movies[j])-1]-avgtrainrating[i])
            denoa+=(int(rating[j])-avgrating)**(2)
            denob+=(int(train[i][int(rating[j])-1]*iuf[int(movies[j])-1])-avgtrainrating[i])**(2)
            co_rated+=1
        if denob==0.0 or denoa==0.0 or co_rated==1:
            weight.append(0)
        else:
            weight.append(numerater/(math.sqrt(denoa)*math.sqrt(denob)))
    return weight

def calc_p(avg_rating,avg_trainrating,weightlist,train,target_movie):
    numer = 0.0
    deno = 0.0
    k_users = heapq.nlargest(50, range(len(weightlist)), weightlist.__getitem__)
    for i in range(len(k_users)):
        weight=(float(weightlist[k_users[i]]))
        if int(train[k_users[i]][int(target_movie)-1]) ==0:
            continue
        numer += (int(train[k_users[i]][int(target_movie)-1])-avg_trainrating[k_users[i]]) * weight
        deno += abs(weight)
    p = avg_rating if deno == 0.0 else avg_rating + (numer/deno)
    p = 5 if p > 5 else p = 1
    return p

def calc_p_caseAmp(avg_rating,avg_trainrating,weightlist,train,target_movie):
    numer = 0.0
    deno = 0.0
    k_users = heapq.nlargest(50, range(len(weightlist)), weightlist.__getitem__)
    for i in range(len(k_users)):
        weight=(float(weightlist[k_users[i]]))
        weight = weight * (abs(weight)**1.5)
        if int(train[k_users[i]][int(target_movie)-1]) ==0:
            continue
        numer += (int(train[k_users[i]][int(target_movie)-1])-avg_trainrating[k_users[i]]) * weight
        deno += abs(weight)
    p = avg_rating if deno == 0.0 else avg_rating + (numer/deno)
    p = 5 if p > 5 else p = 1
    return p

def calc_p_iuf(avg_rating,avg_trainrating,weightlist,train,target_movie):
    numer = 0.0
    m=0
    deno = 0.0
    k_users = heapq.nlargest(50, range(len(weightlist)), weightlist.__getitem__)
    for i in range(len(k_users)):
        if int(train[k_users[i]][int(target_movie)-1]) !=0:
            m+=1
    w = 0 if m == 0 else math.log(200/m,10)
    for i in range(len(k_users)):
        weight=(float(weightlist[k_users[i]]))
        weight = weight * (abs(weight))**2.5
        if int(train[k_users[i]][int(target_movie)-1]) ==0:
            continue
        numer += (int(train[k_users[i]][int(target_movie)-1])* w -avg_trainrating[k_users[i]]) * weight
        deno += abs(weight)
    p = avg_rating if deno == 0.0 else avg_rating + (numer/deno)
    p = 5 if p > 5 else p = 1
    return p
if __name__ == '__main__':
    #get input file and set up the matrix
    file = open("C:\\Users\\songjie\\Desktop\\train.txt","r")
    train = [line . split('\t') for line in file]
    file.close()
    file = open("C:\\Users\\songjie\\Desktop\\test5.txt","r")
    test5 = [line.split(" ") for line in file]
    file.close()
    average_testrating = []
    train_rating=[]
    average_trainrating=[calc_avg(x) for x in train]
    test_count = 5 # test count
    test_rating = []
    for i in range(len(test5)):
        counter = 0
        if int(test5[i][2])!= 0:
            test_rating.append(int(test5[i][2]))
            counter+=1
        if len(test_rating)==test_count:
            average_testrating.append(calc_avg(test_rating))
            test_rating.clear()
            counter=0
    correlation_weight=[]
    movies =[]
    avg_count = 0
    for i in range(len(test5)):
        counter=0
        if int(test5[i][2]) != 0:
            test_rating.append(int(test5[i][2]))
            movies.append(int(test5[i][1]))
            counter+=1
        if len(test_rating)==test_count:
            correlation_weight.append(calc_weight(train,test_rating,movies,average_trainrating,average_testrating[avg_count]))
            # correlation_weight.append(calc_weight_iuf(train,test_rating,movies,average_trainrating,average_testrating[avg_count]))
            test_rating.clear()
            counter=0
            avg_count+=1
    rated_movies = []
    res=[]
    user=0
    for b in range(len(test5)):
        if int(test5[b][2]) !=0:
            if len(rated_movies) == test_count:
                rated_movies.clear()
                user+=1
            rated_movies.append(int(test5[b][1]))
        elif int(test5[b][2]) ==0:
            p = calc_p(average_testrating[user],average_trainrating,correlation_weight[user],train,int(test5[b][1]))
            # p = calc_p_caseAmp(average_testrating[u], average_trainrating, correlation_weight[u], train, int(test5[b][1]))
            # p= calc_p_iuf(average_testrating[u], average_trainrating, correlation_weight[u], train, int(test5[b][1]))
            p = int(round(p))
            test5[b][2] = str(p)+ '\n'
            res.append(test5[b][0] + ' ' + test5[b][1] + ' ' + test5[b][2])
    with open("C:\\Users\\songjie\\Desktop\\result5.txt", 'w+') as f:
        for i in range(len(res)):
            f.writelines(res[i])