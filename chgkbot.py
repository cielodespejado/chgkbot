import config
import configparser
import telebot
from telebot import types
import time
from time import sleep
import browse

config = configparser.ConfigParser()
config.read('config.ini')
bot = telebot.TeleBot(config['DEFAULT']['Token'])
#bot = telebot.TeleBot(config.token)

knownUsers = []

quest = {}
answ = {}
img_q = {}
img_a = {}
qid = {}
yid = {}
year1 = {}
year2 = {}

commands = {  'start': 'Описание бота',
              'help': 'Список команд',
              'question': 'Случайный вопрос из базы',
              'set_year': 'Установить диапазон лет, из которого нужно брать вопросы',
              'timer': 'Запустить таймер'
           }

@bot.message_handler(commands=['start'])
def start(m):
    cid = m.chat.id
    if cid not in knownUsers:  
        knownUsers.append(cid)
        with open('uids.txt', 'w', encoding='utf_8') as u:
          u.write(str(cid)+'\n')
        bot.send_message(cid, "Привет, добро пожаловать")
        help(m)  
    elif cid==131041034:
        bot.send_message(cid, "Привет, Наденька!")
        help(m)
    else:
        bot.send_message(cid, "Снова привет!")
        help(m)


@bot.message_handler(commands=['help'])
def help(m):
    cid = m.chat.id
    help_text = "Доступны следующие команды: \n"
    for key in commands:  
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  

@bot.message_handler(commands=['question'])    
def get_random(m):
    global quest
    global answ
    global img_q
    global img_a
    global qid
    cid = m.chat.id
    if cid in year1:
      y1 = str(year1[cid])
    else:
      y1 = '2007'
    if cid in year2:
      y2 = str(year2[cid])
    else:
      y2 = str(time.gmtime().tm_year)
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
        bot.send_photo(cid, img_q[cid])
    sent = bot.send_message(cid, quest[cid], reply_markup=keyboard)
    qid[cid] = sent.message_id
    
@bot.message_handler(commands=['set_year'])    
def set_year(m):
    cid = m.chat.id
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text='1991-2000', callback_data='int1')
    callback_button1 = types.InlineKeyboardButton(text='2001-2010', callback_data='int2')
    callback_button2 = types.InlineKeyboardButton(text='2011-н.в.', callback_data='int3')
    keyboard.add(callback_button, callback_button1, callback_button2)
    sent = bot.send_message(cid, 'Выберите начало интервала', reply_markup=keyboard)
    yid[cid] = sent.message_id

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    cid = call.message.chat.id
    if call.message:
        if call.data == "timer":
            sent = bot.send_message(cid, "01:00")
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
                    bot.edit_message_text(chat_id=cid, message_id=mid, text="Время истекло")
            time.sleep(5)
            bot.delete_message(cid, mid)
        elif call.data == "answer":
            if timer:
                timer = False
            bot.send_message(cid, answ[cid])
            if img_a[cid]:
                bot.send_photo(cid, img_a[cid])
            bot.edit_message_text(chat_id=cid, message_id=qid[cid], text=quest[cid]) 
        elif call.data == "int1":
          keyboard = types.InlineKeyboardMarkup()
          callback_button = types.InlineKeyboardButton(text='91', callback_data='1991')
          callback_button1 = types.InlineKeyboardButton(text='92', callback_data='1992')
          callback_button2 = types.InlineKeyboardButton(text='93', callback_data='1993')
          callback_button3 = types.InlineKeyboardButton(text='94', callback_data='1994')
          callback_button4 = types.InlineKeyboardButton(text='95', callback_data='1995')
          callback_button5 = types.InlineKeyboardButton(text='96', callback_data='1996')
          callback_button6 = types.InlineKeyboardButton(text='97', callback_data='1997')
          callback_button7 = types.InlineKeyboardButton(text='98', callback_data='1998')
          callback_button8 = types.InlineKeyboardButton(text='99', callback_data='1999')
          callback_button9 = types.InlineKeyboardButton(text='00', callback_data='2000')
          keyboard.add(callback_button, callback_button1, callback_button2, callback_button3, callback_button4, callback_button5, callback_button6, callback_button7, callback_button8, callback_button9)
          sent = bot.edit_message_text(chat_id=cid, message_id=yid[cid], text='Выберите начало интервала', reply_markup=keyboard)
          yid[cid] = sent.message_id
        elif call.data == "int2":
          keyboard = types.InlineKeyboardMarkup()
          callback_button = types.InlineKeyboardButton(text='01', callback_data='2001')
          callback_button1 = types.InlineKeyboardButton(text='02', callback_data='2002')
          callback_button2 = types.InlineKeyboardButton(text='03', callback_data='2003')
          callback_button3 = types.InlineKeyboardButton(text='04', callback_data='2004')
          callback_button4 = types.InlineKeyboardButton(text='05', callback_data='2005')
          callback_button5 = types.InlineKeyboardButton(text='06', callback_data='2006')
          callback_button6 = types.InlineKeyboardButton(text='07', callback_data='2007')
          callback_button7 = types.InlineKeyboardButton(text='08', callback_data='2008')
          callback_button8 = types.InlineKeyboardButton(text='09', callback_data='2009')
          callback_button9 = types.InlineKeyboardButton(text='10', callback_data='2010')
          keyboard.add(callback_button, callback_button1, callback_button2, callback_button3, callback_button4, callback_button5, callback_button6, callback_button7, callback_button8, callback_button9)
          sent = bot.edit_message_text(chat_id=cid, message_id=yid[cid], text='Выберите начало интервала', reply_markup=keyboard)
          yid[cid] = sent.message_id
        elif call.data == "int3":
          keyboard = types.InlineKeyboardMarkup()
          callback_button = types.InlineKeyboardButton(text='11', callback_data='2011')
          callback_button1 = types.InlineKeyboardButton(text='12', callback_data='2012')
          callback_button2 = types.InlineKeyboardButton(text='13', callback_data='2013')
          callback_button3 = types.InlineKeyboardButton(text='14', callback_data='2014')
          callback_button4 = types.InlineKeyboardButton(text='15', callback_data='2015')
          callback_button5 = types.InlineKeyboardButton(text='16', callback_data='2016')
          callback_button6 = types.InlineKeyboardButton(text='17', callback_data='2017')
          callback_button7 = types.InlineKeyboardButton(text='18', callback_data='2018')
          callback_button8 = types.InlineKeyboardButton(text='19', callback_data='2019')
          callback_button9 = types.InlineKeyboardButton(text='20', callback_data='2020')
          keyboard.add(callback_button, callback_button1, callback_button2, callback_button3, callback_button4, callback_button5, callback_button6, callback_button7, callback_button8, callback_button9)
          sent = bot.edit_message_text(chat_id=cid, message_id=yid[cid], text='Выберите начало интервала', reply_markup=keyboard)
          yid[cid] = sent.message_id  

@bot.message_handler(commands=['timer'])    
def timer(m):
    cid = m.chat.id
    sent = bot.send_message(cid, "01:00")
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
            bot.edit_message_text(chat_id=cid, message_id=mid, text="Время истекло")    

if __name__ == '__main__':
  with open('uids.txt', 'r', encoding='utf_8') as u:
    for line in u.readlines():
      if line not in knownUsers:
        knownUsers.append(line)
  bot.polling(none_stop=True) 

