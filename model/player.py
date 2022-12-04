class Player:
    def __init__(self,id,firstname,lastname,team_id,number,position_id):
        self.id=id
        self.firstname=firstname
        self.lastname=lastname
        self.team_id=team_id
        self.number=number
        self.position_id=position_id

    def __str__(self):
        return f"Id: {self.id:5}; Name: {self.firstname}"