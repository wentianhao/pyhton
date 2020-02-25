import pandas as pd

def check(keyword:str, line:str):
    words = line.split(" ")
    for word in words:
        if keyword == word.lower():
            return True
    return False

data = pd.read_csv('./data1.csv', encoding = 'utf-8')
keyword = input("input keyword:\n").lower()
has_result = False

for idx in range(len(data['line'])):
    if check(keyword, data['line'][idx]):
        has_result = True
        print(data['id'][idx])
if not has_result:
    print("404")
