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
    markup.add( types.InlineKeyboardButton(text='Что могу?', callback_data="what?"),
                types.InlineKeyboardButton(text="Ссылка на гит с кодом",callback_data="gitcode"),
                types.InlineKeyboardButton(text="Конвертер BYN/KZT",callback_data="tenge_is"))
    markup.add(types.KeyboardButton(text="Что по погоде?",request_location=True))

    bot.send_message(message.chat.id,f"Погнали, {message.from_user.username}!",reply_markup=markup)
    bot.send_sticker(message.chat.id, sticker='CAACAgIAAxkBAAEGqV5jiyw2iRSTw6bH788UxRAvS6u5uAACJxgAApd54UvWARYS3sXfTysE')

@bot.message_handler(content_types=['location'])
def message_reply_location(message):
    if message.location is not None:
        weather=s.get_weather(message.location.latitude,message.location.longitude)
        bot.send_message(message.chat.id,f"Погода за окном такая:\n Температура {weather.get('temperature')} градусов\n Скорость ветра {weather.get('windspeed')}м/с\n")
        bot.send_message(message.chat.id,f"Кстати, между Вами и офисом гугл {s.get_distance_between_points(message.location.latitude,message.location.longitude)} км")

@bot.message_handler(commands=['info'])
def get_info_messages(message):
    bot.send_message(message.from_user.id,"Команды",reply_markup=s.teams_to_markups())
    bot.callback_query_handler(get_callback_team)

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
    team_id=bot.send_message(message.chat.id,f"Введите id номер команды",reply_markup=s.teams_to_markups_add())
    bot.register_next_step_handler(team_id, number_handler, firstname,lastname)

def number_handler(message,firstname,lastname):
    team_id=message.text
    number=bot.send_message(message.chat.id,f"Введите игровой номер")
    bot.register_next_step_handler(number, position_handler, firstname, lastname, team_id)

def position_handler(message,firstname,lastname,team_id):
    number=message.text
    position_id=bot.send_message(message.chat.id,f"Введите id номер позиции",reply_markup=s.positions_to_markups_add())
    bot.register_next_step_handler(position_id, summary_handler, firstname, lastname, team_id,number)

def summary_handler(message,firstname,lastname,team_id,number):
    position_id=message.text
    res=dbs.add_player(firstname,lastname,team_id,number,position_id)
    if res!=-1:
        bot.send_message(message.chat.id,f'Игрок успешно добавлен')
    else:
        bot.send_message(message.chat.id,f'Не удалось добавить игрока')

@bot.callback_query_handler(func=lambda call: call.data.startswith('lin'))
def get_callback_player_details(call):
    print("subs")
    bot.answer_callback_query(callback_query_id=call.id, text="Неверно, Верный ответ...", show_alert=True)

def get_count_tenge(message):
    count_money=float(message.text)
    bot.send_sticker(message.chat.id,"CAACAgIAAxkBAAEGqXdjiy8tTv-fqQJLo3OKf8-fiddXbgAC3BQAAnWf4EtIjabVCNG-PisE")
    bot.send_message(message.chat.id,f"{count_money} BYN это {s.get_exchange_currency(cur.Currency.KZT.value,count_money)} KZT в тенге")

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

@bot.message_handler(content_types=['text'])
def message_reply(message):
    if message.text.lower().strip()=="привет":
        bot.send_sticker(message.chat.id,"CAACAgIAAxkBAAEGrjtjjNUJLFyOJRT_L3XX8H07O9gQJQACaRcAAqnJOUoBu84B21ly6isE")
        bot.send_message(message.chat.id,"И тебе привет)")
    elif message.text.lower()=="как дела?" or message.text.lower()=="как дела":
        bot.send_sticker(message.chat.id,"CAACAgIAAxkBAAEGrj1jjNUe36tGdpHA7CsEUJYY5RMr9QAC-BEAAoPF6UvVPQGi07k3jSsE")
        bot.send_message(message.chat.id,"А у тебя?")
    elif message.text=="Конвертер BYN/KZT":
        count = bot.send_message(message.chat.id, f"Введите сумму в BYN")
        bot.register_next_step_handler(count, get_count_tenge)
    elif message.text=="Ссылка на гит с кодом":
        bot.send_sticker(message.chat.id,"CAACAgIAAxkBAAEGrktjjNjTDAJuWz_MA0tEAAGZoo_YZa4AApAZAAKn6UFKS0BguZTHflkrBA")
        count = bot.send_message(message.chat.id, "https://github.com/flatislove/derby_bot")
    elif message.text=="Что могу?":
        bot.send_sticker(message.chat.id,"CAACAgIAAxkBAAEGrk1jjNkBgQhb796wZ-vwpnPkzMMmOgACRiAAAkRbyErWG5mnIxS-aCsE")
        count = bot.send_message(message.chat.id, s.get_description())
    else:
        bot.send_sticker(message.chat.id,"CAACAgIAAxkBAAEGrj9jjNWr6sgP5-edjkWOZnDoE9FwkwACPhYAAiR2OUhOF80tn_t59CsE")
        bot.send_message(message.chat.id,"Такой команды нет)")
           
@bot.message_handler(content_types=['sticker'])
def message_reply(message):
    bot.send_sticker(message.chat.id,"CAACAgIAAxkBAAEGqV5jiyw2iRSTw6bH788UxRAvS6u5uAACJxgAApd54UvWARYS3sXfTysE")

try:
    bot.polling(none_stop=True)
except Exception as ex:
    time.sleep(5)
    bot.polling(non_stop=True)
    print(f"[INFO] Ошибка {ex}")