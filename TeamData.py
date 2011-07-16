class TeamData:
    def __init__(self):
        self.team = []
        self.money = 100


    def add(self, member):
        self.team.append(member)

    def remove(self, member):
        self.team.remove(member)        
