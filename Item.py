import Position
import GameObject
import GlobalData

data = GlobalData.itemData

class Item(GameObject.GameObject):
    def __init__(self, name):
        GameObject.GameObject.__init__(self)
        self.name = name
        self.types = data[self.name][0].split(',')
        self.size = int(data[self.name][1])
        self.ATK = int(data[self.name][2])
        self.DEF = int(data[self.name][3])
        self.WTC = int(data[self.name][4])
        self.HTC = int(data[self.name][5])
        self.ACC = int(data[self.name][6])
        self.USE = "NA"    
        if data[self.name][7].strip() != "NA":
            self.USE = int(data[self.name][7])   
