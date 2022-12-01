import model.database as db
import model.team as team
import model.position as position
import model.player as player

def q_get_teams():
    get=db.get_from_database("""SELECT * 
                                FROM "Team";""")
    teams=[]
    for i in get:
        teams.append(team.Team(i[0],i[1]))
    return teams

def q_get_positions():
    get=db.get_from_database("""SELECT * 
                                FROM "Position";""")
    positions=[]
    for i in get:
        positions.append(position.Position(i[0],i[1]))
    return positions

def q_get_players_by_team_id(id_team):
    get=db.get_from_database(f"""   SELECT * 
                                    FROM public."Player"
                                    WHERE "Player".team_id='{id_team}';""")
    players=[]
    for plr in get:
        players.append(player.Player(plr[0],plr[1],plr[2],plr[3],plr[4],plr[5]))
    return players

def q_add_player(player):
    add=f"""INSERT INTO "Player"(firstname,lastname,team_id,number,position_id)
            VALUES('{player.firstname}','{player.lastname}','{int(player.team_id)}','{player.number}','{int(player.position_id)}');"""
    return db.add_to_database(add)

def q_get_player_by_id(id):
    get=db.get_from_database(f"""   SELECT * FROM public."Player"
                                    WHERE "Player".id='{id}';""")
    plr=player.Player(get[0][0],get[0][1],get[0][2],get[0][3],get[0][4],get[0][5])
    return plr

def q_get_team_by_id(id):
    get=db.get_from_database(f"""   SELECT * FROM public."Team"
                                    WHERE "Team".id='{id}';""")
    tm=team.Team(get[0][0],get[0][1])
    return tm

def q_get_position_by_id(id):
    get=db.get_from_database(f"""   SELECT * FROM public."Position"
                                    WHERE "Position".id='{id}';""")
    ps=position.Position(get[0][0],get[0][1])
    return ps