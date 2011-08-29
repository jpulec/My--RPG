import string
import GameObject
import Attributes
import GlobalData


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

    def getStats(self):
        self.attributes.stats = GlobalData.statsData[self.name]

    def getMaxHitPoints(self):
        return self.attributes.maxHP()

    def getCurrentHitPoints(self):
        return self.HP
            
    def getAttributes(self):
        return self.attributes

    def display(self, x, y):
        self.image = GlobalData.textureManager.textures[self.name][0]    
        GlobalData.display.getScreen().blit(self.image, (x, y))            

            
        





    

    
        
        
    
    

