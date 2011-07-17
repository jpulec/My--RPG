import string
import GameObject
import Attributes
import GlobalData
import Game


def loadCreatureImages():
    file1 = "data/Monsters.data"
    fileToLoad = open(file1, 'r')
    for lines in fileToLoad:
        GlobalData.textureManager.loadTexture(lines[:-1], "images/battle/monsters/" + lines[:-1] + ".png")                    
    fileToLoad.close()

class Creature(GameObject.GameObject):
    def __init__(self, name):
        GameObject.GameObject.__init__(self)
        self.name = name
        self.attributes = Attributes.Attributes() 
        self.getStats()  
        self.HP = int(self.attributes.maxHP())
        self.shit = []
        self.carryAbility = 0
        #self.image = Game.textureManager.textures[self.name][0]

    def getStats(self):
        self.attributes.stats = GlobalData.statsData[self.name]

    def getMaxHitPoints(self):
        return self.attributes.maxHP()

    def getCurrentHitPoints(self):
        return self.HP
            
    def getAttributes(self):
        return self.attributes

    def display(self, array, monNum):
        self.image = GlobalData.textureManager.textures[self.name][0]
        self.num = monNum
        self.x = self.num/3
        self.y = self.num%3
        self.array = array
        if self.x == 0:
            if self.y == 0:
                self.array[0][0] = self
                GlobalData.display.getScreen().blit(self.image, (80, 96))
            if self.y == 1:
                self.array[0][1] = self
                GlobalData.display.getScreen().blit(self.image, (168+8, 96))
            if self.y == 2:
                self.array[0][2] = self
                GlobalData.display.getScreen().blit(self.image, (212+56, 96))         
        if self.x == 1:
            if self.y == 0:
                self.array[1][0] = self
                GlobalData.display.getScreen().blit(self.image, (80, 144 + 24))
            if self.y == 1:
                self.array[1][1] = self
                GlobalData.display.getScreen().blit(self.image, (168+8, 144 + 24))
            if self.y == 2:
                self.array[1][2] = self
                GlobalData.display.getScreen().blit(self.image, (212+56, 144 + 24)) 
        if self.x == 2:
            if self.y == 0:
                self.array[2][0] = self
                GlobalData.display.getScreen().blit(self.image, (80, 196 + 48))
            if self.y == 1:
                self.array[2][1] = self
                GlobalData.display.getScreen().blit(self.image, (168+8, 196 + 48))
            if self.y == 2:
                self.array[2][2] = self
                GlobalData.display.getScreen().blit(self.image, (212+56, 196 + 48)) 
                                         
            
        





    

    
        
        
    
    

