import json
import re
import os
from functools import reduce

def docID(item:str)->int:
    return int(item.replace("d",""))

def intersect(L1, L2):
    answer = []
    len1,len2 = len(L1),len(L2)
    p1,p2 = 0,0
    while p1 < len1 and p2 < len2:
        print(f"p1={p1},p2={p2},L1[p1]={L1[p1]},L2[p2]={L2[p2]}, docID(L1[p1]) = {docID(L1[p1])},docID(L2[p2])={docID(L2[p2])}")
        if docID(L1[p1]) == docID(L2[p2]):
            answer.append(L1[p1])
            p1 = p1 + 1
            p2 = p2 + 1
        elif docID(L1[p1]) < docID(L2[p2]): 
            p1 = p1 + 1
        else:
            p2 = p2 + 1
    return answer


def jaccard_coefficient(A,B):
    A,B = set(A),set(B)
    return len(A & B) / len(A | B)


def file2list(filename):
    with open(os.getcwd() + "./data/"+filename) as f:
        for line in f.readlines():
            words = re.split('[ ,.]',line)
            words.remove("")
    return words


def calc(invert, words, resultSet):
    values = []
    for item in resultSet:
        value = 0
        for word in words:
            if word in invert and item in invert[word]:
                value = value + invert[word][item]
        values.append((item,value))
    return values


# 加载离线计算的数据
invert = {}
with open("./tf-idf") as f:
    invert  = json.loads(f.readline())

while True:
    words = input("input keyword:").split()
    print(f"words are {words}")
    
    resultSet = []
    for word in words:
        word = word.lower()
        if word in invert:
            resultSet.append(set(invert[word].keys()))
        # else:
        #     print(f"{word} is not in dict")
    print(f"resultSet are {resultSet}")
    if len(resultSet) == 0:
        print("Empty Result")
    else:
        resultSet = reduce(lambda x, y: x|y,resultSet)
        print(f"result is {resultSet}")

        value_list = calc(invert,words,resultSet)
        print(value_list)
        print(f"sorted list is {sorted(value_list,key = lambda item: item[1],reverse=True)}")

