import random
import os, pygame
from pygame.locals import *
import pygame.time
import ImageData
pygame.init()
import DisplayInfo
import PlayerData
import Map
import TextBox
import Creature
import GlobalData
import Attributes
import TeamData
import Item
import Battle
import StartMenu



class GameLoop:
    def __init__(self):
        self.displayInitialized = 0
        self.display = DisplayInfo.DisplayInfo()
        self.timer = pygame.time.Clock()
        self.player = PlayerData.PlayerData()
        self.team = TeamData.TeamData()
        self.maps = dict()
        
    

    def initDisplay(self):
        self.display.createScreen()
        self.displayInitilized = 1
        self.textureManager = ImageData.ImageData()
    

    def mainloop(self):
        if (self.displayInitialized==0):
            self.initDisplay()
            self.initPlayer()
        pygame.key.set_repeat(75, 75)       
        self.team.add(self.player)
        TextBox.loadTextImages(self.textureManager, 3, 3, -1)
        Battle.loadBattleTextures(self.textureManager)
        Creature.loadCreatureImages(self.textureManager)
        Map.loadTileSet("Exterior_Town1.png", self.textureManager, 30, 16)
        Map.loadTileSet("Interior_Town1.png", self.textureManager, 30, 16)
        Map.loadTileSet("Interior_Cave1.png", self.textureManager, 30, 16)
        self.map = Map.Map("Exterior_Town1", self.textureManager, self.display, "Exterior_Town1-6", 30, 30)
        self.maps["Exterior_Town1"] = [self.map] 
        timer = pygame.time.get_ticks()
        timeOffset = 0.00
 

        while not GlobalData.quitFlag:
            for e in pygame.event.get():
                if e.type == QUIT:
                    GlobalData.quitFlag = 1
                    return
                self.playerInput(e)
                pygame.event.pump()     
            self.drawWorld()
            self.printFPS()
            self.flipScreenBuffer()
            self.timer.tick(12)


 
    def printFPS(self):
        pygame.font.init()
        self.font = pygame.font.Font(None, 24)
        self.display.getScreen().blit(self.font.render(str(self.timer.get_fps()), 0, (255,255,255)), (24,24))
        self.display.getScreen().blit(self.font.render("X:" + str(self.map.getXoff()/24), 0, (255,255,255)), (24,48))
        self.display.getScreen().blit(self.font.render("Y:" + str(self.map.getYoff()/24), 0, (255,255,255)), (24,72))
        self.display.getScreen().blit(self.font.render("PrevX:" + str(self.map.prevXoff/24 - 1), 0, (255,255,255)), (24,96))
        self.display.getScreen().blit(self.font.render("PrevY:" + str(self.map.prevYoff/24 - 1), 0, (255,255,255)), (24,120))
        self.display.getScreen().blit(self.font.render("Monsters:" + str(self.map.hasMonsters), 0, (255,255,255)), (24,144))
        
    def flipScreenBuffer(self):
        pygame.display.flip()

    def playerInput(self, event):
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                if (self.map.getYoff() % 24) is not 0:
                    return
                if (self.map.getXoff() % 24) is not 0:
                    return    
                self.player.setFacing(12)
                for x in self.map.collisionRects:
                    for y in x:
                        if y.colliderect(self.player.collisionRect) and (y.top == 215) and (y.right == 289):
                            return
                self.map.setXYoff(self.map.getXoff() + 6,self.map.getYoff())

            elif event.key == K_RIGHT:
                if (self.map.getYoff() % 24) is not 0:
                    return
                if (self.map.getXoff() % 24) is not 0:
                    return    
                self.player.setFacing(4)
                for x in self.map.collisionRects:
                    for y in x:
                        if y.colliderect(self.player.collisionRect) and (y.top == 215) and (y.left == 311):
                            return
                self.map.setXYoff(self.map.getXoff() - 6,self.map.getYoff())
                   
            elif event.key == K_UP:
                if (self.map.getXoff() % 24) is not 0:
                    return
                if (self.map.getYoff() % 24) is not 0:
                    return    
                self.player.setFacing(0)
                for x in self.map.collisionRects:
                    for y in x:
                        if y.colliderect(self.player.collisionRect) and (y.left == 287) and (y.bottom == 217):
                            return
                self.map.setXYoff(self.map.getXoff(), self.map.getYoff() + 6)
  
            elif event.key == K_DOWN:

                if (self.map.getXoff() % 24) is not 0:
                    return
                if (self.map.getYoff() % 24) is not 0:
                    return    
                self.player.setFacing(8)
                for x in self.map.collisionRects:
                    for y in x:
                        if y.colliderect(self.player.collisionRect) and (y.left == 287) and (y.top == 239):
                            return
                self.map.setXYoff(self.map.getXoff(), self.map.getYoff() - 6)
            self.mods =  pygame.key.get_mods()       
            if event.key == K_RETURN and (self.mods == 4160 or self.mods == 20480 or self.mods == 256 or self.mods == 512):
                if self.display.isFullscreen == 0:   
                    self.display.isFullscreen = 1
                    self.display.createScreen()
                else:
                    self.display.isFullscreen = 0
                    self.display.createScreen()
            elif event.key == K_RETURN:
                #print len(self.map.allTiles[4][4].contents)
                if self.player.facing is 4 and self.map.currentPiece.array[13][9].text != "":
                    self.textBox(self.display, self.textureManager, 48, 48, self.map.currentPiece.array[13][9].text)
                    if len(self.map.currentPiece.array[13][9].contents) != 0:
                        self.map.drawMap()  
                        self.player.display(self.display, self.textureManager)
                        self.gotItem(self.display, self.textureManager, 48, 48, self.map.currentPiece.array[13][9])
                elif self.player.facing is 8 and self.map.currentPiece.array[12][10].text != "":
                    self.textBox(self.display, self.textureManager, 48, 48, self.map.currentPiece.array[12][10].text)
                    if len(self.map.currentPiece.array[12][10].contents) != 0:
                        self.map.drawMap()  
                        self.player.display(self.display, self.textureManager)
                        self.gotItem(self.display, self.textureManager, 48, 48, self.map.currentPiece.array[12][10])
                elif self.player.facing is 12 and self.map.currentPiece.array[11][9].text != "":
                    self.textBox(self.display, self.textureManager, 48, 48, self.map.currentPiece.array[11][9].text)
                    if len(self.map.currentPiece.array[11][9].contents) != 0:
                        self.map.drawMap()  
                        self.player.display(self.display, self.textureManager)
                        self.gotItem(self.display, self.textureManager, 48, 48, self.map.currentPiece.array[11][9])
                elif self.player.facing is 0 and self.map.currentPiece.array[12][8].text != "":
                    self.textBox(self.display, self.textureManager, 48, 48, self.map.currentPiece.array[12][8].text)
                    if len(self.map.currentPiece.array[12][8].contents) != 0:
                        self.map.drawMap()  
                        self.player.display(self.display, self.textureManager)
                        self.gotItem(self.display, self.textureManager, 48, 48, self.map.currentPiece.array[12][8])
            elif event.key == 105:
                self.startMenu()
                                           
            if event.key > 272 and event.key < 277:
                self.map.drawMap()
                self.player.setFacing(self.player.facing + 1)
                self.player.display(self.display, self.textureManager)
                self.printFPS()                
                self.flipScreenBuffer()
                pygame.time.delay(50)         

    def battle(self):
        self.instance = Battle.Battle(self.textureManager, self.display, self.map, self.team, self.player)
        self.instance.battleMain()
                        
    def portal(self):
        self.list = self.map.currentPiece.array[12][9].portal.split(';')
        self.mapName = self.list[0]            
        self.startPiece = self.list[1]
        self.xPiece = int(self.list[2])
        self.yPiece = int(self.list[3])
        if self.mapName not in self.maps:   
            self.map = Map.Map(self.mapName, self.textureManager, self.display, self.startPiece, self.xPiece, self.yPiece)
            self.maps[self.mapName] = [self.map]
        else:
            self.map = self.maps[self.mapName][0]
            self.map.startPieceOffsetX = self.xPiece
            self.map.startPieceOffsetY = self.yPiece 
            self.map.startPieceName = self.startPiece       
        #self.display.getScreen().fill((0,0,0))
        for x in range(-1,26):
            for y in range(-1,20):
                self.map.currentPiece.array[x][y] = self.map.allTiles[-self.map.Xoff/24 + x + self.map.startPieceOffsetX][-self.map.Yoff/24 + y + self.map.startPieceOffsetY]        
        #print str(self.map.currentPiece)    
                
    def initPlayer(self):
        PlayerData.loadPlayerGraphics(self.textureManager, "rena", "nightgown")
        self.player.currentSkin = "rena_nightgown"
        self.player.setPosition(288, 192)
        self.player.display(self.display, self.textureManager)
        
    def drawWorld(self):
        
        #print self.map.objectManager.collisionRects
        if (self.map.getXoff() % 24) is not 0:
            if self.player.facing > 3 and self.player.facing < 7:
                self.player.setFacing(self.player.facing + 1)
                self.map.setXYoff(self.map.getXoff() - 6,self.map.getYoff())
                self.map.drawMap()

            elif self.player.facing is 7:
                self.player.setFacing(4)
                self.map.setXYoff(self.map.getXoff() - 6,self.map.getYoff())
                self.map.drawMap()
                if self.map.currentPiece.array[12][9].portal != "":
                    self.portal()
                if self.map.hasMonsters == True:
                    random.seed()
                    self.chance = random.randint(0,self.map.freq)
                    #print self.chance
                    if self.chance == 0:
                        self.battle()    

            elif self.player.facing > 11 and self.player.facing < 15:
                self.player.setFacing(self.player.facing + 1)
                self.map.setXYoff(self.map.getXoff() + 6,self.map.getYoff())
                self.map.drawMap()

            elif self.player.facing is 15:
                self.player.setFacing(12)
                self.map.setXYoff(self.map.getXoff() + 6,self.map.getYoff())
                self.map.drawMap()
                if self.map.currentPiece.array[12][9].portal != "":
                    self.portal()
                if self.map.hasMonsters == True:
                    random.seed()
                    self.chance = random.randint(0,self.map.freq)
                    #print self.chance
                    if self.chance == 0:
                        self.battle()              
            
        elif (self.map.getYoff() % 24) is not 0:
            if self.player.facing > 7 and self.player.facing < 11:
                self.player.setFacing(self.player.facing + 1)
                self.map.setXYoff(self.map.getXoff(), self.map.getYoff() - 6)
                self.map.drawMap()

            elif self.player.facing is 11:
                self.player.setFacing(8)
                self.map.setXYoff(self.map.getXoff(), self.map.getYoff() - 6)
                self.map.drawMap()
                if self.map.currentPiece.array[12][9].portal != "":
                    self.portal()
                if self.map.hasMonsters == True:
                    random.seed()
                    self.chance = random.randint(0,self.map.freq)
                    #print self.chance
                    if self.chance == 0:
                        self.battle()        
   
            elif self.player.facing < 3:
                self.player.setFacing(self.player.facing + 1)
                self.map.setXYoff(self.map.getXoff(), self.map.getYoff() + 6)
                self.map.drawMap()

            elif self.player.facing is 3:
                self.player.setFacing(0)
                self.map.setXYoff(self.map.getXoff(), self.map.getYoff() + 6)
                self.map.drawMap()
                if self.map.currentPiece.array[12][9].portal != "":
                    self.portal()
                if self.map.hasMonsters == True:
                    random.seed()
                    self.chance = random.randint(0,self.map.freq)
                    #print self.chance
                    if self.chance == 0:
                        self.battle()    
                    
        
        self.map.drawMap()  
        self.player.display(self.display, self.textureManager)

    def textBox(self, display, graphicsData, x, y, text):
        self.box = TextBox.TextBox(display, graphicsData, x, y, text)
        self.open = True
        while self.open:
            self.box.draw()
            pygame.display.flip()       
            for e in pygame.event.get():
                if e.type == QUIT:
                    GlobalData.quitFlag = 1
                    return
                elif e.type == KEYDOWN:
                    if e.key == K_RETURN:
                        self.open = False            

    def gotItem(self, display, graphicsData, x, y, mapTile):
        for z in mapTile.contents:
            self.player.shit.append(z)
            self.box = TextBox.TextBox(self.display, self.textureManager, x, y, "You receieved " + z.name + ".")
            mapTile.contents.remove(z)
            self.open = True
            while self.open:
                self.box.draw()
                pygame.display.flip()       
                for e in pygame.event.get():
                    if e.type == QUIT:
                        GlobalData.quitFlag = 1
                        return
                    elif e.type == KEYDOWN:
                        if e.key == K_RETURN:
                            self.open = False


    def startMenu(self):
        self.instance = StartMenu.StartMenu(self.textureManager, self.display, self.map, self.team, self.player)
        self.instance.menuMain()
                                              
                        
if __name__ == "__main__":                                                   
    game = GameLoop()
    #print "Default Font: %s"%(pygame.font.get_default_font())
    #print "All fonts:\n-------------"
    #print pygame.font.get_fonts()
    game.mainloop()
