class Team:
    def __init__(self,id,name):
        self.id=id
        self.name=name

    def __str__(self):
        return f"Id: {self.id:5}; Name: {self.name}"