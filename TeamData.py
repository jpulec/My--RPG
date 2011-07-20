class TeamData:
    def __init__(self):
        self.team = dict()
        self.money = 100
        self.shit = dict()


    def add(self, name, character):
        self.team[name] = character

    def remove(self, name):
        del self.team[name]        
