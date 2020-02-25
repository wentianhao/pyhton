import json
from functools import reduce

invert = {}
with open("./invertDict") as f:
    invert  = json.loads(f.readline())



while True:
    words = input("input keyword:").split()
    print(f"words are {words}")
    resultSet = []
    for word in words:
        if word in invert:
            resultSet.append(set(invert[word][1]))
        else:
            print(f"{word} is not in dict")
    if len(resultSet) == 0:
        print("Empty Result")
    else:
        print(f"result is {reduce(lambda x, y: x&y,resultSet)}")

