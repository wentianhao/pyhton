import os
import re
import json

data = "./data"
pattern = r',|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|，|。|、|；|‘|’|【|】|·|！| |…|（|）'
print(os.getcwd())

invert = {}

for file in os.listdir(data):
    with open(os.getcwd() + "./data/"+file) as f:
        for line in f.readlines():
            words = re.split('[ ,.]',line)
            for word in words:
                word = word.lower()
                if word not in invert:
                    invert[word] = [1,[file]]
                else:
                    if file not in invert[word][1]:
                        invert[word][0] = invert[word][0] + 1
                        invert[word][1].append(file)

with open("./invertDict","w") as f:
    print(invert)
    f.write(json.dumps(invert))
    



