import Attributes
import Creature
import pygame
pygame.font.init()

def loadPlayerGraphics(graphicsData, name, skin):
    graphicsData.loadTexture(name+"_"+skin,"images/characters/" + name + "/" + skin + "/" + name + "_" + skin + ".png", -1)
    for y in range(0,4):
        for x in range(0,4):
            graphicsData.spriteRects[name+"_"+skin].append(pygame.rect.Rect(x*24,y*48,24,48)) 
    graphicsData.loadTexture(name+"_"+skin+"-20","images/characters/" + name + "/" + skin + "/" + name + "_" + skin + "-20.png", -1)
    for y in range(0,4):
        for x in range(0,4):
            graphicsData.spriteRects[name+"_"+skin+"-20"].append(pygame.rect.Rect(x*24,y*48,24,48)) 
    graphicsData.loadTexture(name+"_"+skin+"-40","images/characters/" + name + "/" + skin + "/" + name + "_" + skin + "-40.png", -1)
    for y in range(0,4):
        for x in range(0,4):
            graphicsData.spriteRects[name+"_"+skin+"-40"].append(pygame.rect.Rect(x*24,y*48,24,48)) 
    graphicsData.loadTexture(name+"_"+skin+"-60","images/characters/" + name + "/" + skin + "/" + name + "_" + skin + "-60.png", -1)
    for y in range(0,4):
        for x in range(0,4):
            graphicsData.spriteRects[name+"_"+skin+"-60"].append(pygame.rect.Rect(x*24,y*48,24,48)) 
    graphicsData.loadTexture(name+"_"+skin+"-80","images/characters/" + name + "/" + skin + "/" + name + "_" + skin + "-80.png", -1)
    for y in range(0,4):
        for x in range(0,4):
            graphicsData.spriteRects[name+"_"+skin+"-80"].append(pygame.rect.Rect(x*24,y*48,24,48))                         

class PlayerData(Creature.Creature):
    def __init__(self):
        Creature.Creature.__init__(self, "Rena")
        self.facing = 0
        self.collisionRect = pygame.Rect(288, 216, 24, 24)
        self.font = pygame.font.Font(None, 24)
        self.currentSkin = None
        self.equipment = []
        self.alive = True
    
    def setFacing(self, facing):
        self.facing = facing    
        
    def display(self, displayInfo, graphicsData):        
        playerSurface =  graphicsData.textures[self.currentSkin][0]
        playerSprite = graphicsData.spriteRects[self.currentSkin][self.facing + 1]
        displayInfo.getScreen().blit(playerSurface,(self.position.X,self.position.Y), playerSprite)
        #displayInfo.getScreen().blit(self.font.render(str(self.facing), 0, (255,255,255)), (self.position.X,self.position.Y))   
        
        
