import model.queries as query
import model.player as player

def add_team():
    pass

def get_team_by_id(id):
    return query.q_get_team_by_id(id)

def get_teams():
    return query.q_get_teams()

def add_player(firstname,lastname,team_id,number,position_id):
    plr=player.Player(0,firstname,lastname,team_id,number,position_id)
    return query.q_add_player(plr)
    
def get_player_by_id(player_id):
    return query.q_get_player_by_id(player_id)

def get_player_by_id_team(id_team):
    return query.q_get_players_by_team_id(id_team)

def get_players():
    pass

def add_position():
    pass

def get_position_by_id(position_id):
    return query.q_get_position_by_id(position_id)

def get_positions():
    return query.q_get_positions()