from bs4 import BeautifulSoup
import urllib
import requests
import sys

def get(year1, year2):
    url = 'http://db.chgk.info/random/from_'+year1+'-01-01/to_'+year2+'-12-31/types1/'
    with urllib.request.urlopen(url) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        question = soup.find_all('div','random_question', limit = 1)
        answer = question[0].find('div','collapsible collapsed')
        razdatka = question[0].find('div','razdatka')
        q = question[0].get_text()
        if razdatka:
            razdatka = question[0].find('div','razdatka').extract()
            r = razdatka.get_text()
        img_q = question[0].find_all('img')
        img_a = answer.find_all('img')
        if img_q:
            if len(img_q)==len(img_a):
                img_q = []
            elif len(img_q)>len(img_a):
                img_q[:len(img_q)-len(img_a)]
        if img_q:
            img_q = img_q[0].get('src')
        if img_a:
            img_a = img_a[0].get('src')

    quest = ['']
    answ = ['']
            
    words = q.split()

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

    coords = [b,c,d,e,f,len(words)]
    coords = [i for i in coords if i!=0]

    if razdatka:
        quest.append(r)
        quest.append('\n')
        
    for i in range(a+1,b-1):
        quest.append(words[i])
    quest.append('\n')
    
    for i in range(0,len(coords)-1):
        for j in range(coords[i],coords[i+1]):
            answ.append(words[j])
        answ.append('\n')

    for i in range(0,a-1):
        answ.append(words[i])
    answ.append('\nВыбранный диапазон лет: '+year1+'...'+year2+'\n')

    quest = (' '.join(quest)).replace(" \n ", "\n")
    answ = (' '.join(answ)).replace(" \n ", "\n")

    return (quest, answ, img_q, img_a)
#print (quest,'\n',answ,'\n',img_q,'\n',img_a)




