from telebot import types
import service.service_db as s
import service.exchange_service as ex_s

def teams_to_markups():
    markup = types.InlineKeyboardMarkup()
    teams=s.get_teams()
    for team in teams:
        markup.add(types.InlineKeyboardButton(team.name, callback_data=f"team {team.id} {team.name}"))
    return markup

def teams_to_markups_add():
    markup = types.InlineKeyboardMarkup()
    teams=s.get_teams()
    for team in teams:
        markup.add(types.InlineKeyboardButton(team.name, callback_data=f"add_player_team {team.id} {team.name}"))
    return markup

def players_to_markups(id_team):
    markup = types.InlineKeyboardMarkup()
    players=s.get_player_by_id_team(id_team)
    for p in players:
        markup.add(types.InlineKeyboardButton(f"{p.firstname} {p.lastname}", callback_data=f"player {p.id}"))
    return markup

def show_player_details(p):
    team=s.get_team_by_id(p.team_id)
    position=s.get_position_by_id(p.position_id)
    info=f"Информация по {p.id}:\n Имя:{p.firstname}\n Фамилия:{p.lastname}\n Название команды:{team.name}\n Игровой номер:{p.number}\n Позиция:{position.name}"
    return info

def positions_to_markups():
    markup = types.InlineKeyboardMarkup()
    positions=s.get_positions()
    for position in positions:
        markup.add(types.InlineKeyboardButton(position.name, callback_data=f"position {position.id}"))
    return markup

def get_exchange_currency(currency,count_money):
    return round(ex_s.get_currency_rates(currency,count_money),3)