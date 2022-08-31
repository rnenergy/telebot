import telebot
import time
from telebot import types
import pymysql
from config import host, user, password, db_name


bot = telebot.TeleBot("5167420584:AAEfgV_kt112YWgPB7kU5WrJnUnTwNuCjIo", parse_mode=None)

bot.set_my_commands([
    telebot.types.BotCommand("/start", "Start Page"),
    telebot.types.BotCommand("/register_me", "register phone number"),
    telebot.types.BotCommand("/wirte_a_message", "Send Message")
])

@bot.message_handler(commands=['start'])
def func(message):
    bot.send_message(message.chat.id, text="Hello, {0.first_name}! I am introserv.eu registrator bot. After registration you will get notifications from Introserv.eu and will be able to write a messages to service support.".format(message.from_user),)


@bot.message_handler(commands=['wirte_a_message'])
def handle_text(message):
    cid = message.chat.id
    msgPhone = bot.send_message(cid, 'Write your message:')
    bot.register_next_step_handler(msgPhone , message_from_client)

def message_from_client(message):
    cid = message.chat.id
    client_message = message.text
    timenow = time.strftime('%H:%M', time.localtime())
    datenow = time.strftime('%Y-%m-%d', time.localtime())
    bot.send_message(cid, f"Message \"{client_message}\" from {cid} was sent.")
    
    try:
        connection = pymysql.connect(
        host = host,
        port = 3306,
        user = user,
        password = password,
        database = db_name,
        cursorclass = pymysql.cursors.DictCursor
    )
   
        try:
        
            with connection.cursor() as cursor:
                insert_query = "INSERT INTO `messeges` (tg_user_id, message, date, time) VALUES ('%(cid)s','%(client_message)s','%(datenow)s','%(timenow)s');" % {'cid': cid, 'client_message': client_message, 'datenow': datenow, 'timenow': timenow}
                cursor.execute(insert_query)
                connection.commit()

        finally:
            connection.close()
            
    except Exception as ex:
        print("Connection refused...")
        print(ex)

@bot.message_handler(commands=['register_me'])
def handle_text(message):
    cid = message.chat.id
    msgPhone = bot.send_message(cid, 'Set your phone number similar to your introserv.eu account:')
    bot.register_next_step_handler(msgPhone , step_Set_Price)

def step_Set_Price(message):
    cid = message.chat.id
    phonenumb = message.text
    timenow1 = time.strftime('%H:%M', time.localtime())
    datenow1 = time.strftime('%Y-%m-%d', time.localtime())
    
    bot.send_message(cid, f"Your ID: {cid} Your Phone numb: {phonenumb} и эта пара ключ-значение пишется в БД для дальнейшего использования в ПФ. Так у нас будет сопоставление клиент-телеграм, а посылать сообщение по кнопке с POST запросом: https://api.telegram.org/bot5167420584:AAEfgV_kt112YWgPB7kU5WrJnUnTwNuCjIo/sendMessage?chat_id=5535529693&text=Текст тикета!")
    
    try:
        connection = pymysql.connect(
        host = host,
        port = 3306,
        user = user,
        password = password,
        database = db_name,
        cursorclass = pymysql.cursors.DictCursor
    )
   
        try:
        
            with connection.cursor() as cursor:
                insert_query = "INSERT INTO `user_ids` (phone_number, tg_user_id, date, time) VALUES ('%(phonenumb)s','%(cid)s','%(datenow1)s','%(timenow1)s');" % {'phonenumb': phonenumb, 'cid': cid, 'datenow1': datenow1, 'timenow1': timenow1}
                cursor.execute(insert_query)
                connection.commit()

        finally:
            connection.close()
            
    except Exception as ex:
        print("Connection refused...")
        print(ex)
                                   
@bot.message_handler(content_types=['text'])
def func(message):

    bot.send_message(message.chat.id, text="If you want to send a message or answer on it, use Send Message link in the menu.")



bot.polling(none_stop=True)
