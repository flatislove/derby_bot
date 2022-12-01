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

    def get_id(self):
        return self.get_id

    def get_firstname(self):
        return self.firstname

    def get_lastname(self):
        return self.lastname

    def get_team_id(self):
        return self.team_id

    def get_number(self):
        return self.number

    def get_position_id(self):
        return self.position_id

    def set_firstname(self,firstname):
        self.firstname=firstname

    def set_lastname(self,lastname):
        self.lastname=lastname

    def set_team_id(self,team_id):
        self.team_id=team_id

    def set_number(self,number):
        self.number=number

    def set_position_id(self,position_id):
        self.position_id=position_id