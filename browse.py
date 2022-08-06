from bs4 import BeautifulSoup
import urllib
import requests
import sys
import random

def get(year1, year2):
	
    quest = ['']
    answ = ['']
    img_q = []
    img_a = []
    url = 'http://db.chgk.info/random/from_'+year1+'-01-01/to_'+year2+'-12-31/types1/'
    print(url)
    try:
        with urllib.request.urlopen(url) as fp:
            soup = BeautifulSoup(fp, 'html.parser')
            question = soup.find_all('div','random_question', limit = 1)
            answer = question[0].find('div','collapsible collapsed')
            razdatka = question[0].find('div','razdatka')
            if razdatka:
                razdatka = question[0].find('div','razdatka').extract()
                r = razdatka.get_text()
            q = question[0].get_text()
            img_question = question[0].find_all(src=True)
            img_answer = answer.find_all(src=True)
            if img_question:
                if len(img_question)==len(img_answer):
                    img_question = []
                elif len(img_question)>len(img_answer):
                    img_question = img_question[:len(img_question)-len(img_answer)]
            if img_question:
                for n in img_question:
                    m = n.get('src')
                    img_q.append(m)
            if img_answer:
                for n in img_answer:
                    m = n.get('src')
                    img_a.append(m)
	except HTTPError as e:
	    break

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
    quest = (' '.join(quest)).replace(' \n ', '\n')
    answ = (' '.join(answ)).replace(' \n ', '\n')
    return (quest, answ, img_q, img_a)


def get_author(author, year1, year2):
    quest = ['']
    answ = ['']
    img_q = []
    img_a = []
    url = 'https://db.chgk.info/search/questions/author_'+author+'/types1/sort_date/from_'+year1+'-01-01/to_'+year2+'-12-31/limit10000'
    print(url)
	try:		
            with urllib.request.urlopen(url) as fp:
                soup = BeautifulSoup(fp, 'html.parser')
		allquests = soup.find_all('div','question')
        	tournaments = soup.find_all('dt','title')
	except HTTPError as e:
	    break
    if len(allquests)>0:
        N = random.randint(0,len(allquests)-1)
        tournament = tournaments[N].get_text()
        razdatka = allquests[N].find('div','razdatka')
        if razdatka:
            razdatka = allquests[N].find('div','razdatka').extract()
            r = razdatka.get_text()
        question = allquests[N].get_text()    
        soup1 = BeautifulSoup(str(allquests[N]), 'html.parser')
        img_question = soup1.find('strong','Answer').find_all_previous(src=True)
        img_answer = soup1.find('strong','Answer').find_all_next(src=True)
        if img_question:
            for n in img_question:
                m = n.get('src')
                img_q.append(m)
        if img_answer:
            for n in img_answer:
                m = n.get('src')
                img_a.append(m)

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

        coords = [b,c,d,e,f,len(words)-1]
        coords = [i for i in coords if i!=0]

        if razdatka:
            quest.append(r)
            quest.append('\n')
            
        for i in range(a+2,b):
            quest.append(words[i])
        quest.append('\n')
        
        for i in range(0,len(coords)-1):
            for j in range(coords[i],coords[i+1]):
                answ.append(words[j])
            answ.append('\n')
        answ.append(tournament)
        answ.append('Выбранный диапазон лет: '+year1+'...'+year2+'\n')
        quest = (' '.join(quest)).replace(' \n ', '\n')
        answ = (' '.join(answ)).replace(' \n ', '\n')
        return (quest, answ, img_q, img_a)
    else:
        return (['Попробуйте выбрать другой временной диапазон'])

#print (quest,'\n',answ,'\n',img_q,'\n',img_a)




