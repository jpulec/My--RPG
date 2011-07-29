import pygame
from pygame.locals import *
import TextBox








class Menu:
    def __init__(self, display, graphicsData, mapData, team):
        GlobalData.textureManager = graphicsData
        self.display = display
        self.map = mapData
        self.team = team
        pygame.font.init()
        self.font = pygame.font.Font(None, 24)

    def startMenu(self):
        self.menu = TextBox.StartMenu(self.display, GlobalData.textureManager, self.map, self.team)
        self.open = True
        self.selection = 0
        while(True):
            self.menu.show()
            if self.selection == 0:
                self.display.getScreen().blit(GlobalData.textureManager.textures["battle"][0], (514, 48), GlobalData.textureManager.spriteRects["battle"][1])
            elif self.selection == 1:
                self.display.getScreen().blit(GlobalData.textureManager.textures["battle"][0], (514, 48+32), GlobalData.textureManager.spriteRects["battle"][1])
            elif self.selection == 2:
                self.display.getScreen().blit(GlobalData.textureManager.textures["battle"][0], (514, 48+64), GlobalData.textureManager.spriteRects["battle"][1])
            elif self.selection == 3:
                self.display.getScreen().blit(GlobalData.textureManager.textures["battle"][0], (514, 48+96), GlobalData.textureManager.spriteRects["battle"][1])
            elif self.selection == 4:
                self.display.getScreen().blit(GlobalData.textureManager.textures["battle"][0], (514, 48+128), GlobalData.textureManager.spriteRects["battle"][1])
            elif self.selection == 5:
                self.display.getScreen().blit(GlobalData.textureManager.textures["battle"][0], (514, 48+160), GlobalData.textureManager.spriteRects["battle"][1])
            elif self.selection == 6:
                self.display.getScreen().blit(GlobalData.textureManager.textures["battle"][0], (514, 48+192), GlobalData.textureManager.spriteRects["battle"][1])
            elif self.selection == 7:
                self.display.getScreen().blit(GlobalData.textureManager.textures["battle"][0], (514, 48+224), GlobalData.textureManager.spriteRects["battle"][1])        
            pygame.display.flip()
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
                            self.box = TextBox.TextBox(self.display, GlobalData.textureManager, 144, 144, "  Are you sure you want to quit?")
                            self.boxOpen = True
                            self.select = 1
                            
                            while self.boxOpen:
                                self.box.draw()
                                self.display.getScreen().blit(self.font.render("            Yes            No", 0, (255,255,255)), (168, 168))
                                if self.select == 0:
                                    self.display.getScreen().blit(GlobalData.textureManager.textures["battle"][0], (264, 168), GlobalData.textureManager.spriteRects["battle"][1])
                                elif self.select == 1:
                                    self.display.getScreen().blit(GlobalData.textureManager.textures["battle"][0], (336, 168), GlobalData.textureManager.spriteRects["battle"][1])
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
                self.display.getScreen().blit(GlobalData.textureManager.textures["battle"][0], (216, 96), GlobalData.textureManager.spriteRects["battle"][1])
            elif self.selection == 1:
                self.display.getScreen().blit(GlobalData.textureManager.textures["battle"][0], (216, 96+32), GlobalData.textureManager.spriteRects["battle"][1])
            elif self.selection == 2:
                self.display.getScreen().blit(GlobalData.textureManager.textures["battle"][0], (216, 96+64), GlobalData.textureManager.spriteRects["battle"][1])
            elif self.selection == 3:
                self.display.getScreen().blit(GlobalData.textureManager.textures["battle"][0], (216, 96+96), GlobalData.textureManager.spriteRects["battle"][1])    
            pygame.display.flip()
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
                self.display.getScreen().blit(GlobalData.textureManager.textures["battle"][0], (216, 96), GlobalData.textureManager.spriteRects["battle"][1])
            elif self.selection == 1:
                self.display.getScreen().blit(GlobalData.textureManager.textures["battle"][0], (216, 96+32), GlobalData.textureManager.spriteRects["battle"][1])
            elif self.selection == 2:
                self.display.getScreen().blit(GlobalData.textureManager.textures["battle"][0], (216, 96+64), GlobalData.textureManager.spriteRects["battle"][1])
            elif self.selection == 3:
                self.display.getScreen().blit(GlobalData.textureManager.textures["battle"][0], (216, 96+96), GlobalData.textureManager.spriteRects["battle"][1])    
            pygame.display.flip()
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
                self.display.getScreen().blit(GlobalData.textureManager.textures["battle"][0], (216, 96), GlobalData.textureManager.spriteRects["battle"][1])
            elif self.selection == 1:
                self.display.getScreen().blit(GlobalData.textureManager.textures["battle"][0], (216, 96+32), GlobalData.textureManager.spriteRects["battle"][1])
            elif self.selection == 2:
                self.display.getScreen().blit(GlobalData.textureManager.textures["battle"][0], (216, 96+64), GlobalData.textureManager.spriteRects["battle"][1])
            elif self.selection == 3:
                self.display.getScreen().blit(GlobalData.textureManager.textures["battle"][0], (216, 96+96), GlobalData.textureManager.spriteRects["battle"][1])    
            pygame.display.flip()
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
                self.display.getScreen().blit(GlobalData.textureManager.textures["battle"][0], (216, 96), GlobalData.textureManager.spriteRects["battle"][1])
            elif self.selection == 1:
                self.display.getScreen().blit(GlobalData.textureManager.textures["battle"][0], (216, 96+32), GlobalData.textureManager.spriteRects["battle"][1])
            elif self.selection == 2:
                self.display.getScreen().blit(GlobalData.textureManager.textures["battle"][0], (216, 96+64), GlobalData.textureManager.spriteRects["battle"][1])
            elif self.selection == 3:
                self.display.getScreen().blit(GlobalData.textureManager.textures["battle"][0], (216, 96+96), GlobalData.textureManager.spriteRects["battle"][1])    
            pygame.display.flip()
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
                self.display.getScreen().blit(GlobalData.textureManager.textures["battle"][0], (216, 96), GlobalData.textureManager.spriteRects["battle"][1])
            elif self.selection == 1:
                self.display.getScreen().blit(GlobalData.textureManager.textures["battle"][0], (216, 96+32), GlobalData.textureManager.spriteRects["battle"][1])
            elif self.selection == 2:
                self.display.getScreen().blit(GlobalData.textureManager.textures["battle"][0], (216, 96+64), GlobalData.textureManager.spriteRects["battle"][1])
            elif self.selection == 3:
                self.display.getScreen().blit(GlobalData.textureManager.textures["battle"][0], (216, 96+96), GlobalData.textureManager.spriteRects["battle"][1])    
            pygame.display.flip()
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
                self.display.getScreen().blit(GlobalData.textureManager.textures["battle"][0], (216, 96), GlobalData.textureManager.spriteRects["battle"][1])
            elif self.selection == 1:
                self.display.getScreen().blit(GlobalData.textureManager.textures["battle"][0], (216, 96+32), GlobalData.textureManager.spriteRects["battle"][1])
            elif self.selection == 2:
                self.display.getScreen().blit(GlobalData.textureManager.textures["battle"][0], (216, 96+64), GlobalData.textureManager.spriteRects["battle"][1])
            elif self.selection == 3:
                self.display.getScreen().blit(GlobalData.textureManager.textures["battle"][0], (216, 96+96), GlobalData.textureManager.spriteRects["battle"][1])    
            pygame.display.flip()
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
