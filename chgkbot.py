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
userStep = {} 
quest = {}
answ = {}
img = {}
    
commands = {  'start': 'Bot description',
              'help': 'List of commands',
              'question': 'Get random question from db.chgk.info',
              'timer': 'Start 1 minute timer',
           }

def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        return 0

@bot.message_handler(commands=['start'])
def start(m):
    cid = m.chat.id
    if cid not in knownUsers:  
        knownUsers.append(cid)
        u = open('uids.txt', 'w', encoding='utf_8')
        u.write(str(cid)+'\n')
        u.close()
        userStep[cid] = 0
        bot.send_message(cid, "Привет, добро пожаловать")
        help(m)  
    elif cid==131041034:
        bot.send_message(cid, "Привет, Наденька!")
    else:
        bot.send_message(cid, "Снова привет!")


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
    global img
    cid = m.chat.id
    f = browse.get()
    quest[cid] = f[0]
    answ[cid] = f[1]
    img[cid] = f[2]
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Показать ответ", callback_data="answer")
    callback_button1 = types.InlineKeyboardButton(text="Запустить таймер", callback_data="timer")
    keyboard.add(callback_button, callback_button1)
    if img[cid]:
        bot.send_photo(cid, img[cid])
    bot.send_message(cid, quest[cid], reply_markup=keyboard)
   
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
            bot.edit_message_text(chat_id=cid, message_id=mid, text="Время истекло")
            time.sleep(5)
            bot.delete_message(cid, mid)
        elif call.data == "answer":
            if timer:
                timer = False
            bot.send_message(cid, answ[cid])    

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
    bot.polling(none_stop=True) 

#bot.polling()
