import Creature
import TextBox
import Map
import random
import pygame
import Attributes
from pygame.locals import *
import pygame.time
import GlobalData
import PlayerData



class StartMenu:
    def __init__(self, currMap, team, player):
        self.map = currMap
        self.team = team
        self.font = pygame.font.Font(None, 24)
        self.display = GlobalData.display
        self.textureManager = GlobalData.textureManager

    def flipScreenBuffer(self):
        pygame.display.flip()    

    def menuMain(self):
        self.menu = MenuBox(self.map, self.team, 360, 360)
        self.open = True
        self.selection = 0
        self.display.getScreen().fill((0,0,0))
        while(True):
            
            self.menu.show()
            self.menu.showMenu()
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
                            self.menuItems()
                            break
                        elif self.selection == 1:
                            self.menuSelectChar("EQUIP")
                            break 
                        elif self.selection == 2:
                            self.menuSelectChar("HTC")
                            break
                        elif self.selection == 3:
                            self.menuSelectChar("STATUS")
                            break
                        elif self.selection == 4:
                            self.menuSettings()
                            break
                        elif self.selection == 5:
                            self.menuSelectChar("ORDER")
                            break
                        elif self.selection == 6:
                            self.menuSave()
                            break
                        elif self.selection == 7:
                            self.menu.show()
                            self.menu.showMenu()
                            self.box = TextBox.TextBox(144, 144, "  Are you sure you want to quit?")
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
        


    def menuSave(self):
        #TODO
        pass

    def menuSettings(self):
        #TODO
        pass    

    def menuItems(self):
        self.chosen = False
        self.selection = 0
        self.inventory = MenuBox(self.map,self.team,504,360)
        while not self.chosen:   
            self.inventory.show()
            pygame.display.flip()
            for e in pygame.event.get():
                if e.type == QUIT:
                    self.quitFlag = 1
                    return
                elif e.type == KEYDOWN:
                    if e.key == K_UP:
                        self.selection -=1
                        if self.selection < 0:
                            self.selection = len(self.team.itemList) - 1       
                    elif e.key == K_DOWN:
                        self.selection += 1
                        if self.selection > len(self.team.itemList) - 1:
                            self.selection = 0                      
                    elif e.key == K_END:
                        return
                    elif e.key == K_RETURN:
                        if len(self.team.itemList) == 0:
                            return
                        else:                            
                            self.itemInfo(self.team.itemList[self.selection])
                        self.chosen = True
                        break
 
    def itemInfo(self, item):
        pass
        #TODO 
                        
        
    def menuSelectChar(self, selectType):
        self.chosen = False
        self.selection = 0
        while not self.chosen:
            self.menu.show()
            self.menu.showMenu()
            if self.selection == 0:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (200, 72), self.textureManager.spriteRects["battle"][1])
            elif self.selection == 1:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (200, 72+96), self.textureManager.spriteRects["battle"][1])
            elif self.selection == 2:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (200, 72+192), self.textureManager.spriteRects["battle"][1])
            elif self.selection == 3:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (200, 72+288), self.textureManager.spriteRects["battle"][1])    
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
                        if selectType == "ORDER":
                            self.menuOrder(self.team.team[self.selection])
                        elif selectType == "STATUS":
                            self.menuStatus(self.team.team[self.selection])
                        elif selectType == "EQUIP":
                            self.menuEquipment(self.team.team[self.selection])
                        elif selectType == "HTC":
                            self.menuCharShit(self.team.team[self.selection])
                        self.chosen = True
                        break

                        
    def menuStatus(self, member):
        self.selection = 0
        self.status = MenuBox(self.map, self.team, 504, 360)
        self.status.show()
        self.display.getScreen().blit(self.textureManager.textures[member.currentSkin][0], (72,96), self.textureManager.spriteRects[member.currentSkin][9])
        self.display.getScreen().blit(self.font.render(member.name, 0, (255,255,255)), (120, 96))
        self.flipScreenBuffer()
        while True:
            for e in pygame.event.get():
                if e.type == QUIT:
                    self.quitFlag = 1
                    return
                elif e.type == KEYDOWN:                    
                    if e.key == K_END:
                        return
                    elif e.key == K_RETURN:
                        break

    def menuOrder(self, firstMember):
        self.chosen = False
        self.selection2 = 0
        self.show = False
        while not self.chosen:
            self.menu.show()
            self.menu.showMenu()
            if self.show == True:   
                if self.selection == 0:
                    self.display.getScreen().blit(self.textureManager.textures["battle"][0], (200, 72), self.textureManager.spriteRects["battle"][1])
                elif self.selection == 1:
                    self.display.getScreen().blit(self.textureManager.textures["battle"][0], (200, 72+96), self.textureManager.spriteRects["battle"][1])
                elif self.selection == 2:
                    self.display.getScreen().blit(self.textureManager.textures["battle"][0], (200, 72+192), self.textureManager.spriteRects["battle"][1])
                elif self.selection == 3:
                    self.display.getScreen().blit(self.textureManager.textures["battle"][0], (200, 72+288), self.textureManager.spriteRects["battle"][1])
                self.show = False            
            else:
                self.show = True
            if self.selection2 == 0:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (200, 72), self.textureManager.spriteRects["battle"][1])
            elif self.selection2 == 1:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (200, 72+96), self.textureManager.spriteRects["battle"][1])
            elif self.selection2 == 2:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (200, 72+192), self.textureManager.spriteRects["battle"][1])
            elif self.selection2 == 3:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (200, 72+288), self.textureManager.spriteRects["battle"][1])    
            self.flipScreenBuffer()
            for e in pygame.event.get():
                if e.type == QUIT:
                    self.quitFlag = 1
                    return
                elif e.type == KEYDOWN:
                    #print len(self.WTCList)
                    if e.key == K_UP:
                        self.selection2 -=1
                        if self.selection2 < 0:
                            self.selection2 = len(self.team.team) - 1       
                    elif e.key == K_DOWN:
                        self.selection2 += 1
                        if self.selection2 > len(self.team.team) - 1:
                            self.selection2 = 0                      
                    elif e.key == K_END:
                        return
                    elif e.key == K_RETURN:
                        self.tmp = self.team.team[self.selection]
                        self.team.team[self.selection] = self.team.team[self.selection2]
                        self.team.team[self.selection2] = self.tmp 
                        self.chosen = True
                        break                     

    
    def menuCharShit(self, member):
        self.equipped = MenuBox(self.map,self.team,348,108, 216, 48)
        self.charBox = MenuBox(self.map, self.team, 168, 168)
        self.list = MenuBox(self.map,self.team, 504, 272, 48, 144)
        self.selection2 = 0
        while True:
            self.equipped.show()
            self.charBox.show()
            self.list.show()
            self.display.getScreen().blit(self.textureManager.textures[member.currentSkin][0], (72,72), self.textureManager.spriteRects[member.currentSkin][9])
            self.display.getScreen().blit(self.font.render(member.name, 0, (255,255,255)), (120, 72))
            self.display.getScreen().blit(self.font.render("R. Hand: " + str(member.rHand), 0, (255,255,255)), (224, 54))
            self.display.getScreen().blit(self.font.render("L. Hand: " + str(member.lHand), 0, (255,255,255)), (224, 90))
            self.display.getScreen().blit(self.font.render("Armor: " + str(member.armor), 0, (255,255,255)), (224, 126))
            self.display.getScreen().blit(self.textureManager.textures["battle"][0], (528, 54 + self.selection2*36), self.textureManager.spriteRects["battle"][1])

            self.flipScreenBuffer()
            
            for e in pygame.event.get():
                if e.type == QUIT:
                    self.quitFlag = 1
                    return
                elif e.type == KEYDOWN:
                    #print len(self.WTCList)
                    if e.key == K_UP:
                        self.selection2 -=1
                        if self.selection2 < 0:
                            self.selection2 = 2       
                    elif e.key == K_DOWN:
                        self.selection2 += 1
                        if self.selection2 > 2:
                            self.selection2 = 0                      
                    elif e.key == K_END:
                        return
                    elif e.key == K_RETURN:
                        self.menuList(member)
                        break 

    def menuList(self, member):
        self.lines = self.team.WTCList
        self.selectionList = [[None for i in range(2)] for j in range(10)]
        self.fullList = [[None for i in range(2)] for j in range(100)]
        self.pointerLoc = 0
        for x in range(len(self.lines)):
            if x < 20:
                self.selectionList[x/2][x%2] = self.lines[x]
                self.fullList[x/2][x%2] = self.lines[x]
            else:
                self.fullList[x/2][x%2] = self.lines[x]
        self.selection3 = (0,0)
        self.lineNum = len(self.lines)
        self.show = False
        self.arrow = 1
        while True:
            self.equipped.show()
            self.list.show()
            self.display.getScreen().blit(self.font.render("R. Hand: " + str(member.rHand), 0, (255,255,255)), (224, 54))
            self.display.getScreen().blit(self.font.render("L. Hand: " + str(member.lHand), 0, (255,255,255)), (224, 90))
            self.display.getScreen().blit(self.font.render("Armor: " + str(member.armor), 0, (255,255,255)), (224, 126))
            if self.show == True:            
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (528, 54 + self.selection2*36), self.textureManager.spriteRects["battle"][1])
                self.show = False
               
            else:
                self.show = True
            pygame.time.delay(150)
            if self.selection3[0] == 0:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (276, 144 + self.pointerLoc*24), self.textureManager.spriteRects["battle"][1])
            else:
                self.display.getScreen().blit(self.textureManager.textures["battle"][0], (504, 144 + self.pointerLoc*24), self.textureManager.spriteRects["battle"][1])
            self.display.getScreen().blit(self.textureManager.textures["battle2"][0], (528, 388), self.textureManager.spriteRects["battle2"][self.arrow])       
            self.arrow += 1
            if self.arrow == 4:
                self.arrow = 1    
            
            self.whichRow = 0
            for x in self.selectionList:
                self.whichCol = 0                
                for y in x:
                    self.display.getScreen().blit(self.font.render(y, 0, (255,255,255)), (60 + self.whichCol*240, 150 + self.whichRow*24))
                    self.whichCol += 1
                self.whichRow += 1
            self.flipScreenBuffer()
            for e in pygame.event.get():
                if e.type == QUIT:
                    self.quitFlag = 1
                    return
                elif e.type == KEYDOWN:
                    if e.key == K_UP:
                        self.selection3 = (self.selection3[0], self.selection3[1] - 1)
                        if self.selection3[1] < 0:
                            self.selection3 = (self.selection3[0], 0) 
                        elif self.pointerLoc > 0:
                            self.pointerLoc -= 1      
                            
                    elif e.key == K_DOWN:
                        self.selection3 = (self.selection3[0], self.selection3[1] + 1)
                        if self.selection3[1] > 99:
                            self.selection3 = (self.selection3[0], 99) 
                        elif self.pointerLoc < 9:
                            self.pointerLoc += 1  
                                            
                    elif e.key == K_RIGHT:
                        self.selection3 = (self.selection3[0] + 1, self.selection3[1])
                        if self.selection3[0] > 1:
                            self.selection3 = (1, self.selection3[1])  
                                 
                    elif e.key == K_LEFT:
                        self.selection3 = (self.selection3[0] - 1, self.selection3[1])
                        if self.selection3[0] < 0:
                            self.selection3 = (0, self.selection3[1])       
                    elif e.key == K_END:
                        return
                    elif e.key == K_RETURN:
                        if self.selection2 == 0:
                            self.tmp = member.rHand
                            member.rHand = self.fullList[self.selection3[0]][self.selection3[1]]
                            self.fullList[self.selection3[0]][self.selection3[1]] = self.tmp
                            self.team.WTCList
                            return
                        elif self.selection2 == 1:
                            self.tmp = member.lHand
                            member.lHand = self.fullList[self.selection3[0]][self.selection3[1]]
                            self.fullList[self.selection3[0]][self.selection3[1]] = self.tmp
                            return 
                        elif self.selection2 == 2:
                            self.tmp = member.armor
                            member.armor = self.fullList[self.selection3[0]][self.selection3[1]]
                            self.fullList[self.selection3[0]][self.selection3[1]] = self.tmp
                            return

    def menuEquipment(self, player):
        self.HTC = MenuBox(self.map,self.team,180,360, 240, 48)
        self.selected = False
        self.lines = self.team.HTCList
        self.lineNum = len(self.lines)
        self.lineOffset = 0
        self.width = 160
        self.height = 48
        self.x = 240
        self.y = 48
        self.selection2 = 0
        while self.selected is False:
            self.HTC.show()
            self.flipScreenBuffer()
            final_lines = []
            if self.lineNum < 11:
                final_lines = self.lines
            else:
                for x in range(11):
                    print x
                    final_lines.append(self.lines[x+self.lineOffset])
         
            self.xCount = self.width/24
            if self.width%24 != 0:
                self.xCount += 1
            if len(final_lines) <= 5:    
                self.yCount = len(final_lines)
                if len(final_lines) == 1:
                    self.yCount +=1
            else:
                self.yCount = 5        
            for x in range(self.xCount):
                for y in range(self.yCount):
                    if x == 0:
                        if y == 0:
                            #print "topleft"
                            self.display.getScreen().blit(self.textureManager.textures["text"][0], (self.x + x*24, self.y + y*24), self.textureManager.spriteRects["text"][1])              
                        elif y == self.yCount-1:
                            #print "botleft"
                            self.display.getScreen().blit(self.textureManager.textures["text"][0], (self.x + x*24, self.y + y*24), self.textureManager.spriteRects["text"][7])
                        else:
                            #print "midleft"
                            self.display.getScreen().blit(self.textureManager.textures["text"][0], (self.x + x*24, self.y + y*24), self.textureManager.spriteRects["text"][4])
                    elif x == self.xCount - 1 :
                        if y == 0:
                            #print "topright"
                            self.display.getScreen().blit(self.textureManager.textures["text"][0], (self.x + x*24, self.y + y*24), self.textureManager.spriteRects["text"][3])              
                        elif y == self.yCount-1:
                            #print "botright"
                            self.display.getScreen().blit(self.textureManager.textures["text"][0], (self.x + x*24, self.y + y*24), self.textureManager.spriteRects["text"][9])
                        else:
                            #print "midright"
                            self.display.getScreen().blit(self.textureManager.textures["text"][0], (self.x + x*24, self.y + y*24), self.textureManager.spriteRects["text"][6])
                    else:
                        if y == 0:
                            #print "topmid"
                            self.display.getScreen().blit(self.textureManager.textures["text"][0], (self.x + x*24, self.y + y*24), self.textureManager.spriteRects["text"][2])              
                        elif y == self.yCount-1:
                            #print "botmid"
                            self.display.getScreen().blit(self.textureManager.textures["text"][0], (self.x + x*24, self.y + y*24), self.textureManager.spriteRects["text"][8])
                        else:
                            #print "center"
                            self.display.getScreen().blit(self.textureManager.textures["text"][0], (self.x + x*24, self.y + y*24), self.textureManager.spriteRects["text"][5])
                          
            self.yPlus = 0
            for x in final_lines:            
                self.display.getScreen().blit(self.font.render(x, 0, (255,255,255)), (self.x + 6, self.y + self.yPlus + 4))
                self.yPlus += 24
            for e in pygame.event.get():
                if e.type == QUIT:
                    self.quitFlag = 1
                    return
                elif e.type == KEYDOWN:
                    #print len(self.WTCList)
                    if e.key == K_UP:
                        self.selection2 -=1
                        if self.selection2 < 0:
                            self.selection2 = len(self.team.HTCList) - 1       
                    elif e.key == K_DOWN:
                        self.selection2 += 1
                        if self.selection2 > len(self.team.HTCList) - 1:
                            self.selection2 = 0                      
                    elif e.key == K_END:
                        return
                    elif e.key == K_RETURN:
                        self.selected = True
                        break 

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


#######################################
class MenuBox:    
    def __init__(self, themap, team, width, height, x = 48, y = 48):
        self.x = x
        self.y = y
        self.team = team
        self.width = width
        self.height = height     
        self.lines = []
        self.map = themap
        self.lineNum = 0
        self.facing = 9
        self.font = pygame.font.Font(None, 24)
        self.timer = GlobalData.timer
        self.display = GlobalData.display
        self.textureManager = GlobalData.textureManager
         

    def show(self):
        self.xCount = self.width/24
        self.yCount = self.height/24
        for x in range(self.xCount):
            for y in range(self.yCount):
                if x == 0:
                    if y == 0:
                        self.display.getScreen().blit(self.textureManager.textures["text"][0], (self.x + x*24, self.y + y*24), self.textureManager.spriteRects["text"][1])              
                    elif y == self.yCount-1:
                        self.display.getScreen().blit(self.textureManager.textures["text"][0], (self.x + x*24, self.y + y*24), self.textureManager.spriteRects["text"][7])
                    else:
                        self.display.getScreen().blit(self.textureManager.textures["text"][0], (self.x + x*24, self.y + y*24), self.textureManager.spriteRects["text"][4])
                elif x == self.xCount - 1 :
                    if y == 0:
                        self.display.getScreen().blit(self.textureManager.textures["text"][0], (self.x + x*24, self.y + y*24), self.textureManager.spriteRects["text"][3])              
                    elif y == self.yCount-1:
                        self.display.getScreen().blit(self.textureManager.textures["text"][0], (self.x + x*24, self.y + y*24), self.textureManager.spriteRects["text"][9])
                    else:
                        self.display.getScreen().blit(self.textureManager.textures["text"][0], (self.x + x*24, self.y + y*24), self.textureManager.spriteRects["text"][6])
                else:
                    if y == 0:
                        self.display.getScreen().blit(self.textureManager.textures["text"][0], (self.x + x*24, self.y + y*24), self.textureManager.spriteRects["text"][2])              
                    elif y == self.yCount-1:
                        self.display.getScreen().blit(self.textureManager.textures["text"][0], (self.x + x*24, self.y + y*24), self.textureManager.spriteRects["text"][8])
                    else:
                        self.display.getScreen().blit(self.textureManager.textures["text"][0], (self.x + x*24, self.y + y*24), self.textureManager.spriteRects["text"][5])                         

    def showMenu(self):
        
        self.menuLines = ["Item", "Equipment", "HTC", "Status", "Settings", "Order", "Save", "Quit"]
        self.otherxCount = 6
        self.otheryCount = 11
        for x in range(self.otherxCount):
            for y in range(self.otheryCount):
                if x == 0:
                    if y == 0:
                        self.display.getScreen().blit(self.textureManager.textures["text"][0], (456-48 + x*24, self.y + y*24), self.textureManager.spriteRects["text"][1])              
                    elif y == self.otheryCount-1:
                        self.display.getScreen().blit(self.textureManager.textures["text"][0], (456-48 + x*24, self.y + y*24), self.textureManager.spriteRects["text"][7])
                    else:
                        self.display.getScreen().blit(self.textureManager.textures["text"][0], (456-48 + x*24, self.y + y*24), self.textureManager.spriteRects["text"][4])
                elif x == self.otherxCount - 1:
                    if y == 0:
                        self.display.getScreen().blit(self.textureManager.textures["text"][0], (456-48 + x*24, self.y + y*24), self.textureManager.spriteRects["text"][3])              
                    elif y == self.otheryCount-1:
                        self.display.getScreen().blit(self.textureManager.textures["text"][0], (456-48 + x*24, self.y + y*24), self.textureManager.spriteRects["text"][9])
                    else:
                        self.display.getScreen().blit(self.textureManager.textures["text"][0], (456-48 + x*24, self.y + y*24), self.textureManager.spriteRects["text"][6])
                else:
                    if y == 0:
                        self.display.getScreen().blit(self.textureManager.textures["text"][0], (456-48 + x*24, self.y + y*24), self.textureManager.spriteRects["text"][2])              
                    elif y == self.otheryCount-1:
                        self.display.getScreen().blit(self.textureManager.textures["text"][0], (456-48 + x*24, self.y + y*24), self.textureManager.spriteRects["text"][8])
                    else:
                        self.display.getScreen().blit(self.textureManager.textures["text"][0], (456-48 + x*24, self.y + y*24), self.textureManager.spriteRects["text"][5])                  
        self.yPlus = 0
        for x in self.menuLines:            
            self.display.getScreen().blit(self.font.render(x, 0, (255,255,255)), (456-48 + 6, self.y + self.yPlus + 4))
            self.yPlus += 32        

        self.yPlus = 0
        for x in self.team.team:
            self.display.getScreen().blit(self.textureManager.textures[x.currentSkin][0], (72,72 + self.yPlus), self.textureManager.spriteRects[x.currentSkin][self.facing])
            self.display.getScreen().blit(self.font.render(x.name, 0, (255,255,255)), (120, 72 + self.yPlus))
            self.yPlus += 96
            if self.yPlus/96 > len(self.team.team):
                self.yPlus = 0
        self.facing += 1
        if self.facing == 13:
            self.facing  = 9            


        final_lines = []
        requested_lines = "Money   " + str(self.team.money) + " Location: " + str(self.map.name)
        if self.font.size(requested_lines)> 148 - 24:
            words = requested_lines.split(' ')
            accumulated_line = ""
            for word in words:
                test_line = accumulated_line + word + " "
                # Build the line while the words fit.    
                if self.font.size(test_line)[0] < 148 - 24:
                    accumulated_line = test_line 
                else: 
                    final_lines.append(accumulated_line) 
                    accumulated_line = word + " "
            final_lines.append(accumulated_line)
        else: 
            final_lines = requested_lines
        self.displayLines = final_lines
        self.otherxCount = 6
        self.otheryCount = 4
        for x in range(self.otherxCount):
            for y in range(self.otheryCount):
                if x == 0:
                    if y == 0:
                        self.display.getScreen().blit(self.textureManager.textures["text"][0], (456-48 + x*24, 312 + y*24), self.textureManager.spriteRects["text"][1])              
                    elif y == self.otheryCount-1:
                        self.display.getScreen().blit(self.textureManager.textures["text"][0], (456-48 + x*24, 312 + y*24), self.textureManager.spriteRects["text"][7])
                    else:
                        self.display.getScreen().blit(self.textureManager.textures["text"][0], (456-48 + x*24, 312 + y*24), self.textureManager.spriteRects["text"][4])
                elif x == self.otherxCount - 1:
                    if y == 0:
                        self.display.getScreen().blit(self.textureManager.textures["text"][0], (456-48 + x*24, 312 + y*24), self.textureManager.spriteRects["text"][3])              
                    elif y == self.otheryCount-1:
                        self.display.getScreen().blit(self.textureManager.textures["text"][0], (456-48 + x*24, 312 + y*24), self.textureManager.spriteRects["text"][9])
                    else:
                        self.display.getScreen().blit(self.textureManager.textures["text"][0], (456-48 + x*24, 312 + y*24), self.textureManager.spriteRects["text"][6])
                else:
                    if y == 0:
                        self.display.getScreen().blit(self.textureManager.textures["text"][0], (456-48 + x*24, 312 + y*24), self.textureManager.spriteRects["text"][2])              
                    elif y == self.otheryCount-1:
                        self.display.getScreen().blit(self.textureManager.textures["text"][0], (456-48 + x*24, 312 + y*24), self.textureManager.spriteRects["text"][8])
                    else:
                        self.display.getScreen().blit(self.textureManager.textures["text"][0], (456-48 + x*24, 312 + y*24), self.textureManager.spriteRects["text"][5])                  
        self.yPlus = 0
        for x in self.displayLines:            
            self.display.getScreen().blit(self.font.render(x, 0, (255,255,255)), (456-48 + 6, 312 + self.yPlus + 4))
            self.yPlus += 32        
        #pygame.display.flip()
        #pygame.time.delay(150)
        self.timer.tick(8)
    
        
    def addText(self, text):       
        self.text = text
        self.open = True
        self.draw()
        self.show()
        pygame.display.flip()
       
        self.selected = False
