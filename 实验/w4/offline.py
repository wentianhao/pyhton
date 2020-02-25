import os
import re
import json
from math import log

data = "./data"
pattern = r',|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|，|。|、|；|‘|’|【|】|·|！| |…|（|）'
print(os.getcwd())

invert = {}
N = len(os.listdir(data))

for file in os.listdir(data):
    with open(os.getcwd() + "./data/"+file) as f:
        for line in f.readlines():
            words = re.split('[ ,.]',line)
            for word in words:
                word = word.lower()
                if word == "":
                    continue
                if word not in invert:
                    invert[word] = {str(file):1}
                elif str(file) not in invert[word]:
                    invert[word][str(file)] = 1
                else:
                    invert[word][str(file)] = invert[word][str(file)] + 1
                
with open("./invertDict","w") as f:
    print(invert)
    f.write(json.dumps(invert))

print(f"N = {N}")
for word in invert:
    idf = log(N / (len(invert[word])+1))
    termTotal = 0
    for doc in invert[word]:
        termTotal = termTotal + invert[word][doc]
    for doc in invert[word]:
        termThis = invert[word][doc]
        tf = termThis / termTotal
        print(f"word = {word}, doc= {doc}, tf={tf},idf={idf}")
        invert[word][doc] = tf * idf

with open("./tf-idf","w") as f:
    print(invert)
    f.write(json.dumps(invert))

