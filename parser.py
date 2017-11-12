# imports
import numpy as np
import pandas as pd
from utils import get_currency
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.corpus import stopwords

# libraries and lists
debit_interest = ['debit','debited','paid','payment','spend','spent','expense','purchase','payment']
credit_interest = ['credited', 'credit', 'reversed', 'reverse', 'credited/reversed','recieved','recieve','sent','send']
currency = get_currency()
stop_words = set(stopwords.words('english'))
acList = ["ac", "account", "account/no","a/c","acct"]
genericList = ["hdfc","icici","sbi","kotak","credit","debit","mahindra","bank","card","axis","citi","hsbc","vijaya","obc","oriental","curr","ac", "account", "account/no","a/c","o/s","acct","credit","card","jun","jul","jan","feb","mar","apr","may","aug","sept","oct","nov","dec","today","tomorrow","dear","customer","balance","bal","info","bil","your","vps","imps","ips","cash","cashback","cashbck"]
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

def extractCategory(cat):
    food=["mcdonals","pizza","burger","food","dinner","restaurant","cart","cafe","coffee","breakfast","lunch","buffet","anand","adyar","dominos"]
    travel=["ola","uber","taxi","lyft","taxi","car","zoomcar","hire","rental","makemytrip","airbnb","goibibo","airlines","travels","travelling","tours","airways","fly","auto"]
    shopping=["amazon","flipkart","myntara","snapdeal","myntra","shopping","store","walmart","hypercity","enterprise","mall","store","market","supermarket","sports","super","more","reliance","fresh","dmart","village"]
    payments=["emi","payment","home","loan","tax","house",]
    mobile = ["paytm","recharge","airtel","vodafone","bsnl","mobile","internet","broadband","tariff","topup","broadband","freecharge","mobikwik"]
    expenses=["expense","deduction","monthly","gas","water","electricty"]
    entertainment = ["pvr","movie","inox","cinema","play","tv","bookmyshow"]
    health =["healthcare","health","doctor","hlth","medical","pharmacy","medicine","dental","dentist","health center","chemist","chemi","druggist","hospital","institute","trauma","heart"]
    for h in health:
        if(h in cat):
            return "Healthcare expenses"
    for f in food:
        if(f in cat):
            return "Eating Out"
    for t in travel:
        if(t in cat):
            return "Travel and Accomodation"
    for s in shopping:
        if(s in cat):
            return "Purchases and Shopping"
    for m in mobile:
        if(m in cat):
            return "Mobile and Broadband"
    for e in expenses:
        if(e in cat):
            return "Expenses and Withdrawls"
    for p in payments:
        if(p in cat):
            return "Loan EMIs and Payments"
    for ent in entertainment:
        if(ent in cat):
            return "Entertainment"
    return "Other"


def parseSentence(st,currency):
    # basic text cleaning
    # remove "*" char
    st = st.replace("*"," ")
    st = st.replace(":"," ")
    from textblob import TextBlob
    blob = TextBlob(st)
    sentence = blob.sentences
    phrases = []
    for sen in sentence:
        phrases.append(blob.noun_phrases)
    amt = 0
    typ = ""
    card = None
    ac = None
    sentences = [w.lower() for w in word_tokenize(st) if w not in stop_words]
    currency = getCurrency(sentences,currency)
    cat = ""
    for i in range(0,len(sentences)):
        if(card == None and sentences[i] == 'card'):
            card = parseCardNumber(sentences[i+1:len(sentences)])
        if(ac == None and sentences[i] in acList):
            ac = parseCardNumber(sentences[i+1:len(sentences)])
        if(typ != 'credit' and sentences[i] in debit_interest and sentences[i+1] != 'card'):
            typ = "debit"
            amt = parseAmt(sentences,i,currency)
        elif(typ != 'debit' and sentences[i] in credit_interest and sentences[i+1] != 'card'):
            typ = "credit"
            amt = parseAmt(sentences,i,currency)

    for phrase in phrases[0]:
        for w in genericList:
            if(w in phrase):
                phrase = str(phrase).replace(w,"")
        if(phrase != "" and currency not in phrase and pos_tag([phrase])[0][1] != "CD" and phrase not in cat and "xx" not in phrase):
            cat = cat + " " + phrase + " "
    cat = cat.replace(".avl", "").strip()
    return amt,typ,currency,card,ac,extractCategory(cat)
print(get_currency())
