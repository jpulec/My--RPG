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



class GameLoop:
    def __init__(self):
        self.displayInitialized = 0
        self.quitFlag = 0
        self.display = DisplayInfo.DisplayInfo()
        self.timer = pygame.time.Clock()
        self.player = PlayerData.PlayerData()
        self.team = TeamData.TeamData()
        self.maps = dict()
        
        
    

    def initDisplay(self):
        self.display.createScreen()
        self.displayInitilized = 1
        self.textureManager = ImageData.ImageData()

    def loadBattleTextures(self):
        self.textureManager.loadTexture("battle","images/battle/BattleCursor.png", -1)
        for y in range(4):
            for x in range(2):
                self.textureManager.spriteRects["battle"].append(pygame.rect.Rect(x*24,y*24,24,24))
    

    def mainloop(self):
        if (self.displayInitialized==0):
            self.initDisplay()
            self.initPlayer()
        pygame.key.set_repeat(75, 75)       
        self.team.add(self.player)
        TextBox.loadTextImages(self.textureManager, 3, 3, -1)
        self.loadBattleTextures()
        Creature.loadCreatureImages(self.textureManager)
        Map.loadTileSet("Exterior_Town1.png", self.textureManager, 30, 16)
        Map.loadTileSet("Interior_Town1.png", self.textureManager, 30, 16)
        Map.loadTileSet("Interior_Cave1.png", self.textureManager, 30, 16)
        self.map = Map.Map("Exterior_Town1", self.textureManager, self.display, "Exterior_Town1-6", 30, 30)
        self.maps["Exterior_Town1"] = [self.map] 
        timer = pygame.time.get_ticks()
        timeOffset = 0.00
 

        while not self.quitFlag:
            for e in pygame.event.get():
                if e.type == QUIT:
                    self.quitFlag = 1
                    return
                self.playerInput(e)
                pygame.event.pump()     
            self.drawWorld()
            self.printFPS()
            self.flipScreenBuffer()
            self.timer.tick(12)


    def drawStats(self):
        pygame.font.init()
        self.font = pygame.font.Font(None, 24)
        self.display.getScreen().blit(self.font.render(str(Attributes.attributeNames), 0, (255,255,255)), (24,24))
        self.display.getScreen().blit(self.font.render(str(self.player.attributes.stats), 0, (255,255,255)), (24,48))
        self.display.getScreen().blit(self.font.render("HP:" + str(self.player.HP), 0, (255,255,255)), (24,72))

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
        self.numMonsters = random.randint(1,self.map.numMonsters)
        self.monsterNames = []
        self.monsters = []
        for x in range(self.numMonsters):
            self.monster = random.randint(0, len(self.map.monsters)-1)
            self.monsterNames.append(self.map.monsters[self.monster])
        for x in self.monsterNames:
            self.monsters.append(Creature.Creature(x))
        self.monArray = [[None for i in range(3)] for j in range(3)]
        self.monArrayNum = 0            
        self.battleMenu = TextBox.BattleMenu(self.display, self.textureManager, 360, 312, ["Attack", "WTC", "HTC", "Item", "Run"])
        self.battleBox = TextBox.BattleBox(self.display, self.textureManager)
        self.selection = 0
        self.battleBool = True
        self.display.getScreen().blit(self.textureManager.textures["bg"][0], (0,0))
        self.display.getScreen().blit(self.textureManager.textures[self.player.currentSkin][0], (504,96), self.textureManager.spriteRects[self.player.currentSkin][13])
        self.teamNum = 0
        self.selectedMember = self.team.team[self.teamNum]
        self.selectedMemNum = 13
        self.actions = []
        self.doActions = False
        while(self.battleBool):
            if self.doActions:
                while(len(self.actions)>0):
                    #print self.actions
                    self.highestSPD = 0
                    self.highestAction = None
                    for x in self.actions:
                        if x[0].attributes.stats[7] > self.highestSPD:
                            self.highestSPD = x[0].attributes.stats[7]
                            self.highestAction = x   
                    if self.highestAction[1] == "ATTACK":
                        self.attackTarget(self.highestAction[0], self.highestAction[2])
                    if self.highestAction[1] == "WTC":
                        self.WTCTarget(self.highestAction[0], self.highestAction[2], self.highestAction[3])
                    if self.highestAction[1] == "HTC":
                        self.HTCTarget(self.highestAction[0], self.highestAction[2], self.highestAction[3])
                    if self.highestAction[1] == "ITEM":
                        self.itemTarget(self.highestAction[0], self.highestAction[2], self.highestAction[3])
                    if self.highestAction[1] == "RUN":
                        self.run(self.highestAction[0])
                        if self.battleBool == False:
                            break        
                    self.actions.remove(self.highestAction)
                    self.display.getScreen().blit(self.textureManager.textures["bg"][0], (0,0))
                    for x in self.team.team:
                        if float(x.attributes.stats[0])*.8 <= x.HP:
                            if x.currentSkin.count('-') == 0:
                                x.currentSkin = x.currentSkin
                            else:
                                x.currentSkin = x.currentSkin[:-2]
                        elif float(x.attributes.stats[0])*.6 <= x.HP:
                            if x.currentSkin.count('-') == 0:
                                x.currentSkin = x.currentSkin + "-80"
                            else:
                                x.currentSkin = x.currentSkin[:-2] + "80"
                        elif float(x.attributes.stats[0])*.4 <= x.HP:
                            if x.currentSkin.count('-') == 0:
                                x.currentSkin = x.currentSkin + "-60"
                            else:
                                x.currentSkin = x.currentSkin[:-2] + "60" 
                        elif float(x.attributes.stats[0])*.2 <= x.HP:
                            if x.currentSkin.count('-') == 0:
                                x.currentSkin = x.currentSkin + "-40"
                            else:
                                x.currentSkin = x.currentSkin[:-2] + "40"
                        elif 0 <= x.HP:
                            if x.currentSkin.count('-') == 0:
                                x.currentSkin = x.currentSkin + "-20"
                            else:
                                x.currentSkin = x.currentSkin[:-2] + "20"                                     
                    for x in range(len(self.team.team)):
                         self.display.getScreen().blit(self.textureManager.textures[self.team.team[x].currentSkin][0], (504,96+x*32), self.textureManager.spriteRects[self.team.team[x].currentSkin][13])    
                    self.drawStats()
                    for x in self.monsters:
                        if x.HP <= 0:
                            self.battleBox.addText(x.name + " was defeated.")
                            self.monsters.remove(x)
                            for y in range(len(self.monArray)-1):
                                for z in self.monArray[y]:
                                    if z == x:
                                        self.monArray[y].remove(x)
                                    
                    if len(self.monsters) == 0:
                        self.battleBox.addText("Battle won!")
                        self.open = True
                        while self.open:      
                            for e in pygame.event.get():
                                if e.type == QUIT:
                                    self.quitFlag = 1
                                    return
                                elif e.type == KEYDOWN:
                                    if e.key == K_RETURN:
                                        self.open = False
                        #Won battle
                        return

                    for x in self.team.team:
                        if x.HP <= 0:
                            self.team.team.remove(x)
                    if len(self.team.team) == 0:
                        for x in self.monsters:
                            x.display(self.textureManager, self.display, self.monArray, self.monArrayNum)
                            self.monArrayNum += 1
                        self.monArrayNum = 0
                        self.battleBox.addText("Game Over...")
                        self.quitFlag = 1
                        self.open = True
                        while self.open:      
                            for e in pygame.event.get():
                                if e.type == QUIT:
                                    self.quitFlag = 1
                                    return
                                elif e.type == KEYDOWN:
                                    if e.key == K_RETURN:
                                        self.open = False
                                        return    
                    for x in self.monsters:
                        x.display(self.textureManager, self.display, self.monArray, self.monArrayNum)
                        self.monArrayNum += 1
                    self.monArrayNum = 0
                    self.battleBox.show()
                    self.battleMenu.show()
                    self.flipScreenBuffer()
                    self.open = True
                    while self.open:      
                        for e in pygame.event.get():
                            if e.type == QUIT:
                                self.quitFlag = 1
                                return
                            elif e.type == KEYDOWN:
                                if e.key == K_RETURN:
                                    self.open = False
                                    break
                        pygame.time.delay(300)
                        self.open = False            
                self.doActions = False                                    
            self.display.getScreen().blit(self.textureManager.textures["bg"][0], (0,0))
            if self.selectedMemNum != 17: 
                self.display.getScreen().blit(self.textureManager.textures[self.selectedMember.currentSkin][0], (504 - self.selectedMemNum%13*6,96), self.textureManager.spriteRects[self.selectedMember.currentSkin][self.selectedMemNum])
            else:
                self.display.getScreen().blit(self.textureManager.textures[self.selectedMember.currentSkin][0], (504 - 4*6,96), self.textureManager.spriteRects[self.selectedMember.currentSkin][13])    
            self.drawStats()
            #first player up
            #print self.monsters
            for x in self.monsters:
                if x.HP <= 0:
                    self.battleBox.addText(x.name + " was defeated.")
                    self.monsters.remove(x)
                    for y in range(len(self.monArray)-1):
                        for z in self.monArray[y]:
                            if z == x:
                                self.monArray[y].remove(x)
                            
            if len(self.monsters) == 0:
                self.battleBox.addText("Battle won!")
                self.open = True
                while self.open:      
                    for e in pygame.event.get():
                        if e.type == QUIT:
                            self.quitFlag = 1
                            return
                        elif e.type == KEYDOWN:
                            if e.key == K_RETURN:
                                self.open = False
                #Won battle
                return

            for x in self.team.team:
                if x.HP <= 0:
                    self.team.team.remove(x)
            if len(self.team.team) == 0:
                self.battleBox.addText("Game Over...")
                self.quitFlag = 1
                self.open = True
                while self.open:      
                    for e in pygame.event.get():
                        if e.type == QUIT:
                            self.quitFlag = 1
                            return
                        elif e.type == KEYDOWN:
                            if e.key == K_RETURN:
                                self.open = False
                                return    
            for x in self.monsters:
                x.display(self.textureManager, self.display, self.monArray, self.monArrayNum)
                self.monArrayNum += 1
            self.monArrayNum = 0
            self.battleBox.show()
            self.battleMenu.show()
            if self.selection == 0:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (442, 316), self.textureManager.spriteRects["battle"][1])
            elif self.selection == 1:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (442, 316+24), self.textureManager.spriteRects["battle"][1])
            elif self.selection == 2:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (442, 316+48), self.textureManager.spriteRects["battle"][1])
            elif self.selection == 3:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (442, 316+72), self.textureManager.spriteRects["battle"][1])
            elif self.selection == 4:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (442, 316+96), self.textureManager.spriteRects["battle"][1])
            self.flipScreenBuffer()
            #print self.selectedMemNum
            pygame.time.delay(75)
            if self.selectedMemNum < 16:
                self.selectedMemNum += 1
            else:
                self.selectedMemNum = 17    
            for e in pygame.event.get():
                if self.selectedMemNum != 17:
                    break
                if e.type == QUIT:
                    self.quitFlag = 1
                    return
                elif e.type == KEYDOWN:
                    if e.key == K_UP:
                        if self.selection == 0:
                            self.selection = 4
                        elif self.selection == 1:
                            self.selection = 0
                        elif self.selection == 2:
                            self.selection = 1
                        elif self.selection == 3:
                            self.selection = 2
                        elif self.selection == 4:
                            self.selection = 3    
                    elif e.key == K_DOWN:
                        if self.selection == 0:
                            self.selection = 1
                        elif self.selection == 1:
                            self.selection = 2
                        elif self.selection == 2:
                            self.selection = 3
                        elif self.selection == 3:
                            self.selection = 4
                        elif self.selection == 4:
                            self.selection = 0                        
                    elif e.key == K_END:
                        return
                    elif e.key == K_RETURN:
                        if self.selection == 0:
                            #print self.monArray[0]
                            #print self.monArray[1]
                            #print self.monArray[2]
                            self.attackSelected()
                            break
                        elif self.selection == 1:
                            self.WTC()
                            break 
                        elif self.selection == 2:
                            self.HTC()
                            break
                        elif self.selection == 3:
                            self.item()
                            break
                        elif self.selection == 4:
                            #self.run()
                            tmp = [self.selectedMember, "RUN"]
                            self.actions.append(tmp)
                            self.teamNum += 1
                            if self.teamNum == len(self.team.team):
                                self.enemyActions()                                
                                self.teamNum = 0
                                self.doActions = True
                            for x in range(4):    
                                self.display.getScreen().blit(self.textureManager.textures["bg"][0], (0,0))
                                self.display.getScreen().blit(self.textureManager.textures[self.selectedMember.currentSkin][0], (504 - (3-x)*6,96), self.textureManager.spriteRects[self.selectedMember.currentSkin][16-x])    
                                self.drawStats()   
                                for x in self.monsters:
                                    x.display(self.textureManager, self.display, self.monArray, self.monArrayNum)
                                    self.monArrayNum += 1
                                self.monArrayNum = 0
                                self.battleBox.show()
                                self.battleMenu.show()
                                pygame.time.delay(75)
                                self.flipScreenBuffer()
                            self.selectedMemNum = 13        
                            self.selectedMember = self.team.team[self.teamNum]
                            
                            break                                                                   
                pygame.event.pump()

    def enemyActions(self):
        #print "Enemy monsters"
        for x in self.monsters:
            #print x.name
            self.WTCList = []
            self.HTCList = []
            self.itemList = []
            self.num = 0
            self.itemTrue = False
            self.WTCTrue = False  
            for z in x.shit:
                for y in z.types:
                    if y.strip() == "WTC":
                        self.WTCList.append(z.name)
                for y in z.types:
                    if y.strip() == "HTC":
                        self.HTCList.append(z.name)
                for y in z.types:
                    if y.strip() == "ITEM":
                        self.itemList.append(z.name)
            if x.HP <= float(GlobalData.statsData[x.name][0])*.3:
                if len(self.HTCList) > 0:
                    self.rand = random.randint(0, len(self.HTCList)-1)
                    tmp = [x, "HTC", self.HTCList[rand], x] 
                    self.actions.append(tmp)
                    continue            
            if len(self.WTCList) > 0:
                self.randWTC = random.randin(0,len(self.WTCList)-1)
                self.num += 1
                self.WTCTrue = True
            if len(self.itemList) > 0:
                self.randItem = random.randint(0,len(self.itemList)-1)
                self.num += 1
                self.itemTrue = True
            self.act = random.randint(0,self.num)
            self.actedOn = random.randint(0,len(self.team.team)-1)
            
            if self.act == 0:
                tmp = [x, "ATTACK", self.team.team[self.actedOn]]
                self.actions.append(tmp)
            elif self.act == 1 and self.WTCTrue:
                tmp = [x, "WTC", self.randWTC, self.team.team[self.actedOn]]
                self.actions.append(tmp)
            elif self.act == 1 and self.itemTrue:
                tmp = [x, "ITEM", self.randItem, x]
                self.actions.append(tmp)    
            elif self.act == 2:
                tmp = [x, "ITEM", self.randItem, x]
                self.actions.append(tmp)                                                 

    def run(self, actor):
        self.topMonSpeed = 0
        for x in self.monsters:
            if x.attributes.stats[7] > self.topMonSpeed:
                self.topMonSpeed = x.attributes.stats[7]

        self.runMod = int(actor.attributes.stats[7]) - int(self.topMonSpeed)
        #print self.runMod                    
        if self.runMod <= 0:
            #cant run
            self.battleBox.addText("Can't run away!")
            #self.battleBox.draw()
            #print "Can't run away!"
        else:
            self.draw  = random.randint(1,25)
            if self.draw <= self.runMod:
                #success
                self.battleBox.addText("Got away!")
                #self.battleBox.draw()
                #print "Ran Away"
                self.battleBool = False
                self.open = True
                while self.open:      
                    for e in pygame.event.get():
                        if e.type == QUIT:
                            self.quitFlag = 1
                            return
                        elif e.type == KEYDOWN:
                            if e.key == K_RETURN:
                                self.open = False
                return
            else:
                #couldnt run
                self.battleBox.addText("Couldn't get away!")
                #self.battleBox.draw()
                #print "Could not run"        

    def item(self):
        self.itemBool = True
        self.itemList = []
        for x in self.player.shit:
            for y in x.types:
                if y.strip() == "ITEM":
                    self.itemList.append(x.name)
        if len(self.itemList) == 0:
            self.textBox(self.display, self.textureManager, 192, 312, "No items!              ")
            return                      
        self.itemMenu = TextBox.BattleMenu(self.display, self.textureManager, 192, 312, self.itemList)
        self.selectionitem = 0
        while self.itemBool:
            self.display.getScreen().blit(self.textureManager.textures["bg"][0], (0,0))
            self.drawStats()
            for x in self.monsters:
                x.display(self.textureManager, self.display, self.monArray, self.monArrayNum)
                self.monArrayNum += 1
            self.monArrayNum = 0    
            self.display.getScreen().blit(self.textureManager.textures[self.selectedMember.currentSkin][0], (504 - 4*6,96), self.textureManager.spriteRects[self.selectedMember.currentSkin][13])    
            self.battleMenu.show()
            self.battleBox.show()
            self.itemMenu.show()
            if self.selectionitem == 0:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (334, 316), self.textureManager.spriteRects["battle"][1])
            elif self.selectionitem == 1:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (334, 316+24), self.textureManager.spriteRects["battle"][1])
            elif self.selectionitem == 2:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (334, 316+48), self.textureManager.spriteRects["battle"][1])
            elif self.selectionitem == 3:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (334, 316+72), self.textureManager.spriteRects["battle"][1])
            elif self.selectionitem == 4:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (334, 316+96), self.textureManager.spriteRects["battle"][1])
            self.flipScreenBuffer()
            for e in pygame.event.get():
                if e.type == QUIT:
                    self.quitFlag = 1
                    return
                elif e.type == KEYDOWN:
                    #print len(self.itemList)
                    if e.key == K_UP:
                        self.selectionitem -=1
                        if self.selectionitem < 0:
                            self.selectionitem = len(self.itemList) - 1       
                    elif e.key == K_DOWN:
                        self.selectionitem += 1
                        if self.selectionitem > len(self.itemList) - 1:
                            self.selectionitem = 0                      
                    elif e.key == K_END:
                        return
                    elif e.key == K_RETURN:
                        if self.selectionitem == 0:
                            self.itemSelected(self.itemMenu.lines[0])
                            break
                        elif self.selectionitem == 1:
                            self.itemSelected(self.itemMenu.lines[1])
                            break
                        elif self.selectionitem == 2:
                            self.itemSelected(self.itemMenu.lines[2])
                            break
                        elif self.selectionitem == 3:
                            self.itemSelected(self.itemMenu.lines[3])
                            break
                        elif self.selectionitem == 4:
                            self.itemSelected(self.itemMenu.lines[4])
                            break                                                                       
                pygame.event.pump()



    def itemSelected(self, itemItem):            
        self.itemBool = True
        self.selectionitem = (0,0)
        self.itemChoice = itemItem
        while self.itemBool:
            self.display.getScreen().blit(self.textureManager.textures["bg"][0], (0,0))
            self.drawStats()
            for x in self.monsters:
                x.display(self.textureManager, self.display, self.monArray, self.monArrayNum)
                self.monArrayNum += 1
            self.monArrayNum = 0    
            self.display.getScreen().blit(self.textureManager.textures[self.selectedMember.currentSkin][0], (504 - 4*6,96), self.textureManager.spriteRects[self.selectedMember.currentSkin][13])    
            self.battleMenu.show()
            self.battleBox.show()
            self.itemMenu.show()
            if self.selectionitem == (0,0):
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (128, 96), self.textureManager.spriteRects["battle"][1])                 
            elif self.selectionitem == (0,1):
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (128, 144 + 24), self.textureManager.spriteRects["battle"][1])              
            elif self.selectionitem == (0,2):
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (128, 196 + 48), self.textureManager.spriteRects["battle"][1])                 
            elif self.selectionitem == (1,0):
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (214, 96), self.textureManager.spriteRects["battle"][1])              
            elif self.selectionitem == (1,1):
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (214, 144 + 24), self.textureManager.spriteRects["battle"][1])
            elif self.selectionitem == (1,2):
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (214, 196 + 48), self.textureManager.spriteRects["battle"][1])
            elif self.selectionitem == (2,0):
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (316, 96), self.textureManager.spriteRects["battle"][1])
            elif self.selectionitem == (2,1):
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (316, 144 + 24), self.textureManager.spriteRects["battle"][1])
            elif self.selectionitem == (2,2):
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (316, 196 + 48), self.textureManager.spriteRects["battle"][1])                 
            self.flipScreenBuffer()                  
            for e in pygame.event.get():
                self.noChange = False        
                if e.type == QUIT:
                    self.quitFlag = 1
                    return    
                elif e.type == KEYDOWN:
                    if e.key == K_UP:
                        if self.selectionitem[1] == 0 and self.monArray[2][self.selectionitem[0]] is not None:
                            self.selectionitem = (self.selectionitem[0],2)
                        elif self.selectionitem[1] == 0 and self.monArray[1][self.selectionitem[0]] is not None:
                            self.selectionitem = (self.selectionitem[0],1)       
                        elif self.selectionitem[1] == 1:
                            self.selectionitem = (self.selectionitem[0],0)
                        elif self.selectionitem[1] == 2:
                            self.selectionitem = (self.selectionitem[0],1)   
                    elif e.key == K_DOWN:
                        if self.selectionitem[1] == 0 and self.monArray[1][self.selectionitem[0]] is not None:
                            self.selectionitem = (self.selectionitem[0],1)
                        elif self.selectionitem[1] == 1 and self.monArray[2][self.selectionitem[0]] is not None:
                            self.selectionitem = (self.selectionitem[0],2)
                        elif self.selectionitem[1] == 2:
                            self.selectionitem = (self.selectionitem[0],0)
                    elif e.key == K_RIGHT:
                        if self.selectionitem[0] == 0 and self.monArray[self.selectionitem[1]][1] is not None:
                            self.selectionitem = (1,self.selectionitem[1])
                        elif self.selectionitem[0] == 1 and self.monArray[self.selectionitem[1]][2] is not None:
                            self.selectionitem = (2,self.selectionitem[1])
                        elif self.selectionitem[0] == 2:
                            self.selectionitem = (0,self.selectionitem[1])   
                    elif e.key == K_LEFT:
                        if self.selectionitem[0] == 0 and self.monArray[self.selectionitem[1]][2] is not None:
                            self.selectionitem = (2,self.selectionitem[1])
                        if self.selectionitem[0] == 0 and self.monArray[self.selectionitem[1]][1] is not None:
                            self.selectionitem = (1,self.selectionitem[1])    
                        elif self.selectionitem[0] == 1:
                            self.selectionitem = (0,self.selectionitem[1])
                        elif self.selectionitem[0] == 2:
                            self.selectionitem = (1,self.selectionitem[1])
                    elif e.key == K_END:
                        self.itemBool = False
                        break

                    elif e.key == K_RETURN:    
                        self.itemTarget()
                        if self.noChange == True:
                            continue
                        tmp = [self.selectedMember, "ITEM", self.itemChoice, self.monArray[self.selectionitem[1]][self.selectionitem[0]]]
                        self.actions.append(tmp)
                        self.teamNum += 1
                        if self.teamNum == len(self.team.team):
                            self.enemyActions()                                
                            self.teamNum = 0
                            self.doActions = True
                        for x in range(4):    
                            self.display.getScreen().blit(self.textureManager.textures["bg"][0], (0,0))
                            self.display.getScreen().blit(self.textureManager.textures[self.selectedMember.currentSkin][0], (504 - (3-x)*6,96), self.textureManager.spriteRects[self.selectedMember.currentSkin][16-x])    
                            self.drawStats()   
                            for x in self.monsters:
                                x.display(self.textureManager, self.display, self.monArray, self.monArrayNum)
                                self.monArrayNum += 1
                            self.monArrayNum = 0
                            self.battleBox.show()
                            self.battleMenu.show()
                            pygame.time.delay(75)
                            self.flipScreenBuffer()
                        self.selectedMemNum = 13    
                        self.selectedMember = self.team.team[self.teamNum]
                        self.itemBool = False
                        break
                  
    def itemTarget(self, actor, item, actee):
        
        #if self.arrayNum > len(self.monArray) - 1:
        #    self.battleBox.addText("No Target!")
        #    self.battleBox.draw()
        #    self.noChange = True
        #    return                                
        self.accMod = int(actor.attributes.stats[4]) + int(GlobalData.itemData[item][6]) - int(actee.attributes.stats[6])
        #print self.accMod
        for x in actor.shit:
            if x.name == item:
                actor.shit[actor.shit.index(x)].USE -= 1
                if actor.shit[actor.shit.index(x)].USE == 0:
                    actor.shit.remove(x)    
                break
        self.draw = random.randint(0, 100)
        if self.draw > self.accMod:
            self.battleBox.addText(actor.name + " missed " + actee.name + "!")    
            return
        else:
            self.itemMod = int(actor.attributes.stats[2]) + int(GlobalData.itemData[item][4])
            if self.itemMod > 0: 
                actee.HP -= self.itemMod
                self.battleBox.addText(actor.name + " used " + item + " on " + actee.name + "!")
                return
            else:
                self.battleBox.addText(actor.name + "'s " + item + " has no effect on " + actee.name + "!") 
                return
                     

    def attackSelected(self):
        self.attackBool = True
        self.selectionAttack = (0,0)
        while self.attackBool:
            self.display.getScreen().blit(self.textureManager.textures["bg"][0], (0,0))
            self.drawStats()
            for x in self.monsters:
                x.display(self.textureManager, self.display, self.monArray, self.monArrayNum)
                self.monArrayNum += 1
            self.monArrayNum = 0    
            self.display.getScreen().blit(self.textureManager.textures[self.selectedMember.currentSkin][0], (504 - 4*6,96), self.textureManager.spriteRects[self.selectedMember.currentSkin][13])    
            self.battleMenu.show()
            self.battleBox.show()
            if self.selectionAttack == (0,0):
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (128, 96), self.textureManager.spriteRects["battle"][1])                 
            elif self.selectionAttack == (0,1):
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (128, 144 + 24), self.textureManager.spriteRects["battle"][1])              
            elif self.selectionAttack == (0,2):
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (128, 196 + 48), self.textureManager.spriteRects["battle"][1])                 
            elif self.selectionAttack == (1,0):
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (214, 96), self.textureManager.spriteRects["battle"][1])              
            elif self.selectionAttack == (1,1):
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (214, 144 + 24), self.textureManager.spriteRects["battle"][1])
            elif self.selectionAttack == (1,2):
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (214, 196 + 48), self.textureManager.spriteRects["battle"][1])
            elif self.selectionAttack == (2,0):
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (316, 96), self.textureManager.spriteRects["battle"][1])
            elif self.selectionAttack == (2,1):
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (316, 144 + 24), self.textureManager.spriteRects["battle"][1])
            elif self.selectionAttack == (2,2):
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (316, 196 + 48), self.textureManager.spriteRects["battle"][1])                 
            self.flipScreenBuffer()                  
            for e in pygame.event.get():
                self.noChange = False        
                if e.type == QUIT:
                    self.quitFlag = 1
                    return    
                elif e.type == KEYDOWN:
                    if e.key == K_UP:
                        if self.selectionAttack[1] == 0 and self.monArray[2][self.selectionAttack[0]] is not None:
                            self.selectionAttack = (self.selectionAttack[0],2)
                        elif self.selectionAttack[1] == 0 and self.monArray[1][self.selectionAttack[0]] is not None:
                            self.selectionAttack = (self.selectionAttack[0],1)       
                        elif self.selectionAttack[1] == 1:
                            self.selectionAttack = (self.selectionAttack[0],0)
                        elif self.selectionAttack[1] == 2:
                            self.selectionAttack = (self.selectionAttack[0],1)   
                    elif e.key == K_DOWN:
                        if self.selectionAttack[1] == 0 and self.monArray[1][self.selectionAttack[0]] is not None:
                            self.selectionAttack = (self.selectionAttack[0],1)
                        elif self.selectionAttack[1] == 1 and self.monArray[2][self.selectionAttack[0]] is not None:
                            self.selectionAttack = (self.selectionAttack[0],2)
                        elif self.selectionAttack[1] == 2:
                            self.selectionAttack = (self.selectionAttack[0],0)
                    elif e.key == K_RIGHT:
                        if self.selectionAttack[0] == 0 and self.monArray[self.selectionAttack[1]][1] is not None:
                            self.selectionAttack = (1,self.selectionAttack[1])
                        elif self.selectionAttack[0] == 1 and self.monArray[self.selectionAttack[1]][2] is not None:
                            self.selectionAttack = (2,self.selectionAttack[1])
                        elif self.selectionAttack[0] == 2:
                            self.selectionAttack = (0,self.selectionAttack[1])   
                    elif e.key == K_LEFT:
                        if self.selectionAttack[0] == 0 and self.monArray[self.selectionAttack[1]][2] is not None:
                            self.selectionAttack = (2,self.selectionAttack[1])
                        if self.selectionAttack[0] == 0 and self.monArray[self.selectionAttack[1]][1] is not None:
                            self.selectionAttack = (1,self.selectionAttack[1])    
                        elif self.selectionAttack[0] == 1:
                            self.selectionAttack = (0,self.selectionAttack[1])
                        elif self.selectionAttack[0] == 2:
                            self.selectionAttack = (1,self.selectionAttack[1])
                    elif e.key == K_END:
                        self.attackBool = False
                        break

                    elif e.key == K_RETURN:    
                        #self.attackTarget()
                        if self.noChange == True:
                            continue
                        #print self.monArray[0]
                        #print self.monArray[1]
                        #print self.monArray[2]        
                        tmp = [self.selectedMember, "ATTACK", self.monArray[self.selectionAttack[1]][self.selectionAttack[0]]]
                        
                        self.actions.append(tmp)
                        self.teamNum += 1
                        if self.teamNum == len(self.team.team):
                            self.enemyActions()                                
                            self.teamNum = 0
                            self.doActions = True
                        for x in range(4):    
                            self.display.getScreen().blit(self.textureManager.textures["bg"][0], (0,0))
                            self.display.getScreen().blit(self.textureManager.textures[self.selectedMember.currentSkin][0], (504 - (3-x)*6,96), self.textureManager.spriteRects[self.selectedMember.currentSkin][16-x])    
                            self.drawStats()   
                            for x in self.monsters:
                                x.display(self.textureManager, self.display, self.monArray, self.monArrayNum)
                                self.monArrayNum += 1
                            self.monArrayNum = 0
                            self.battleBox.show()
                            self.battleMenu.show()
                            pygame.time.delay(75)
                            self.flipScreenBuffer()
                        self.selectedMemNum = 13    
                        self.selectedMember = self.team.team[self.teamNum]
                        self.attackBool = False
                        break

    def WTC(self):
        self.WTCBool = True
        self.WTCList = []
        for x in self.player.shit:
            for y in x.types:
                if y.strip() == "WTC":
                    self.WTCList.append(x.name)
        if len(self.WTCList) == 0:
            self.textBox(self.display, self.textureManager, 192, 312, "No WTC!              ")
            return                      
        self.WTCMenu = TextBox.BattleMenu(self.display, self.textureManager, 192, 312, self.WTCList)
        self.selectionWTC = 0
        while self.WTCBool:
            self.display.getScreen().blit(self.textureManager.textures["bg"][0], (0,0))
            self.drawStats()
            for x in self.monsters:
                x.display(self.textureManager, self.display, self.monArray, self.monArrayNum)
                self.monArrayNum += 1
            self.monArrayNum = 0    
            self.display.getScreen().blit(self.textureManager.textures[self.selectedMember.currentSkin][0], (504 - 4*6,96), self.textureManager.spriteRects[self.selectedMember.currentSkin][13])    
            self.battleMenu.show()
            self.battleBox.show()
            self.WTCMenu.show()
            if self.selectionWTC == 0:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (334, 316), self.textureManager.spriteRects["battle"][1])
            elif self.selectionWTC == 1:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (334, 316+24), self.textureManager.spriteRects["battle"][1])
            elif self.selectionWTC == 2:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (334, 316+48), self.textureManager.spriteRects["battle"][1])
            elif self.selectionWTC == 3:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (334, 316+72), self.textureManager.spriteRects["battle"][1])
            elif self.selectionWTC == 4:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (334, 316+96), self.textureManager.spriteRects["battle"][1])
            self.flipScreenBuffer()
            for e in pygame.event.get():
                if e.type == QUIT:
                    self.quitFlag = 1
                    return
                elif e.type == KEYDOWN:
                    #print len(self.WTCList)
                    if e.key == K_UP:
                        self.selectionWTC -=1
                        if self.selectionWTC < 0:
                            self.selectionWTC = len(self.WTCList) - 1       
                    elif e.key == K_DOWN:
                        self.selectionWTC += 1
                        if self.selectionWTC > len(self.WTCList) - 1:
                            self.selectionWTC = 0                      
                    elif e.key == K_END:
                        return
                    elif e.key == K_RETURN:
                        if self.selectionWTC == 0:
                            self.WTCSelected(self.WTCMenu.lines[0])
                            break
                        elif self.selectionWTC == 1:
                            self.WTCSelected(self.WTCMenu.lines[1])
                            break
                        elif self.selectionWTC == 2:
                            self.WTCSelected(self.WTCMenu.lines[2])
                            break
                        elif self.selectionWTC == 3:
                            self.WTCSelected(self.WTCMenu.lines[3])
                            break
                        elif self.selectionWTC == 4:
                            self.WTCSelected(self.WTCMenu.lines[4])
                            break                                                                       
                pygame.event.pump()



    def WTCSelected(self, WTCItem):            
        self.WTCBool = True
        self.selectionWTC = (0,0)
        self.WTCChoice = WTCItem
        while self.WTCBool:
            self.display.getScreen().blit(self.textureManager.textures["bg"][0], (0,0))
            self.drawStats()
            for x in self.monsters:
                x.display(self.textureManager, self.display, self.monArray, self.monArrayNum)
                self.monArrayNum += 1
            self.monArrayNum = 0    
            self.display.getScreen().blit(self.textureManager.textures[self.selectedMember.currentSkin][0], (504 - 4*6,96), self.textureManager.spriteRects[self.selectedMember.currentSkin][13])    
            self.battleMenu.show()
            self.battleBox.show()
            self.WTCMenu.show()
            if self.selectionWTC == (0,0):
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (128, 96), self.textureManager.spriteRects["battle"][1])                 
            elif self.selectionWTC == (0,1):
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (128, 144 + 24), self.textureManager.spriteRects["battle"][1])              
            elif self.selectionWTC == (0,2):
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (128, 196 + 48), self.textureManager.spriteRects["battle"][1])                 
            elif self.selectionWTC == (1,0):
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (214, 96), self.textureManager.spriteRects["battle"][1])              
            elif self.selectionWTC == (1,1):
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (214, 144 + 24), self.textureManager.spriteRects["battle"][1])
            elif self.selectionWTC == (1,2):
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (214, 196 + 48), self.textureManager.spriteRects["battle"][1])
            elif self.selectionWTC == (2,0):
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (316, 96), self.textureManager.spriteRects["battle"][1])
            elif self.selectionWTC == (2,1):
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (316, 144 + 24), self.textureManager.spriteRects["battle"][1])
            elif self.selectionWTC == (2,2):
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (316, 196 + 48), self.textureManager.spriteRects["battle"][1])                 
            self.flipScreenBuffer()                  
            for e in pygame.event.get():
                self.noChange = False        
                if e.type == QUIT:
                    self.quitFlag = 1
                    return    
                elif e.type == KEYDOWN:
                    if e.key == K_UP:
                        if self.selectionWTC[1] == 0 and self.monArray[2][self.selectionWTC[0]] is not None:
                            self.selectionWTC = (self.selectionWTC[0],2)
                        elif self.selectionWTC[1] == 0 and self.monArray[1][self.selectionWTC[0]] is not None:
                            self.selectionWTC = (self.selectionWTC[0],1)       
                        elif self.selectionWTC[1] == 1:
                            self.selectionWTC = (self.selectionWTC[0],0)
                        elif self.selectionWTC[1] == 2:
                            self.selectionWTC = (self.selectionWTC[0],1)   
                    elif e.key == K_DOWN:
                        if self.selectionWTC[1] == 0 and self.monArray[1][self.selectionWTC[0]] is not None:
                            self.selectionWTC = (self.selectionWTC[0],1)
                        elif self.selectionWTC[1] == 1 and self.monArray[2][self.selectionWTC[0]] is not None:
                            self.selectionWTC = (self.selectionWTC[0],2)
                        elif self.selectionWTC[1] == 2:
                            self.selectionWTC = (self.selectionWTC[0],0)
                    elif e.key == K_RIGHT:
                        if self.selectionWTC[0] == 0 and self.monArray[self.selectionWTC[1]][1] is not None:
                            self.selectionWTC = (1,self.selectionWTC[1])
                        elif self.selectionWTC[0] == 1 and self.monArray[self.selectionWTC[1]][2] is not None:
                            self.selectionWTC = (2,self.selectionWTC[1])
                        elif self.selectionWTC[0] == 2:
                            self.selectionWTC = (0,self.selectionWTC[1])   
                    elif e.key == K_LEFT:
                        if self.selectionWTC[0] == 0 and self.monArray[self.selectionWTC[1]][2] is not None:
                            self.selectionWTC = (2,self.selectionWTC[1])
                        if self.selectionWTC[0] == 0 and self.monArray[self.selectionWTC[1]][1] is not None:
                            self.selectionWTC = (1,self.selectionWTC[1])    
                        elif self.selectionWTC[0] == 1:
                            self.selectionWTC = (0,self.selectionWTC[1])
                        elif self.selectionWTC[0] == 2:
                            self.selectionWTC = (1,self.selectionWTC[1])
                    elif e.key == K_END:
                        self.WTCBool = False
                        break

                    elif e.key == K_RETURN:    
                        #self.WTCTarget()
                        if self.noChange == True:
                            continue
                        tmp = [self.selectedMember, "WTC", self.WTCChoice, self.monArray[self.selectionWTC[1]][self.selectionWTC[0]]]
                        self.actions.append(tmp)
                        self.teamNum += 1
                        if self.teamNum == len(self.team.team):
                            self.enemyActions()                                
                            self.teamNum = 0
                            self.doActions = True
                        for x in range(4):    
                            self.display.getScreen().blit(self.textureManager.textures["bg"][0], (0,0))
                            self.display.getScreen().blit(self.textureManager.textures[self.selectedMember.currentSkin][0], (504 - (3-x)*6,96), self.textureManager.spriteRects[self.selectedMember.currentSkin][16-x])    
                            self.drawStats()   
                            for x in self.monsters:
                                x.display(self.textureManager, self.display, self.monArray, self.monArrayNum)
                                self.monArrayNum += 1
                            self.monArrayNum = 0
                            self.battleBox.show()
                            self.battleMenu.show()
                            pygame.time.delay(75)
                            self.flipScreenBuffer()
                        self.selectedMemNum = 13    
                        self.selectedMember = self.team.team[self.teamNum]    
                        self.WTCBool = False
                        break
                  
    def WTCTarget(self, actor, WTC, actee):
        #if self.arrayNum > len(self.monArray) - 1:
        #    self.battleBox.addText("No Target!")
        #    self.battleBox.draw()
        #    self.noChange = True
        #    return                                
        self.accMod = int(actor.attributes.stats[4]) + int(GlobalData.itemData[WTC][6]) - int(actee.attributes.stats[6])
        #print self.accMod
        for x in actor.shit:
            if x.name == WTC:
                actor.shit[actor.shit.index(x)].USE -= 1
                if actor.shit[actor.shit.index(x)].USE == 0:
                    actor.shit.remove(x)    
                break
        self.draw = random.randint(0, 100)
        if self.draw > self.accMod:
            self.battleBox.addText(actor.name + " missed " + actee.name + "!")    
            return
        else:
            self.WTCMod = int(actor.attributes.stats[2]) + int(GlobalData.itemData[WTC][4]) - int(actee.attributes.stats[5])
            if self.WTCMod > 0: 
                actee.HP -= self.WTCMod
                self.battleBox.addText(actor.name + " used " + WTC + " on " + actee.name + "!")
                return
            else:
                self.battleBox.addText(actor.name + "'s " + WTC + " has no effect on " + actee.name + "!") 
                return

    def HTC(self):
        self.HTCBool = True
        self.HTCList = []
        self.HTCAct = []
        for x in self.player.shit:
            for y in x.types:
                if y.strip() == "HTC":
                    self.HTCList.append(x.name)
        if len(self.HTCList) == 0:
            self.textBox(self.display, self.textureManager, 192, 312, "No HTC!              ")
            return                      
        self.HTCMenu = TextBox.BattleMenu(self.display, self.textureManager, 192, 312, self.HTCList)
        self.selectionHTC = 0
        while self.HTCBool:
            self.display.getScreen().blit(self.textureManager.textures["bg"][0], (0,0))
            self.drawStats()
            for x in self.monsters:
                x.display(self.textureManager, self.display, self.monArray, self.monArrayNum)
                self.monArrayNum += 1
            self.monArrayNum = 0    
            self.display.getScreen().blit(self.textureManager.textures[self.selectedMember.currentSkin][0], (504 - 4*6,96), self.textureManager.spriteRects[self.selectedMember.currentSkin][13])    
            self.battleMenu.show()
            self.battleBox.show()
            self.HTCMenu.show()
            if self.selectionHTC == 0:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (334, 316), self.textureManager.spriteRects["battle"][1])
            elif self.selectionHTC == 1:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (334, 316+24), self.textureManager.spriteRects["battle"][1])
            elif self.selectionHTC == 2:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (334, 316+48), self.textureManager.spriteRects["battle"][1])
            elif self.selectionHTC == 3:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (334, 316+72), self.textureManager.spriteRects["battle"][1])
            elif self.selectionHTC == 4:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (334, 316+96), self.textureManager.spriteRects["battle"][1])
            self.flipScreenBuffer()
            for e in pygame.event.get():
                if e.type == QUIT:
                    self.quitFlag = 1
                    return
                elif e.type == KEYDOWN:
                    #print len(self.HTCList)
                    if e.key == K_UP:
                        self.selectionHTC -=1
                        if self.selectionHTC < 0:
                            self.selectionHTC = len(self.HTCList) - 1       
                    elif e.key == K_DOWN:
                        self.selectionHTC += 1
                        if self.selectionHTC > len(self.HTCList) - 1:
                            self.selectionHTC = 0                      
                    elif e.key == K_END:
                        return
                    elif e.key == K_RETURN:
                        if self.selectionHTC == 0:
                            self.HTCSelected(self.HTCMenu.lines[0])
                            break
                        elif self.selectionHTC == 1:
                            self.HTCSelected(self.HTCMenu.lines[1])
                            break
                        elif self.selectionHTC == 2:
                            self.HTCSelected(self.HTCMenu.lines[2])
                            break
                        elif self.selectionHTC == 3:
                            self.HTCSelected(self.HTCMenu.lines[3])
                            break
                        elif self.selectionHTC == 4:
                            self.HTCSelected(self.HTCMenu.lines[4])
                            break                                                                       
                pygame.event.pump()



    def HTCSelected(self, HTCItem):            
        self.HTCBool = True
        self.selectionHTC = 0
        self.HTCChoice = HTCItem
        while self.HTCBool:
            self.display.getScreen().blit(self.textureManager.textures["bg"][0], (0,0))
            self.drawStats()
            for x in self.monsters:
                x.display(self.textureManager, self.display, self.monArray, self.monArrayNum)
                self.monArrayNum += 1
            self.monArrayNum = 0    
            self.display.getScreen().blit(self.textureManager.textures[self.selectedMember.currentSkin][0], (504 - 4*6,96), self.textureManager.spriteRects[self.selectedMember.currentSkin][13])    
            self.battleMenu.show()
            self.battleBox.show()
            self.HTCMenu.show()
            if self.selectionHTC == 0:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (528, 96), self.textureManager.spriteRects["battle"][1])                 
            elif self.selectionHTC == 1:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (528, 144), self.textureManager.spriteRects["battle"][1])              
            elif self.selectionHTC == 2:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (528, 196), self.textureManager.spriteRects["battle"][1])                 

            self.flipScreenBuffer()                  
            for e in pygame.event.get():
                self.noChange = False        
                if e.type == QUIT:
                    self.quitFlag = 1
                    return    
                elif e.type == KEYDOWN:
                    if e.key == K_UP:
                        self.selectionHTC -=1
                        if self.selectionHTC < 0:
                            self.selectionHTC = len(self.team.team) - 1       
                    elif e.key == K_DOWN:
                        self.selectionHTC += 1
                        if self.selectionHTC > len(self.team.team) - 1:
                            self.selectionHTC = 0   
                    elif e.key == K_RIGHT:
                        pass
                    elif e.key == K_LEFT:
                        pass
                         #fix Later if I want
                    elif e.key == K_END:
                        self.HTCBool = False
                        break

                    elif e.key == K_RETURN:    
                        #self.HTCTarget()
                        if self.noChange == True:
                            continue
                        tmp = [self.selectedMember, "HTC", self.HTCChoice, self.team.team[self.selectionHTC]]
                        self.actions.append(tmp)
                        self.teamNum += 1
                        if self.teamNum == len(self.team.team):
                            self.enemyActions()                                
                            self.teamNum = 0
                            self.doActions = True
                        for x in range(4):    
                            self.display.getScreen().blit(self.textureManager.textures["bg"][0], (0,0))
                            self.display.getScreen().blit(self.textureManager.textures[self.selectedMember.currentSkin][0], (504 - (3-x)*6,96), self.textureManager.spriteRects[self.selectedMember.currentSkin][16-x])    
                            self.drawStats()   
                            for x in self.monsters:
                                x.display(self.textureManager, self.display, self.monArray, self.monArrayNum)
                                self.monArrayNum += 1
                            self.monArrayNum = 0
                            self.battleBox.show()
                            self.battleMenu.show()
                            pygame.time.delay(75)
                            self.flipScreenBuffer()
                        self.selectedMemNum = 13    
                        self.selectedMember = self.team.team[self.teamNum]    
                        self.HTCBool = False
                        break
                  
    def HTCTarget(self, actor, HTC, actee):                             
        self.accMod = int(actor.attributes.stats[4]) + int(GlobalData.itemData[HTC][6])
        #print self.accMod
        for x in actor.shit:
            if x.name == self.HTCChoice:
                actor.shit.remove(x)
                break
        self.draw = random.randint(0, 100)
        if self.draw > self.accMod:
            self.battleBox.addText(actor.name + " missed " + actee.name + "!")    
            return
        else:
            self.HTCMod = int(actor.attributes.stats[1]) + int(GlobalData.itemData[HTC][5])
            if self.HTCMod > 0: 
                actee.HP += self.HTCMod
                if actee.HP > actee.attributes.stats[0]:
                    actee.HP = actee.attributes.stats[0]
                self.battleBox.addText(actor.name + " used " + HTC + " on " + actee.name + "!")
                return
            else:
                self.battleBox.addText(actor.name + "'s " + HTC + " has no effect on " + actee.name + "!") 
                return

    
    def attackTarget(self, actor, actee):
        #if self.arrayNum > len(self.monArray) - 1:
        #    self.battleBox.addText("No Target!")
        #    self.battleBox.draw()
        #    self.noChange = True
        #    return
        #print self.monArray[self.selectionAttack[0]][self.selectionAttack[1]]
        #print actee                                
        self.accMod = int(actor.attributes.stats[4]) - int(actee.attributes.stats[6])
        #print self.accMod
        self.draw = random.randint(0, 100)
        if self.draw > self.accMod:            
            self.battleBox.addText(actor.name + " missed " + actee.name + "!")    
            return
        else:
            self.strMod = int(actor.attributes.stats[3]) - int(actee.attributes.stats[5])
            if self.strMod > 0: 
                actee.HP -= self.strMod
                self.battleBox.addText(actor.name + " hit " + actee.name + "!")
                return
            else:
                self.battleBox.addText(actor.name + "'s attack has no effect on " + actee.name + "!") 
                return       

                        
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
                    self.quitFlag = 1
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
                        self.quitFlag = 1
                        return
                    elif e.type == KEYDOWN:
                        if e.key == K_RETURN:
                            self.open = False

    def showInventory(self):
        self.nameBox = TextBox.TextBox(self.display, self.textureManager, 168, 168, "Inventory              ")
        self.lines = []
        for x in self.player.shit:
            self.lines.append(x.name.strip() + str(x.USE))
        self.box = TextBox.BattleMenu(self.display, self.textureManager, 168, 216, self.lines)
        self.open = True
        while self.open:
            self.box.show()
            self.nameBox.draw()
            pygame.display.flip()       
            for e in pygame.event.get():
                if e.type == QUIT:
                    self.quitFlag = 1
                    return
                elif e.type == KEYDOWN:
                    if e.key == K_RETURN:
                        self.open = False

    def startMenu(self):
        self.menu = TextBox.StartMenu(self.display, self.textureManager, self.map, self.team)
        self.open = True
        self.selection = 0
        while(True):
            self.menu.show()
            if self.selection == 0:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (514, 48), self.textureManager.spriteRects["battle"][1])
            elif self.selection == 1:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (514, 48+32), self.textureManager.spriteRects["battle"][1])
            elif self.selection == 2:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (514, 48+64), self.textureManager.spriteRects["battle"][1])
            elif self.selection == 3:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (514, 48+96), self.textureManager.spriteRects["battle"][1])
            elif self.selection == 4:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (514, 48+128), self.textureManager.spriteRects["battle"][1])
            elif self.selection == 5:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (514, 48+160), self.textureManager.spriteRects["battle"][1])
            elif self.selection == 6:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (514, 48+192), self.textureManager.spriteRects["battle"][1])
            elif self.selection == 7:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (514, 48+224), self.textureManager.spriteRects["battle"][1])        
            self.flipScreenBuffer()
            for e in pygame.event.get():
                if e.type == QUIT:
                    self.quitFlag = 1
                    return
                elif e.type == KEYDOWN:
                    if e.key == K_UP:
                        self.selection -= 1
                        if self.selection < 0:
                            self.selection = 7   
                    elif e.key == K_DOWN:
                        self.selection += 1
                        if self.selection > 7:
                            self.selection = 0                        
                    elif e.key == K_END or e.key == 105:
                        return
                    elif e.key == K_RETURN:
                        if self.selection == 0:
                            self.menuItem()
                            break
                        elif self.selection == 1:
                            self.menuEquipment()
                            break 
                        elif self.selection == 2:
                            self.menuHTC()
                            break
                        elif self.selection == 3:
                            self.menuStatus()
                            break
                        elif self.selection == 4:
                            self.menuSettings()
                            break
                        elif self.selection == 5:
                            self.menuOrder()
                            break
                        elif self.selection == 6:
                            self.menuSave()
                            break
                        elif self.selection == 7:
                            self.menu.show()
                            self.box = TextBox.TextBox(self.display, self.textureManager, 144, 144, "  Are you sure you want to quit?")
                            self.boxOpen = True
                            self.select = 1
                            
                            while self.boxOpen:
                                self.box.draw()
                                self.display.getScreen().blit(self.font.render("            Yes            No", 0, (255,255,255)), (168, 168))
                                if self.select == 0:
                                    self.display.getScreen().blit(self.textureManager.textures["battle"][0], (264, 168), self.textureManager.spriteRects["battle"][1])
                                elif self.select == 1:
                                    self.display.getScreen().blit(self.textureManager.textures["battle"][0], (336, 168), self.textureManager.spriteRects["battle"][1])
                                pygame.display.flip()       
                                for e in pygame.event.get():
                                    if e.type == QUIT:
                                        self.quitFlag = 1
                                        return
                                    elif e.type == KEYDOWN:
                                        if e.key == K_RETURN:
                                            if self.select == 0:
                                                exit()
                                            else:
                                                self.boxOpen = False
                                                break                    
                                        elif e.key == K_LEFT:
                                            self.select -= 1
                                            if self.select < 0:
                                                self.select = 1   
                                        elif e.key == K_RIGHT:
                                            self.select += 1
                                            if self.select > 1:
                                                self.select = 0
                                                              
                pygame.event.pump()
        
        #while self.open:
        #    self.menu.show()       
        #    for e in pygame.event.get():
        #        if e.type == QUIT:
        #            self.quitFlag = 1
        #            return
        #        elif e.type == KEYDOWN:
        #            if e.key == 105:
        #                self.open = False

    def menuSave(self):
        #TODO
        pass

    def menuSettings(self):
        #TODO
        pass    

    def menuItem(self):
        self.chosen = False
        self.selection = 0
        while not self.chosen:
            self.menu.show()
            if self.selection == 0:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (216, 96), self.textureManager.spriteRects["battle"][1])
            elif self.selection == 1:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (216, 96+32), self.textureManager.spriteRects["battle"][1])
            elif self.selection == 2:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (216, 96+64), self.textureManager.spriteRects["battle"][1])
            elif self.selection == 3:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (216, 96+96), self.textureManager.spriteRects["battle"][1])    
            self.flipScreenBuffer()
            for e in pygame.event.get():
                if e.type == QUIT:
                    self.quitFlag = 1
                    return
                elif e.type == KEYDOWN:
                    #print len(self.WTCList)
                    if e.key == K_UP:
                        self.selection -=1
                        if self.selection < 0:
                            self.selection = len(self.team.team) - 1       
                    elif e.key == K_DOWN:
                        self.selection += 1
                        if self.selection > len(self.team.team) - 1:
                            self.selection = 0                      
                    elif e.key == K_END:
                        return
                    elif e.key == K_RETURN:
                        self.menuItemSelected(self.team.team[self.selection])
                        self.chosen = True
                        break

    def menuEquipment(self):
        self.chosen = False
        self.selection = 0
        while not self.chosen:
            self.menu.show()
            if self.selection == 0:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (216, 96), self.textureManager.spriteRects["battle"][1])
            elif self.selection == 1:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (216, 96+32), self.textureManager.spriteRects["battle"][1])
            elif self.selection == 2:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (216, 96+64), self.textureManager.spriteRects["battle"][1])
            elif self.selection == 3:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (216, 96+96), self.textureManager.spriteRects["battle"][1])    
            self.flipScreenBuffer()
            for e in pygame.event.get():
                if e.type == QUIT:
                    self.quitFlag = 1
                    return
                elif e.type == KEYDOWN:
                    #print len(self.WTCList)
                    if e.key == K_UP:
                        self.selection -=1
                        if self.selection < 0:
                            self.selection = len(self.team.team) - 1       
                    elif e.key == K_DOWN:
                        self.selection += 1
                        if self.selection > len(self.team.team) - 1:
                            self.selection = 0                      
                    elif e.key == K_END:
                        return
                    elif e.key == K_RETURN:
                        self.menuEquipSelected(self.team.team[self.selection])
                        self.chosen = True
                        break

    def menuHTC(self):
        self.chosen = False
        self.selection = 0
        while not self.chosen:
            self.menu.show()
            if self.selection == 0:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (216, 96), self.textureManager.spriteRects["battle"][1])
            elif self.selection == 1:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (216, 96+32), self.textureManager.spriteRects["battle"][1])
            elif self.selection == 2:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (216, 96+64), self.textureManager.spriteRects["battle"][1])
            elif self.selection == 3:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (216, 96+96), self.textureManager.spriteRects["battle"][1])    
            self.flipScreenBuffer()
            for e in pygame.event.get():
                if e.type == QUIT:
                    self.quitFlag = 1
                    return
                elif e.type == KEYDOWN:
                    #print len(self.WTCList)
                    if e.key == K_UP:
                        self.selection -=1
                        if self.selection < 0:
                            self.selection = len(self.team.team) - 1       
                    elif e.key == K_DOWN:
                        self.selection += 1
                        if self.selection > len(self.team.team) - 1:
                            self.selection = 0                      
                    elif e.key == K_END:
                        return
                    elif e.key == K_RETURN:
                        self.menuHTCSelected(self.team.team[self.selection])
                        self.chosen = True
                        break
                        
    def menuStatus(self):
        self.chosen = False
        self.selection = 0
        while not self.chosen:
            self.menu.show()
            if self.selection == 0:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (216, 96), self.textureManager.spriteRects["battle"][1])
            elif self.selection == 1:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (216, 96+32), self.textureManager.spriteRects["battle"][1])
            elif self.selection == 2:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (216, 96+64), self.textureManager.spriteRects["battle"][1])
            elif self.selection == 3:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (216, 96+96), self.textureManager.spriteRects["battle"][1])    
            self.flipScreenBuffer()
            for e in pygame.event.get():
                if e.type == QUIT:
                    self.quitFlag = 1
                    return
                elif e.type == KEYDOWN:
                    #print len(self.WTCList)
                    if e.key == K_UP:
                        self.selection -=1
                        if self.selection < 0:
                            self.selection = len(self.team.team) - 1       
                    elif e.key == K_DOWN:
                        self.selection += 1
                        if self.selection > len(self.team.team) - 1:
                            self.selection = 0                      
                    elif e.key == K_END:
                        return
                    elif e.key == K_RETURN:
                        self.menuStatusSelected(self.team.team[self.selection])
                        self.chosen = True
                        break

    def menuOrder(self):
        self.chosen = False
        self.selection = 0
        while not self.chosen:
            self.menu.show()
            if self.selection == 0:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (216, 96), self.textureManager.spriteRects["battle"][1])
            elif self.selection == 1:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (216, 96+32), self.textureManager.spriteRects["battle"][1])
            elif self.selection == 2:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (216, 96+64), self.textureManager.spriteRects["battle"][1])
            elif self.selection == 3:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (216, 96+96), self.textureManager.spriteRects["battle"][1])    
            self.flipScreenBuffer()
            for e in pygame.event.get():
                if e.type == QUIT:
                    self.quitFlag = 1
                    return
                elif e.type == KEYDOWN:
                    #print len(self.WTCList)
                    if e.key == K_UP:
                        self.selection -=1
                        if self.selection < 0:
                            self.selection = len(self.team.team) - 1       
                    elif e.key == K_DOWN:
                        self.selection += 1
                        if self.selection > len(self.team.team) - 1:
                            self.selection = 0                      
                    elif e.key == K_END:
                        return
                    elif e.key == K_RETURN:
                        self.menuOrderSelected(self.team.team[self.selection])
                        self.chosen = True
                        break                     

    def menuWTC(self):
        self.chosen = False
        self.selection = 0
        while not self.chosen:
            self.menu.show()
            if self.selection == 0:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (216, 96), self.textureManager.spriteRects["battle"][1])
            elif self.selection == 1:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (216, 96+32), self.textureManager.spriteRects["battle"][1])
            elif self.selection == 2:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (216, 96+64), self.textureManager.spriteRects["battle"][1])
            elif self.selection == 3:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (216, 96+96), self.textureManager.spriteRects["battle"][1])    
            self.flipScreenBuffer()
            for e in pygame.event.get():
                if e.type == QUIT:
                    self.quitFlag = 1
                    return
                elif e.type == KEYDOWN:
                    #print len(self.WTCList)
                    if e.key == K_UP:
                        self.selection -=1
                        if self.selection < 0:
                            self.selection = len(self.team.team) - 1       
                    elif e.key == K_DOWN:
                        self.selection += 1
                        if self.selection > len(self.team.team) - 1:
                            self.selection = 0                      
                    elif e.key == K_END:
                        return
                    elif e.key == K_RETURN:
                        self.menuWTCSelected(self.team.team[self.selection])
                        self.chosen = True
                        break

    def menuItemSelected(self, player):
        self.itemList = []
        for x in player.shit:
            for y in x.types:
                if y.strip() == "ITEM":
                    self.itemList.append(x.name)

    def menuHTCSelected(self, player):
        self.HTCList = []
        for x in player.shit:
            for y in x.types:
                if y.strip() == "HTC":
                    self.HTCList.append(x.name)

    def menuEquipSelected(self, player):
        self.equipWpnList = []
        self.equipArmList = []
        for x in player.shit:
            for y in x.types:
                if y.strip() == "WPN":
                    self.equipWpnList.append(x.name)
        for x in player.shit:
            for y in x.types:
                if y.strip() == "ARM":
                    self.equipArmList.append(x.name)

    def menuOrderSelected(self, player):
        self.first = player
           

    def menuStatusSelected(self, player):
        pass

    def menuWTCSelected(self, player):
        self.WTCList = []
        for x in player.shit:
            for y in x.types:
                if y.strip() == "WTC":
                    self.WTCList.append(x.name)                                                            
                        
if __name__ == "__main__":                                                   
    game = GameLoop()
    #print "Default Font: %s"%(pygame.font.get_default_font())
    #print "All fonts:\n-------------"
    #print pygame.font.get_fonts()
    game.mainloop()
