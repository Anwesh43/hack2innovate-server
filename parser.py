# imports
import numpy as np
import pandas as pd
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.corpus import stopwords

# libraries and lists
debit_interest = ['debit','debited','paid','payment','spend','spent','expense','purchase','payment']
credit_interest = ['credited', 'credit', 'reversed', 'reverse', 'credited/reversed','recieved','recieve','sent','send']
currency = list(set([c.lower() for c in pd.read_csv("/Users/yjaiswal/Downloads/country-code-to-currency-code-mapping.csv")['Code']]))
currency.pop(currency.index("mad"))
currency.append("rs")
stop_words = set(stopwords.words('english'))
acList = ["ac", "account", "account/no","a/c","acct"]

# utility function
def getCurrency(sentences,currency):
    for s in sentences:
        for c in currency:
            if(c in s):
                return c


def parseAmt(sentences,i,cur):
    amt = 0
    prev = sentences[0:i]
    nxt = sentences[i+1:len(sentences)]
    for p in prev:
        print(p)
        if(pos_tag([p])[0][1] == 'CD'):
            amt = p
            return amt
        elif(cur in p):
            amt = p
            return amt
    if(amt == 0):
        for n in nxt:
            if(cur in n):
                amt = n
                return amt
            elif(pos_tag([n])[0][1] == 'CD'):
                amt = (n)
                return amt
    return amt

def parseCardNumber(sentence):
    for s in sentence:
        if(pos_tag(s)[0][1] == "CD" and len(s) == 4):
            return s
        elif("xx" in s):
            return s


def parseSentence(st,currency):
    sentences = [w.lower() for w in word_tokenize(st) if w not in stop_words]
    amt = 0
    typ = ""
    card = None
    ac = None
    #currency = getCurrency(sentences,currency)
    for i in range(0,len(sentences)):
        if(card == None and sentences[i] == 'card'):
            card = parseCardNumber(sentences[i+1:len(sentences)])
        if(ac == None and sentences[i] in acList):
            ac = parseCardNumber(sentences[i+1:len(sentences)])
        if(typ != 'credit' and sentences[i] in debit_interest and sentences[i+1] != 'card'):
            print(sentences[i])
            typ = "debit"
            amt = parseAmt(sentences,i,currency)
        elif(typ != 'debit' and sentences[i] in credit_interest and sentences[i+1] != 'card'):
            print(sentences[i])
            typ = "credit"
            amt = parseAmt(sentences,i,currency)
    return amt,typ,currency,card,ac
