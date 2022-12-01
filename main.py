import telebot
import service.service as s
import service.service_db as dbs
from src.config import token

bot = telebot.TeleBot(token)

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
    team_id=bot.send_message(message.chat.id,f"Ваше имя {firstname}. Введите номер команды")
    bot.register_next_step_handler(team_id, number_handler, firstname,lastname)

def number_handler(message,firstname,lastname):
    team_id=message.text
    number=bot.send_message(message.chat.id,f"Ваше имя {firstname}. Введите игровой номер")
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
    
@bot.message_handler(commands=['info'])
def get_info_messages(message):
    bot.send_message(message.from_user.id,"Команды",reply_markup=s.teams_to_markups())
    bot.callback_query_handler(get_callback_team)

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


bot.polling(none_stop=True, interval=0)