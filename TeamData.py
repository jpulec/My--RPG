class TeamData:
    def __init__(self):
        self.team = []
        self.money = 100
        self.HTCList = []
        self.WTCList = []
        self.itemList = []
        self.shit = dict()


    def add(self, character):
        self.team.append(character)

    def remove(self, character):
        self.team.remove(character)
        
    def addShit(self, shit):
        if shit.name in self.shit:
            self.shit[shit.name].quantity += shit.quantity
        else:
            self.shit[shit.name] = shit
            for x in shit.types:
<<<<<<< HEAD
                #print x
                if x.strip() == "WTC":
                    #print "WTC"
=======
                print x
                if x.strip() == "WTC":
                    print "WTC"
>>>>>>> ca2130befcd2831510f8fded56024422daa3eae2
                    self.WTCList.append(shit.name)
                if x.strip() == "HTC":
                    self.HTCList.append(shit.name)
                if x.strip() == "ITEM":
                    self.itemList.append(shit.name)
                    
    def removeShit(self, shit):
        if shit.name in self.shit:
            self.shit[shit.name].quantity -= shit.quantity
            if self.shit[shit.name].quantity <= 0:
                del self.shit[shit.name]
                if self.WTCList.count(shit.name) > 0:
                    self.WTCList.remove(shit.name)
                if self.HTCList.count(shit.name) > 0:
                    self.HTCList.remove(shit.name)
                if self.itemList.count(shit.name) > 0:
                    self.itemList.remove(shit.name)                         
        else:
            return -1 #this should not happen
                                              
