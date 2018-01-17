from bs4 import BeautifulSoup
import urllib
import requests
import sys

def get():
    with urllib.request.urlopen('http://db.chgk.info/random/from_2006-01-01/types1/') as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        quest = soup.find_all('div','random_question', limit = 1)
        f = quest[0].get_text()
        img = quest[0].find_all('img')
        if img:
            img = img[0].get('src')
        
    words = f.split()
    I = len(words)

    a = b = c = d = e = f = 0
    for i,word in enumerate(words):
        if word == 'Ответ:':
            b = i
        if word == 'Зачёт:':
            c = i
        if word == 'Комментарий:':
            d = i
        if word == 'Источник(и):':
            e = i
        if word == 'Автор:' or word == 'Авторы:':
            f = i
        elif word == '1:':
            a = i

    quest = ['']
    answ = ['']
    coords = [b,c,d,e,f,I]
    coords = [i for i in coords if i!=0]

    for i in range(a+1,b-1):
        quest.append(words[i])
    quest.append('\n')

#    if img:
#            quest.append(img)

    for i in range(0,len(coords)-1):
        for j in range(coords[i],coords[i+1]):
            answ.append(words[j])
        answ.append('\n')

    for i in range(0,a-1):
        answ.append(words[i])
        
    quest = (' '.join(quest))
    answ = (' '.join(answ))

#   print (quest, '\n', answ)
    return (quest, answ, img)

