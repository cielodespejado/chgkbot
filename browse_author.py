from bs4 import BeautifulSoup
import urllib
import requests
import sys
import random

def get(author, year1, year2):
    quest = ['']
    answ = ['']
    image_q = []
    image_a = []
    url = 'https://db.chgk.info/search/questions/author_'+author+'/types1/sort_date/from_'+year1+'-01-01/to_'+year2+'-12-31/limit10000'
    with urllib.request.urlopen(url) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        allquests = soup.find_all('div','question')
        tournaments = soup.find_all('dt','title')
        N = random.randint(0,len(allquests)-1)
        tournament = tournaments[N].get_text()
        razdatka = allquests[N].find('div','razdatka')
        if razdatka:
            razdatka = allquests[N].find('div','razdatka').extract()
            r = razdatka.get_text()
        question = allquests[N].get_text()    
        soup1 = BeautifulSoup(str(allquests[N]), 'html.parser')
        img_q = soup1.find('strong','Answer').find_all_previous('img')
        img_a = soup1.find('strong','Answer').find_all_next('img')
        if img_q:
            for i in range(0,len(img_q)):
                image_q.append(img_q[i].get('src'))
        if img_a:
            for i in range(0,len(img_q)):
                image_a.append(img_a[i].get('src'))    

    words = question.split()

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
        elif word == 'Вопрос':
            a = i

    coords = [b,c,d,e,f,len(words)]
    coords = [i for i in coords if i!=0]

    if razdatka:
        quest.append(r)
        quest.append('\n')
        
    for i in range(a+2,b-1):
        quest.append(words[i])
    quest.append('\n')
    
    for i in range(0,len(coords)-1):
        for j in range(coords[i],coords[i+1]):
            answ.append(words[j])
        answ.append('\n')

    answ.append(tournament)
    answ.append('\nВыбранный диапазон лет: '+year1+'...'+year2+'\n')

       
    quest = (' '.join(quest)).replace(" \n ", "\n")
    answ = (' '.join(answ)).replace(" \n ", "\n")
     

    return (quest, answ, image_q, image_a)

