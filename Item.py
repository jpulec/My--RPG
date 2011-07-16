import Position
import GameObject
import GlobalData

class Item(GameObject.GameObject):
    def __init__(self, name):
        GameObject.GameObject.__init__(self)
        self.name = name
        self.types = GlobalData.itemData[self.name][0].split(',')
        self.size = int(GlobalData.itemData[self.name][1])
        self.ATK = int(GlobalData.itemData[self.name][2])
        self.DEF = int(GlobalData.itemData[self.name][3])
        self.WTC = int(GlobalData.itemData[self.name][4])
        self.HTC = int(GlobalData.itemData[self.name][5])
        self.ACC = int(GlobalData.itemData[self.name][6])
        self.USE = "NA"    
        if GlobalData.itemData[self.name][7].strip() != "NA":
            self.USE = int(GlobalData.itemData[self.name][7])   
