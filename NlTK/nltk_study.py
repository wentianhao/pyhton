import nltk
# from nltk.book import *
# nltk.download()

# 查找白鲸记中的词 monstrous
# text1.concordance("monstrous")

# nltk.book.babelize_shell()
# nltk.chat.chatbots()
data = nltk.corpus.gutenberg.fileids()
print(data)
emma = nltk.Text(nltk.corpus.gutenberg.words('austen-emma.txt'))
print(len(emma))
emma.concordance("surprize")
