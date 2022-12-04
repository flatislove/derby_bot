import time
import telebot
import service.service as s
import service.service_db as dbs
from src.config import token
from telebot import types
import model.currency as cur

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def button_message_geo(message):
    markup=types.ReplyKeyboardMarkup()
    # markup.row_width = 2
    markup.add( types.InlineKeyboardButton(text="Как далеко офис Google?", request_location=True),
                types.InlineKeyboardButton("subscribe", callback_data="link"),
                types.InlineKeyboardButton(text="Конвертер BYN/KZT",callback_data="tenge_is"))
    # main_keyboard=None
    # main_keyboard=types.KeyboardButton()
    # item1=types.InlineKeyboardButton(text="geo",request_location=True)
    # item2=types.InlineKeyboardButton(text="subscribe")
    # item3=types.InlineKeyboardButton(text="Сколько это в тенге?")
    # markup.add(item1)
    # markup.add(item2)
    # markup.add(item3)
    bot.send_message(message.chat.id,"Погнали!",reply_markup=markup)
    bot.send_sticker(message.chat.id, sticker='CAACAgIAAxkBAAEGqV5jiyw2iRSTw6bH788UxRAvS6u5uAACJxgAApd54UvWARYS3sXfTysE')

@bot.message_handler(content_types=['location'])
def message_reply_location(message):
    if message.location is not None:
        print(message.location)
        print("latitude: %s;longitude:%s"%(message.location.latitude,message.location.longitude))

# @bot.message_handler(commands=['button'])
# def button_message(message):
    # markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    # item1=types.KeyboardButton("button")
    # main_keyboard.add(item1)
    # bot.send_message(message.chat.id,"Выберите, что вам нужно", reply_markup=main_keyboard)
@bot.message_handler(commands=['info'])
def get_info_messages(message):
    bot.send_message(message.from_user.id,"Команды",reply_markup=s.teams_to_markups())
    bot.callback_query_handler(get_callback_team)

@bot.message_handler(content_types=['text'])
def message_reply(message):
    if message.text=="button":
        bot.send_message(message.chat.id,"click")
    if message.text.lower()=="как дела?":
        bot.send_sticker(message.chat.id,)
    if message.text=="Конвертер BYN/KZT":
        count = bot.send_message(message.chat.id, f"Введите сумму в BYN")
        bot.register_next_step_handler(count, get_count_tenge)
    if message.text=="Как далеко офис Google?":
        location=bot.send_location(message.chat.id,"lokat")
        print(location)

def get_count_tenge(message):
    count_money=float(message.text)
    bot.send_message(message.chat.id,f"{count_money} BYN это {s.get_exchange_currency(cur.Currency.KZT.value,count_money)} KZT в тенге")
    

@bot.message_handler(content_types=['sticker'])
def message_reply(message):
    bot.send_sticker(message.chat.id,"CAACAgIAAxkBAAEGqV5jiyw2iRSTw6bH788UxRAvS6u5uAACJxgAApd54UvWARYS3sXfTysE")

@bot.message_handler(commands=['add_player'])
def firstname_handler(message):
    firstname = bot.send_message(message.chat.id, 'Введите имя',)
    bot.register_next_step_handler(firstname, lastname_handler)

def lastname_handler(message):
    firstname=message.text
    lastname = bot.send_message(message.chat.id, f"Ваше имя {firstname}. Введите фамилию")
    bot.register_next_step_handler(lastname, team_handler, firstname)

def team_handler(message,firstname):
    lastname=message.text
    team_id=bot.send_message(message.chat.id,f"Ваше имя {firstname}. Введите номер команды",reply_markup=s.teams_to_markups_add())
    bot.register_next_step_handler(team_id, number_handler, firstname,lastname)

def number_handler(message,firstname,lastname):
    team_id=message.text
    number=bot.send_message(message.chat.id,f"Ваше имя {firstname}. Введите игровой номер")
    print(f"{number.text}<---team id")
    bot.register_next_step_handler(number, position_handler, firstname, lastname, team_id)

def position_handler(message,firstname,lastname,team_id):
    number=message.text
    position_id=bot.send_message(message.chat.id,f"Ваше имя {firstname}. Введите номер позиции")
    bot.register_next_step_handler(position_id, summary_handler, firstname, lastname, team_id,number)

def summary_handler(message,firstname,lastname,team_id,number):
    position_id=message.text
    res=dbs.add_player(firstname,lastname,team_id,number,position_id)
    if res!=-1:
        bot.send_message(message.chat.id,f'Игрок успешно добавлен')
    else:
        bot.send_message(message.chat.id,f'Не удалось добавить игрока')
    


@bot.callback_query_handler(func=lambda call: call.data.startswith('team'))
def get_callback_team(call):
    team=call.data.split(" ")
    id_team,name_team=team[1],team[2]
    bot.send_message(call.from_user.id,f"Состав {name_team}:",reply_markup=s.players_to_markups(id_team))
    bot.callback_query_handler(get_callback_player_details)

@bot.callback_query_handler(func=lambda call: call.data.startswith('player'))
def get_callback_player_details(call):
    p=dbs.get_player_by_id(call.data.split(" ")[1])
    bot.send_message(call.from_user.id,s.show_player_details(p))

# @bot.callback_query_handler(func=lambda call: call.data.startswith('pos'))
# def get_callback_position(call):
#     print(call.data)

# @bot.callback_query_handler(func=lambda call: call.data.startswith('player'))
# def get_callback_position(call):
#     print(call.data)


try:
    bot.polling(none_stop=True)
except Exception as e:
    time.sleep(15)


# bot.polling(none_stop=True, interval=0)