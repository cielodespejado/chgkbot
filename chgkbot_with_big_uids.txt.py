import configparser
import telebot
from telebot import types
import time
from time import sleep
import browse
from collections import namedtuple

config = configparser.ConfigParser()
config.read('config.ini')
bot = telebot.TeleBot(config['DEFAULT']['Token'])
#bot = telebot.TeleBot(config.token)

DB = {}
db = namedtuple('db', 'year1 year2 author')
with open('uids.txt', 'r') as u:
    k = u.readlines()
    for i in k:
        n = i.split()
        DB[int(n[0])] = db(n[1],n[2],n[3])
quest = {}
answ = {}
img_q = {}
img_a = {}
qid = {}
yid = {}
aid = {}
authors = {}
authors_keys = []
alphabet = []
end_int = False
start_int = False
set_author = False
global act_year
act_year = time.gmtime().tm_year 

commands = {  'start': 'Описание бота',
              'help': 'Список команд',
              'question': 'Случайный вопрос из базы',
              'set_year': 'Установить диапазон лет, из которого нужно брать вопросы',
              'rst_year': 'Сбросить диапазон лет до 2007-н.в.',
              'set_author': 'Выбрать автора вопросов',
              'rst_author': 'Отменить выбранного автора',
              'timer': 'Запустить таймер'
           }

def fillDB(cid, *flag):
    if flag:
        DB[cid] = db('2007', str(time.gmtime().tm_year), None)
    with open('uids.txt', 'w') as u:
        for i, k in DB.items():
            u.write(str(i)+' ')
            for k in tuple(k):
                u.write(str(k)+' ')
            u.write('\n')   

@bot.message_handler(commands=['start'])
def start(m):
    cid = m.chat.id
    if cid not in DB:
        fillDB(cid, 1)
        bot.send_message(cid, 'Привет, добро пожаловать')
        help(m)  
    elif cid==131041034:
        bot.send_message(cid, 'Привет, Наденька!')
        help(m)
    else:
        bot.send_message(cid, 'Снова привет!')
        help(m)


@bot.message_handler(commands=['help'])
def help(m):
    cid = m.chat.id
    if cid not in DB:
        fillDB(cid, 1)
    help_text = 'Доступны следующие команды: \n'
    for key in commands:  
        help_text += '/' + key + ': '
        help_text += commands[key] + '\n'
    bot.send_message(cid, help_text)  

@bot.message_handler(commands=['question'])    
def get_random(m):
    global quest
    global answ
    global img_q
    global img_a
    global qid
    cid = m.chat.id
    if cid not in DB:
        fillDB(cid, 1)
    y1 = DB[cid].year1
    y2 = DB[cid].year2
    a = DB[cid].author
    if a != None:
        f = browse.get_author(a,y1,y2)
        quest[cid] = f[0]
        answ[cid] = f[1]
        img_q[cid] = f[2]
        img_a[cid] = f[3]
    else:
        f = browse.get(y1,y2)
        quest[cid] = f[0]
        answ[cid] = f[1]
        img_q[cid] = f[2]
        img_a[cid] = f[3]
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text='Показать ответ', callback_data='answer')
    callback_button1 = types.InlineKeyboardButton(text='Запустить таймер', callback_data='timer')
    keyboard.add(callback_button, callback_button1)
    if img_q[cid]:
        for img in img_q[cid]:
            bot.send_photo(cid, img)
    sent = bot.send_message(cid, quest[cid], reply_markup=keyboard)
    qid[cid] = sent.message_id
    
@bot.message_handler(commands=['set_year'])    
def set_year(m):
    cid = m.chat.id
    if cid not in DB:
        fillDB(cid, 1)
    global set_author
    set_author = False
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text='1990-2000', callback_data='int1')
    callback_button1 = types.InlineKeyboardButton(text='2001-2010', callback_data='int2')
    callback_button2 = types.InlineKeyboardButton(text='2011-'+str(act_year-1), callback_data='int3')
    keyboard.add(callback_button, callback_button1, callback_button2)
    sent = bot.send_message(cid, 'Выберите начало интервала', reply_markup=keyboard)
    yid[cid] = sent.message_id
    global start_int
    start_int = True
    global end_int
    end_int = False
    
@bot.message_handler(commands=['set_author'])    
def set_author(m):
    global end_int
    global start_int
    end_int = False
    start_int = False
    cid = m.chat.id
    if cid not in DB:
        fillDB(cid, 1)
    button = []
    global alphabet
    alphabet = []
    with open('Authors.txt', 'r', encoding = 'utf-8') as u:
        spisok = u.readlines()
        for i in spisok:
            i.split()
            if i[0] not in alphabet:
                alphabet.append(i[0])
    keyboard = types.InlineKeyboardMarkup()
    for letter in alphabet:
        button.append(types.InlineKeyboardButton(text=letter, callback_data=letter))
    keyboard.add(*button)
    sent = bot.send_message(cid, 'Выберите автора:', reply_markup=keyboard)
    aid[cid] = sent.message_id
    global set_author
    set_author = True
    
@bot.message_handler(commands=['rst_year'])    
def rst_year(m):
    cid = m.chat.id
    if cid not in DB:
        fillDB(cid, 1)
    DB[cid] = DB[cid]._replace(year1 = '2007', year2 = str(time.gmtime().tm_year))
    fillDB(cid)
    
@bot.message_handler(commands=['rst_author'])    
def rst_author(m):
    cid = m.chat.id
    if cid not in DB:
        fillDB(cid, 1)
    DB[cid] = DB[cid]._replace(author = None)
    fillDB(cid)
    
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    cid = call.message.chat.id
    global end_int
    global start_int
    global year1
    global year2
    global set_author
    global author
    global authors
    global authors_keys
    if call.message:
        if call.data == 'timer':
            sent = bot.send_message(cid, '01:00')
            mid = sent.message_id
            global timer
            timer = True
            interval = 60
            time.sleep(1)
            while interval and timer:
                interval -= 1
                mins, secs = divmod(interval, 60)
                t = '{:01d}:{:02d}'.format(mins, secs)
                bot.edit_message_text(chat_id=cid, message_id=mid, text=t)
                time.sleep(1)
                if interval == 0:
                    bot.edit_message_text(chat_id=cid, message_id=mid, text='Время истекло')
            time.sleep(5)
            bot.delete_message(cid, mid)
        elif call.data == 'answer':
            if timer:
                timer = False
            bot.send_message(cid, answ[cid])
            if img_a[cid]:
                for img in img_a[cid]:
                    bot.send_photo(cid, img)
            bot.edit_message_text(chat_id=cid, message_id=qid[cid], text=quest[cid])
        elif call.data == 'int1':
            keyboard = types.InlineKeyboardMarkup()
            button = []
            if start_int==True:
                txt = 'Выберите начало интервала'
                i = 1990
            else:
                txt = 'Выберите конец интервала'
                i = int(year1[cid])
            for text in range(i,2001):
                button.append(types.InlineKeyboardButton(text=str(text), callback_data=str(text)))
            keyboard.add(*button)
            sent = bot.edit_message_text(chat_id=cid, message_id=yid[cid], text=txt, reply_markup=keyboard)
        elif call.data == 'int2':
            keyboard = types.InlineKeyboardMarkup()
            button = []
            if start_int==True:
                txt = 'Выберите начало интервала'
                i = 2001
            else:
                txt = 'Выберите конец интервала'
                i = int(year1[cid])
            for text in range(i,2011):
                button.append(types.InlineKeyboardButton(text=str(text), callback_data=str(text)))
            keyboard.add(*button)    
            sent = bot.edit_message_text(chat_id=cid, message_id=yid[cid], text=txt, reply_markup=keyboard)
        elif call.data == 'int3':
            keyboard = types.InlineKeyboardMarkup()
            button = []
            if start_int==True:
                txt = 'Выберите начало интервала'
                i = 2011
            else:
                txt = 'Выберите конец интервала'
                i = int(year1[cid])
            for text in range(i,act_year):
                button.append(types.InlineKeyboardButton(text=str(text), callback_data=str(text)))
            keyboard.add(*button)
            sent = bot.edit_message_text(chat_id=cid, message_id=yid[cid], text=txt, reply_markup=keyboard)
        elif start_int==True and int(call.data) in range(1991,act_year+1):
            DB[cid] = DB[cid]._replace(year1 = call.data)
            button = []  
            keyboard = types.InlineKeyboardMarkup()
            if 1990<int(call.data)<2000:
                button.append(types.InlineKeyboardButton(text=year1[cid]+'-2000', callback_data='int1'))
                button.append(types.InlineKeyboardButton(text='2001-2010', callback_data='int2'))
                button.append(types.InlineKeyboardButton(text='2011-'+str(act_year-1), callback_data='int3'))
                button.append(types.InlineKeyboardButton(text=str(act_year), callback_data=str(act_year)))
            elif int(call.data)==2000:
                button.append(types.InlineKeyboardButton(text='2000', callback_data='2000'))
                button.append(types.InlineKeyboardButton(text='2001-2010', callback_data='int2'))
                button.append(types.InlineKeyboardButton(text='2011-'+str(act_year-1), callback_data='int3'))
                button.append(types.InlineKeyboardButton(text=str(act_year), callback_data=str(act_year)))
            elif 2000<int(call.data)<2010:
                button.append(types.InlineKeyboardButton(text=year1[cid]+'-2010', callback_data='int2'))
                button.append(types.InlineKeyboardButton(text='2011-'+str(act_year-1), callback_data='int3'))
                button.append(types.InlineKeyboardButton(text=str(act_year), callback_data=str(act_year)))
            elif int(call.data)==2010:
                button.append(types.InlineKeyboardButton(text='2010', callback_data='2010'))
                button.append(types.InlineKeyboardButton(text='2011-'+str(act_year-1), callback_data='int3'))
                button.append(types.InlineKeyboardButton(text=str(act_year), callback_data=str(act_year)))    
            elif 2010<int(call.data)<act_year-1:
                button.append(types.InlineKeyboardButton(text=year1[cid]+'-'+str(act_year-1), callback_data='int3'))
                button.append(types.InlineKeyboardButton(text=str(act_year), callback_data=str(act_year)))
            elif int(call.data)==act_year-1:
                button.append(types.InlineKeyboardButton(text=str(act_year), callback_data=str(act_year-1)))
                button.append(types.InlineKeyboardButton(text=str(act_year), callback_data=str(act_year)))
            keyboard.add(*button)
            sent = bot.edit_message_text(chat_id=cid, message_id=yid[cid], text='Выберите конец интервала', reply_markup=keyboard)
            end_int = True
            start_int = False
        elif end_int==True and int(call.data) in range(1991,act_year+1):
            DB[cid] = DB[cid]._replace(year2 = call.data)
            fillDB(cid)
            sent = bot.edit_message_text(chat_id=cid, message_id=yid[cid], text='Интервал сохранён')
            end_int = False
        elif set_author==True and call.data in alphabet:
            authors = {}
            authors_keys = []            
            with open('Authors.txt', 'r', encoding = 'utf-8') as u:
                spisok = u.readlines()
                for i in spisok:
                    i.split()
                    if i[0] == call.data:
                        k = i.split()
                        authors[k[0]+' '+k[1]] = k[2]
                authors_keys = list(authors.keys())
            keyboard = types.InlineKeyboardMarkup(row_width = 2)
            button = []
            for a in authors_keys:
                button.append(types.InlineKeyboardButton(text=a, callback_data=a))
            keyboard.add(*button)
            sent = bot.edit_message_text(chat_id=cid, message_id=aid[cid], text='Выберите автора:', reply_markup=keyboard)  
        elif set_author==True and call.data in authors:
            DB[cid] = DB[cid]._replace(author = authors[call.data])
            fillDB(cid)
            sent = bot.edit_message_text(chat_id=cid, message_id=aid[cid], text='Автор выбран')
            set_author = False
            
@bot.message_handler(commands=['timer'])    
def timer(m):
    cid = m.chat.id
    sent = bot.send_message(cid, '01:00')
    mid = sent.message_id
    interval = 60
    time.sleep(1)
    while interval:
        interval -= 1
        mins, secs = divmod(interval, 60)
        t = '{:01d}:{:02d}'.format(mins, secs)
        time.sleep(1)
        bot.edit_message_text(chat_id=cid, message_id=mid, text=t)
        if interval == 0:
            bot.edit_message_text(chat_id=cid, message_id=mid, text='Время истекло')
    time.sleep(5)
    bot.delete_message(cid, mid)    

if __name__ == '__main__':
    bot.polling(none_stop=True) 



# 131041034 надин
# 55030446 мой
