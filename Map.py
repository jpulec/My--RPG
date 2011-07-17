import pygame
import ImageData
import DisplayInfo
import random
import GameObject
import string
import pygame.time
import GlobalData
import Item


def loadTileSet(mapName, xNum, yNum, alpha = None):
    GlobalData.textureManager.loadTexture(mapName,"images/" + mapName, alpha)
    for y in range(0,xNum):
        for x in range(0,yNum):
            GlobalData.textureManager.spriteRects[mapName].append(pygame.rect.Rect(x*24,y*24,24,24))
            
def loadBattleBG(mapName, alpha = None):
    GlobalData.textureManager.loadTexture("bg", "images/battle/bg/" + mapName +str(".png"), alpha)            

class MapTile:
    def __init__(self):

        self.text = ""
        self.name = ""
        self.collision = 0
        self.rect = None
        self.backRect = None
        self.tileSet = None
        self.tileSetName = ""
        self.contents = []
        self.visible = 0
        self.portal = ""
    
    def __str__(self):
        if self.rect is not None:
            if self.rect.top == 0:
                return "[]"
            else:
                return "[!]"
        return "{}"                    
    
    def displayTile(self, x, y):
        if self.tileSetName != "":
            #print self.name
            if self.backRect is not None:
                GlobalData.display.getScreen().blit(GlobalData.textureManager.textures[self.tileSetName][0], (x,y), self.backRect)
            #GlobalData.display.getScreen().fill((0,0,0), pygame.rect.Rect(x,y,24,24)) 
            GlobalData.display.getScreen().blit(GlobalData.textureManager.textures[self.tileSetName][0], (x, y), self.rect)
    
    def setRect(self, rect):
        self.rect = rect
        
    def setTileSet(self, tileSet):
        self.tileSet = tileSet
    
    def getRect(self):
        return self.rect
    
    def getTileSet(self):
        return self.tileSet
    
    def setTileSetName(self, name):
        self.tileSetName = name     
    
    def getName(self):
        return self.name
    
    def setName(self, name):
        self.name = name    
    
    def getCollision(self):
        return self.collision
    
    def setCollision(self, collision):
        self.collision = collision
    
    def setText(self, text):
        self.text = text
        
    def getText(self):
        return self.text
    
    def getContents(self):
        return self.contents
        
    def setContents(self, contents):
        self.contents = contents
    
    def isVisible(self):
        return self.visible == 1       

class MapPiece:
    def __init__(self, piece, name):
        self.array = piece
        self.name = name
        #print self.collisions
        
    def __str__(self):
        for y in range(19):
            for x in range(25):
                if x != 24: 
                    print str(self.array[x][y]) + "\t",
                else:
                    print str(self.array[x][y])
        return ""                        
                      
                       
    def drawRow(self, row, xOff, yOff):
        for y in range(19):
            self.array[row][y].displayTile(xOff + row*24, yOff + y*24)
                                
    def draw(self, Xoff, Yoff):
        #print Xoff
        #print Yoff
        for x in range(-1,26):
            for y in range(-1,20):
                self.array[x][y].displayTile(x*24 + Xoff, y*24 + Yoff)
    
    def getName(self):
        return self.name            
                    
class Map:
    def __init__(self, mapName, startPieceName, startPieceOffsetX, startPieceOffsetY):

        self.name = mapName
        self.mapPieceWidth = None
        self.mapPieceLength = None
        self.hasMonsters = None
        self.monsters = None
        self.numMonsters = None
        self.freq = None
        self.getMapData()
        self.objectManager = ObjectManager()
        self.collisionRects = [[pygame.Rect(0,0,0,0) for i in range(19)] for j in range(25)]
        self.mapPieces = [[MapTile() for i in range(self.mapPieceWidth)] for j in range(self.mapPieceLength)]
        self.currentPiece = None
        self.startPieceOffsetX = startPieceOffsetX
        self.startPieceOffsetY = startPieceOffsetY 
        self.startPieceName = startPieceName
        self.prevXoff = 0
        self.prevYoff = 0
        self.Xoff = 0
        self.Yoff = 0
        self.loadMap(mapName)
        self.allTiles = [[MapTile() for i in range(30*self.mapPieceWidth)] for j in range(30*self.mapPieceLength)]
        self.getAllTiles()
        self.getCollisionRects()
        if self.hasMonsters == True:
            loadBattleBG(mapName)
            #print GlobalData.textureManager.textures["bg"]
            self.battleBG = GlobalData.textureManager.textures["bg"]
            #self.monsters = ["creep", "goblin"]
            
    def getMapData(self):
        self.mapPieceWidth = int(GlobalData.mapsData[self.name][0])
        self.mapPieceLength = int(GlobalData.mapsData[self.name][1])
        self.hasMonsters = GlobalData.mapsData[self.name][2] == "True"
        self.monsters = string.split(GlobalData.mapsData[self.name][3], ',')
        #self.monsters[len(self.monsters)-1] = self.monsters[len(self.monsters)-1]      Useless?
        self.numMonsters = int(GlobalData.mapsData[self.name][4])
        self.freq = int(GlobalData.mapsData[self.name][5])                   
    
    def getCollisionRects(self):
        for x in range(25):
            for y in range(19):
                if self.currentPiece.array[x][y].getCollision() == 1:
                    self.collisionRects[x][y] = (pygame.Rect(x*24 - 1, y*24 - 1, 26, 26))
                else:
                    self.collisionRects[x][y] = (pygame.Rect(0, 0, 0, 0))    
        
    def printCollisionRects(self):
        for y in range(19):
            for x in range(25):
                if x != 24: 
                    print str(self.collisionRects[x][y].top) + "\t",
                else:
                    print str(self.collisionRects[x][y].top)
        return ""                        
 
    def getAllTiles(self):
        self.xCount = 0
        self.yCount = 0
        self.yBase = -1
        self.xBase = -1
        #self.count = 0
        for y in range(self.mapPieceLength):
            self.yBase = -1
            for x in range(self.mapPieceWidth):
                self.xCount = self.xBase + 1
                for v in range(30):
                    self.yCount = self.yBase + 1
                    for z in range(30):
                        #print "V:" + str(v)
                        #print "X:" + str(x)
                        #print "Y:" + str(y)
                        #print "xCount:" + str(self.xCount)
                        #print "yCount:" + str(self.yCount)
                        #print "xBase:" + str(self.xBase)
                        #print "yBase:" + str(self.yBase)
                        #print self.mapPieces[x][y].array[v][z].getName()
                        self.allTiles[self.xCount][self.yCount] = self.mapPieces[x][y].array[v][z]
                        self.yCount += 1
                        #self.count += 1        
                    self.xCount += 1
                self.yBase += 30
            self.xBase += 30                
        #print self.count                   
                       
        
    def loadMapPiece(self, name, xNum, yNum, mapPieceName):
        self.file = "data/" + name[:-2] + "/" + name
        self.workingMap = [[MapTile() for i in range(30)] for j in range(30)]
        self.tmpList = []
        self.fileToLoad = open(self.file, 'r')
        for x in range(30):
            for y in range(30):               
                self.tmpList = string.split(self.fileToLoad.readline(), ',')
                self.workingMap[x][y].text = self.tmpList[0]
                self.workingMap[x][y].name = self.tmpList[1]
                self.workingMap[x][y].collision = int(self.tmpList[2])
                if self.tmpList[3] == "None":
                    self.workingMap[x][y].rect = None
                    continue
                elif self.tmpList[3] != "None":        
                    self.workingMap[x][y].rect = pygame.Rect(int(self.tmpList[3]), int(self.tmpList[4]),24,24)    
                if self.tmpList[5] != "":
                    self.workingMap[x][y].tileSetName = self.tmpList[5]
                    self.workingMap[x][y].tileSet = GlobalData.textureManager.textures[self.tmpList[5]][0]
                self.splitList = self.tmpList[6].split(';')
                for z in self.splitList:
                    if self.splitList[0] != "":
                        self.workingMap[x][y].contents.append(Item.Item(z))                                   
                self.workingMap[x][y].portal = self.tmpList[7]
                if self.tmpList[8][:-1] == "None":
                    self.workingMap[x][y].backRect = None
                    continue
                else:    
                    self.workingMap[x][y].backRect = pygame.Rect(int(self.tmpList[8]), int(self.tmpList[9]), 24, 24) 
                          
        self.fileToLoad.close()
        self.mapPieces[xNum][yNum] = MapPiece(self.workingMap, mapPieceName)    
            
               
        
    def drawMap(self):
        if self.Xoff != self.prevXoff:
            if self.Xoff % 24 == 0:
                for x in range(-1,26):
                    for y in range(-1,20):
                        self.currentPiece.array[x][y] = self.allTiles[-self.Xoff/24 + x + self.startPieceOffsetX][-self.Yoff/24 + y + self.startPieceOffsetY]
        if self.Yoff != self.prevYoff:
            if self.Yoff % 24 == 0:
                for x in range(-1,26):
                    for y in range(-1,20):
                        self.currentPiece.array[x][y] = self.allTiles[-self.Xoff/24 + x + self.startPieceOffsetX][-self.Yoff/24 + y + self.startPieceOffsetY]
                        
                #print "Y+1" 
        #self.currentPiece.drawRow(24, self.Xoff, self.Yoff)
        #self.currentPiece.drawRow(25, self.Xoff, self.Yoff)
        #self.printCollisionRects()
        #print "X:" + str(self.Xoff)
        #print "PrevX:" + str(self.prevXoff)         
        if self.Xoff > self.prevXoff:
            GlobalData.display.getScreen().fill((0,0,0))    
            self.currentPiece.draw((self.Xoff%24), self.Yoff%24)
            #print "Left"
        elif self.Xoff < self.prevXoff:
            #print 24 - (self.Xoff%24)
            GlobalData.display.getScreen().fill((0,0,0))        
            self.currentPiece.draw(-(24-(self.Xoff%24)), self.Yoff%24)
            #print "Right"
        elif self.Yoff < self.prevYoff:
            GlobalData.display.getScreen().fill((0,0,0))        
            self.currentPiece.draw(self.Xoff%24, -(24 - (self.Yoff%24)))
            #print "Up"
        elif self.Yoff > self.prevYoff:
            GlobalData.display.getScreen().fill((0,0,0))        
            self.currentPiece.draw(self.Xoff%24, (self.Yoff%24))
            #print "Down"
        elif self.Xoff%24 == 0 and self.Yoff%24 == 0:
            GlobalData.display.getScreen().fill((0,0,0))        
            self.currentPiece.draw(self.Xoff%24, self.Yoff%24)
            #print "Stop"  
        
        self.prevYoff = self.Yoff
        self.prevXoff = self.Xoff
        self.getCollisionRects()                    
        #print str(self.currentPiece)
        
    
        
    #def drawRects(self):
    #    for x in self.collisionRects:
    #        for y in x:
                
                                
    
    def loadMap(self, mapName):
        self.count = 0     
        for x in range(self.mapPieceWidth):
            #self.count = 0
            for y in range(self.mapPieceLength): 
                if self.count == 7:
                    self.count = 0
                self.loadMapPiece(mapName + str("-") + str(self.count), x, y, mapName + str("-") + str(self.count))
                if mapName + str("-") + str(self.count) == self.startPieceName:
                    self.currentPiece = self.mapPieces[x][y]
                self.count += 1
                #print self.count
        #print str (self.currentPiece)                
    
    def setXYoff(self, x, y):
        self.prevXoff = self.Xoff
        self.prevYoff = self.Yoff
        self.Xoff = x
        self.Yoff = y
        
    def getXoff(self):
        return self.Xoff
        
    def getYoff(self):
        return self.Yoff
    
            
                   

class Object(GameObject.GameObject):
    def __init__(self, graphicsData, name, surf, objectID, collision):
        GameObject.GameObject.__init__(self)
        self.name = name
        self.surf = surf
        self.tileSurface = graphicsData.textures[name + str(".png")][0]
        self.tileSprite = graphicsData.spriteRects[name + str(".png")][objectID]
        self.collision = collision                   
        
    def render(self,x,y):
        rect = self.surf.blit(self.tileSurface,(x,y), self.tileSprite)

        
class ObjectManager:
    def __init__(self):
        self.surf = GlobalData.display.getScreen()
        self.objects = []
        self.collisionRects = []
        self.Xoff = 0
        self.Yoff = 0
        
        
    def makeObjects(self, low, high, collision, name):
        for x in range(low, high):
            self.objects.append(Object(name, self.surf, x, collision))    
        
                
    def drawObjects(self):
        self.tmpCollisions = []
        #for x in range(1, 50):
         #   self.objects[x].render(32*x + self.Xoff, 32*x + self.Yoff)
          #  self.objects[x].setPosition(32*x + self.Xoff, 32*x + self.Yoff)
            
           # if self.objects[x].collision == 1:
            #    self.tmpCollisions.append(pygame.Rect(32*x + self.Xoff - 1, 32*x + self.Yoff -1, 32 + 2, 32 + 2))
        self.collisionRects = self.tmpCollisions

                
    
    def setXYoff(self, x, y):
        self.Xoff = x
        self.Yoff = y
        
    def getXoff(self):
        return self.Xoff
        
    def getYoff(self):
        return self.Yoff                                     
                      
                                
        
        
        
        
        
        
        
        
        
        
        
                
                     
