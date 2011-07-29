import pygame, os
pygame.init()
pygame.font.init()
from pygame.locals import *
import pygame.time
import ImageData
import string
import pickle

class DisplayInfo:
    def __init__(self):
        self.screenheight = 1248
        self.screenwidth = 768
        self.isFullscreen = 0 # changed for testing
        self.window = pygame.rect.Rect(0, 0, self.screenwidth-1, self.screenheight-1)
        self.screen = None
        self.iconSurface = None
        pygame.mouse.set_visible(1)  #changed for testing 

    def getScreenHeight(self):
        return self.screenheight

    def getScreenWidth(self):
        return self.screenwidth

    def setScreenSize(self, sizeX, sizeY):
        self.screenheight = sizeY
        self.screenwidth = sizeX
        self.checkWindowSize()

    def setWindow(self, startX, startY, sizeX, sizeY):
        self.window = pygame.rect.Rect(startX, startY, (sizeX - startX)-1, (sizeY - startY)-1)
        self.checkWindowSize()
        

    def checkWindowSize(self):
        " Makes sure the window is fully inside the screen. "
        if (self.window.left < self.screenwidth -1):
            self.window.left = 0
        if (self.window.top < self.screenheight -1):
            self.window.top = 0

        if (self.window.right >= self.screenwidth):
            self.window.right = (self.screenwidth - self.left) -1

        if (self.window.bottom >= self.screenheight):
            self.window.bottom = (self.screenheight - self.top)-1

        if (self.screen is not None):
            self.screen.set_clip(self.window)

    
    def createScreen(self):
        #self.iconSurface = pygame.image.load("pygame.bmp")
        #pygame.display.set_icon(self.iconSurface)
        
        self.screen = pygame.display.set_mode((self.screenwidth,
                                                self.screenheight),
                                                (pygame.FULLSCREEN * self.isFullscreen))
            
        self.screen.convert()
        pygame.display.set_caption("RPG Editor!")
        self.checkWindowSize()
        self.displayInitilized = 1

    def getScreen(self):
        return self.screen

    def getWindow(self):
        return self.window 
        
        
class TextBox:
    def __init__(self, display, title, x, y, width, height, inputBool = 0, inputBoolTop = 480, inputBoolHeight = 96):
        self.font = pygame.font.Font(None, 24)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.title = title
        self.inputBool = inputBool
        self.display = display
        self.inputText = ""
        self.text = ""
        self.inputBoolHeight = inputBoolHeight
        self.inputBoolTop = inputBoolTop
        
    def show(self):
        pygame.draw.rect(self.display.getScreen(), (200,200,200), pygame.Rect(self.x, self.y, self.width, self.height))
        pygame.draw.rect(self.display.getScreen(), (0,200,200), pygame.Rect(self.x, self.y, self.width, 24))
        
        if self.inputBool == 1:
            pygame.draw.rect(self.display.getScreen(), (255,255,255), pygame.Rect(self.x + 6, self.inputBoolTop, self.width - 12, self.inputBoolHeight))
        self.display.getScreen().blit(self.font.render(self.title, 0, (0,0,0)), (self.x, self.y))  
        self.display.getScreen().blit(self.font.render(self.text, 0, (0,0,0)), (self.x, self.y + 24))
        final_lines = []
        requested_lines = self.inputText.splitlines()
        for requested_line in requested_lines:
            if self.font.size(requested_line)[0] > self.width - 24:
                words = requested_line.split(' ')
                # if any of our words are too long to fit, return.
                for word in words:
                    if self.font.size(word)[0] >= self.width - 24:
                        print "The word " + word + " is too long to fit in the rect passed."
                # Start a new line
                accumulated_line = ""
                for word in words:
                    test_line = accumulated_line + word + " "
                    # Build the line while the words fit.    
                    if self.font.size(test_line)[0] < self.width - 24:
                        accumulated_line = test_line 
                    else: 
                        final_lines.append(accumulated_line) 
                        accumulated_line = word + " " 
                final_lines.append(accumulated_line)
            else: 
                final_lines.append(requested_line)
        self.yPlus = 0
        for x in final_lines:
             self.display.getScreen().blit(self.font.render(x, 0, (0,0,0)), (self.x + 6, self.inputBoolTop + self.yPlus))
             self.yPlus += 24       
        pygame.display.flip()
    
        
    def setText(self, text):
        if self.font.size(text)[0] > self.width:
            self.width = self.font.size(text)[0]
        if self.font.size(text)[1] > self.height:
            self.height = self.font.size(text)[1]
        if self.font.size(self.title)[0] > self.width:
            self.width = self.font.size(self.title)[0]
        if self.font.size(self.title)[1] > self.height:
            self.height = self.font.size(self.title)[1]        
        self.text = text
        
    def setInputText(self, text): 
        self.inputText = text
    
    def getInputText(self, text):
        return self.inputText                 
                    

class MapTile:
    def __init__(self, textureManager, display):
        self.textureManager = textureManager
        self.display = display
        self.text = ""
        self.name = ""
        self.collision = 0
        self.rect = None
        self.backRect = None
        self.tileSet = None
        self.tileSetName = ""
        self.contents = ""
        self.portal = ""
        
    
    def display(self, x, y):
        print self.backRect
        if self.backRect is not None:
            print "Here"
            self.display.getScreen().blit(self.textureManager[tileSet][0], (x, y), self.backRect)
        self.display.getScreen().blit(self.textureManager[tileSet][0], (x, y), self.rect)
    
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
        
        
class MapLoop:
    def __init__(self):
        self.displayInitialized = 0
        self.quitFlag = 0
        self.display = DisplayInfo()
        self.textureManager = ImageData.ImageData()
        self.workingMap = [[MapTile(self.textureManager, self.display) for i in range(30)] for j in range(30)]
        self.tileArray = [[MapTile(self.textureManager, self.display) for i in range(30)] for j in range(30)]
        self.textureManager.loadTexture("collision","images/mapeditor/collision.png")
        self.selectedTile = None
        self.currentTileSet = None
        self.font = pygame.font.Font(None, 24)
        self.menuOpen = 0
        self.timer = pygame.time.Clock()
        self.tileNames = []
        self.prevY = None
        self.prevX = None

    def showSelectedTile(self):
        self.drawTileSpace()
        self.showTileSet(self.currentTileSet)
        if self.selectedTile == None:
            self.display.getScreen().blit(self.font.render("Current tile: None", 0, (255,255,255)), (48, 750))
        else:
            self.display.getScreen().blit(self.font.render("Current tile: " + str(self.selectedTile.getName()), 0, (255,255,255)), (48, 750))
        self.display.getScreen().blit(self.textureManager.textures["collision"][0], (480, 744))        
    
    def initDisplay(self):
        self.display.createScreen()
        self.displayInitilized = 1


    def mainloop(self):
        if (self.displayInitialized==0):
            self.initDisplay()
        pygame.key.set_repeat(100, 50)      
        self.loadTileSet("Exterior_Town1.png", self.textureManager, 30, 16)
        self.drawTileSpace()
        self.showTileSet("Exterior_Town1.png")
        self.loadTileNames("Exterior_Town1", 16, 30)
        


        while not self.quitFlag:
            for e in pygame.event.get():
                if e.type == QUIT:
                    quitFlag = 1
                    return
                elif e.type == KEYDOWN and e.key == K_ESCAPE:
                    self.menu()   
                elif e.type == pygame.MOUSEBUTTONDOWN or (e.type == pygame.MOUSEMOTION and e.dict["buttons"][0] == 1) or (e.type == KEYDOWN and e.key != K_ESCAPE):
                    self.userInput(e)                             
            #self.flipScreenBuffer()
            self.printCurrentMap() #need to redisplay tiles placed
            self.drawGrid()
            #self.timer.tick(2)
            self.fontNumbering()
            self.showSelectedTile()
            self.flipScreenBuffer()



        
    def flipScreenBuffer(self):
        pygame.display.flip()

    def userInput(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.MOUSEMOTION and event.dict["buttons"][0] == 1):
            self.x = event.dict["pos"][0]
            self.y = event.dict["pos"][1]
            self.x = self.x - self.x%24
            self.y = self.y - self.y%24
            if self.prevY == self.y and self.prevX == self.x:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.x >= 24 and self.x <= 720 and self.y >= 768 and self.y <= 1200:
                        self.selectedTile = self.tileArray[self.x/24 - 1][(self.y - 744)/24 - 1]
                    if self.x >= 24 and self.x <= 720 and self.y >= 24 and self.y <= 720 and self.selectedTile != None:                 
                        if self.selectedTile.getName() == "blank":
                            self.workingMap[self.x/24 - 1][self.y/24 - 1].setTileSet(None)
                            self.workingMap[self.x/24 - 1][self.y/24 - 1].setRect(None)
                            self.workingMap[self.x/24 - 1][self.y/24 - 1].setName("")
                            self.workingMap[self.x/24 - 1][self.y/24 - 1].setCollision(0)
                        else:
                            if self.workingMap[self.x/24 - 1][self.y/24 - 1].rect is None:
                                self.workingMap[self.x/24 - 1][self.y/24 - 1].setTileSet(self.selectedTile.getTileSet())
                                self.workingMap[self.x/24 - 1][self.y/24 - 1].setTileSetName(self.currentTileSet)
                                self.workingMap[self.x/24 - 1][self.y/24 - 1].setRect(self.selectedTile.getRect())
                                self.workingMap[self.x/24 - 1][self.y/24 - 1].setName(self.selectedTile.getName())
                                self.workingMap[self.x/24 - 1][self.y/24 - 1].setCollision(self.selectedTile.getCollision())
                            else:
                                if self.workingMap[self.x/24 - 1][self.y/24 - 1].rect != self.selectedTile.getRect():
                                    self.workingMap[self.x/24 - 1][self.y/24 - 1].backRect = self.workingMap[self.x/24 - 1][self.y/24 - 1].rect
                                #print self.workingMap[self.x/24 - 1][self.y/24 - 1].backRect 
                                self.workingMap[self.x/24 - 1][self.y/24 - 1].setTileSet(self.selectedTile.getTileSet())
                                self.workingMap[self.x/24 - 1][self.y/24 - 1].setTileSetName(self.currentTileSet)
                                self.workingMap[self.x/24 - 1][self.y/24 - 1].setRect(self.selectedTile.getRect())
                                self.workingMap[self.x/24 - 1][self.y/24 - 1].setName(self.selectedTile.getName())
                                self.workingMap[self.x/24 - 1][self.y/24 - 1].setCollision(self.selectedTile.getCollision())   
            elif event.type == pygame.MOUSEMOTION:
                if self.x >= 24 and self.x <= 720 and self.y >= 24 and self.y <= 720 and self.selectedTile != None:                 
                    if self.selectedTile.getName() == "blank":
                        self.workingMap[self.x/24 - 1][self.y/24 - 1].setTileSet(None)
                        self.workingMap[self.x/24 - 1][self.y/24 - 1].setRect(None)
                        self.workingMap[self.x/24 - 1][self.y/24 - 1].setName("")
                        self.workingMap[self.x/24 - 1][self.y/24 - 1].setCollision(0)
                    else:
                        if self.workingMap[self.x/24 - 1][self.y/24 - 1].rect is None:
                            self.workingMap[self.x/24 - 1][self.y/24 - 1].setTileSet(self.selectedTile.getTileSet())
                            self.workingMap[self.x/24 - 1][self.y/24 - 1].setTileSetName(self.currentTileSet)
                            self.workingMap[self.x/24 - 1][self.y/24 - 1].setRect(self.selectedTile.getRect())
                            self.workingMap[self.x/24 - 1][self.y/24 - 1].setName(self.selectedTile.getName())
                            self.workingMap[self.x/24 - 1][self.y/24 - 1].setCollision(self.selectedTile.getCollision())
                        else:
                            if self.workingMap[self.x/24 - 1][self.y/24 - 1].rect != self.selectedTile.getRect():
                                self.workingMap[self.x/24 - 1][self.y/24 - 1].backRect = self.workingMap[self.x/24 - 1][self.y/24 - 1].rect
                            #print self.workingMap[self.x/24 - 1][self.y/24 - 1].backRect 
                            self.workingMap[self.x/24 - 1][self.y/24 - 1].setTileSet(self.selectedTile.getTileSet())
                            self.workingMap[self.x/24 - 1][self.y/24 - 1].setTileSetName(self.currentTileSet)
                            self.workingMap[self.x/24 - 1][self.y/24 - 1].setRect(self.selectedTile.getRect())
                            self.workingMap[self.x/24 - 1][self.y/24 - 1].setName(self.selectedTile.getName())
                            self.workingMap[self.x/24 - 1][self.y/24 - 1].setCollision(self.selectedTile.getCollision())                     
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    if self.x >= 24 and self.x <= 720 and self.y >= 768 and self.y <= 1200:
                        self.openText = 1
                        while self.openText == 1:
                            if len(self.tileArray[self.x/24 - 1][(self.y-744)/24 - 1].getName()) > 8:
                                self.text = TextBox(self.display, self.tileArray[self.x/24 - 1][(self.y-744)/24 - 1].getName(), self.x, self.y, len(self.tileArray[self.x/24 - 1][(self.y-744)/24 - 1].getName())*12, 72)
                            else:
                                self.text = TextBox(self.display, self.tileArray[self.x/24 - 1][(self.y-744)/24 - 1].getName(), self.x, self.y, 96, 72)           
                            self.text.setText("Collision: " + str(self.tileArray[self.x/24 - 1][(self.y-744)/24 - 1].getCollision()))
                            self.text.show()
                            for e in pygame.event.get():
                                if e.type == QUIT:
                                    exit()
                                elif e.type == pygame.KEYDOWN:
                                    if e.key == K_ESCAPE:
                                        self.openText = 0
                                        break
                                    elif e.key == K_RETURN:
                                        self.textEnter = 1
                                        self.enterText = str(self.tileArray[self.x/24 - 1][(self.y-744)/24 - 1].getCollision())
                                        self.text2 = TextBox(self.display, self.tileArray[self.x/24 - 1][(self.y-744)/24 - 1].getName() + "-Edit Collision", self.x, self.y, 192, 120, 1, self.y + 48, 24)    
                                        self.text2.setText("Enter Collision:")   
                                        while self.textEnter == 1:
                                            self.text2.show()
                                            self.text2.setInputText(string.join(self.enterText, ""))    
                                            for e in pygame.event.get():
                                                if e.type == QUIT:
                                                    exit()
                                                elif e.type == KEYDOWN:
                                                    if e.key == K_ESCAPE:
                                                        self.openText = 0
                                                        self.textEnter = 0
                                                        break
                                                    elif e.key == K_BACKSPACE:
                                                        self.enterText = self.enterText[0:-1]
                                                    elif e.key <= 49 and e.key >= 48 and not self.enterText:
                                                        self.enterText = (chr(e.key))
                                                    elif e.key == K_RETURN and self.enterText:
                                                        self.textEnter = 0
                                                        self.openText = 0
                                                        break        
                                                    self.text2.setInputText(string.join(self.enterText, ""))     
                                        self.tileArray[self.x/24 - 1][(self.y-744)/24 - 1].setCollision(int(self.enterText))            
                        self.drawTileSpace()
                        self.showTileSet(self.currentTileSet)
                    if self.x >= 24 and self.x <= 720 and self.y >= 24 and self.y <= 720 and self.workingMap[self.x/24 - 1][self.y/24 - 1].getName() != "":
                        self.openText = 1
                        self.menuFontSurfs = [self.font.render("Text", 0, (255,255,255)), self.font.render("Collision", 0, (255,255,255)), self.font.render("Contents", 0, (255,255,255)), self.font.render("Portal", 0, (255,255,255))]
                        self.menuSelectedFontSurfs = [self.font.render("Text", 0, (0,255,0)), self.font.render("Collision", 0, (0,255,0)), self.font.render("Contents", 0, (0,255,0)), self.font.render("Portal", 0, (0,255,0))]
                        self.selection = 0
                        if len(self.workingMap[self.x/24 - 1][self.y/24 - 1].getName()) > 8:
                            self.text = TextBox(self.display, self.workingMap[self.x/24 - 1][self.y/24 - 1].getName(), self.x, self.y, len(self.workingMap[self.x/24 - 1][self.y/24 - 1].getName())*12, 144)
                        else:
                            self.text = TextBox(self.display, self.workingMap[self.x/24 - 1][self.y/24 - 1].getName(), self.x, self.y, 96, 144)
                        self.text.setText("Select what to edit:")
                        self.text.show()    
                        while self.openText == 1:  
                            self.yPlus = 0
                            for x in self.menuFontSurfs:   
                                self.display.getScreen().blit(x, (self.x, self.y + self.yPlus + 48))
                                self.yPlus +=24
                            if self.selection == 0:
                                self.display.getScreen().blit(self.menuSelectedFontSurfs[0], (self.x,self.y + 48))
                            if self.selection == 1:
                                self.display.getScreen().blit(self.menuSelectedFontSurfs[1], (self.x,self.y+24 + 48))
                            if self.selection == 2:
                                self.display.getScreen().blit(self.menuSelectedFontSurfs[2], (self.x,self.y+48 + 48))
                            if self.selection == 3:
                                self.display.getScreen().blit(self.menuSelectedFontSurfs[3], (self.x,self.y+72 + 48))                   
                            self.flipScreenBuffer()
                            for e in pygame.event.get():
                                if e.type == QUIT:
                                    exit()
                                if e.type == KEYDOWN and e.key == K_ESCAPE:
                                    self.openText = 0
                                    break   
                                elif e.type == KEYDOWN:
                                    key = pygame.key.get_pressed()
                                    if key[K_RETURN]:
                                        if self.selection == 0:
                                            self.textEnter = 1
                                            self.enterText = []
                                            self.text = TextBox(self.display, self.workingMap[self.x/24 - 1][self.y/24 - 1].getName() + "-Edit Text", self.x, self.y, 384, 384, 1, self.y + 48, 312)    
                                            self.text.setText("Enter text:")
                                            if self.workingMap[self.x/24 - 1][self.y/24 - 1].getText() != "":
                                                self.size = len(self.workingMap[self.x/24 - 1][self.y/24 - 1].getText())
                                                for x in range(self.size):
                                                    self.enterText.append(self.workingMap[self.x/24 - 1][self.y/24 - 1].getText()[x])   
                                            while self.textEnter == 1:
                                                self.text.show()
                                                if self.workingMap[self.x/24 - 1][self.y/24 - 1].getText() != "":
                                                    self.text.setInputText(string.join(self.enterText, ""))    
                                                for e in pygame.event.get():
                                                    if e.type == QUIT:
                                                        exit()
                                                    elif e.type == KEYDOWN:
                                                        self.mods = pygame.key.get_mods()
                                                        if e.key == K_ESCAPE:
                                                            self.openText = 0
                                                            self.textEnter = 0
                                                            break
                                                        elif e.key == K_BACKSPACE:
                                                            self.enterText = self.enterText[0:-1]
                                                        elif e.key <= 122 and e.key >= 97:
                                                            if self.mods == 4097 or self.mods == 1 or self.mods == 2:
                                                                self.enterText.append(chr(e.key-32))
                                                            else:
                                                                self.enterText.append(chr(e.key))
                                                        elif e.key == K_RETURN:
                                                            self.textEnter = 0
                                                            self.openText = 0
                                                            break        
                                                        elif e.key < 256:
                                                            self.enterText.append(chr(e.key))
                                                        self.text.setInputText(string.join(self.enterText, ""))     
                                            self.workingMap[self.x/24 - 1][self.y/24 - 1].setText(string.join(self.enterText, ""))
                                        elif self.selection == 1:
                                            self.textEnter = 1
                                            self.enterText = []
                                            if self.workingMap[self.x/24 - 1][self.y/24 - 1].getContents() != "":
                                                self.size = len(self.workingMap[self.x/24 - 1][self.y/24 - 1].getContents())
                                                for x in range(self.size):
                                                    self.enterText.append(self.workingMap[self.x/24 - 1][self.y/24 - 1].getContents()[x])
                                            self.text = TextBox(self.display, self.workingMap[self.x/24 - 1][self.y/24 - 1].getName() + "-Edit Collision", self.x, self.y, 192, 120, 1, self.y + 48, 24)    
                                            self.text.setText("Enter Collision:")   
                                            while self.textEnter == 1:
                                                self.text.show()
                                                self.text.setInputText(string.join(self.enterText, ""))    
                                                for e in pygame.event.get():
                                                    if e.type == QUIT:
                                                        exit()
                                                    elif e.type == KEYDOWN:
                                                        if e.key == K_ESCAPE:
                                                            self.openText = 0
                                                            self.textEnter = 0
                                                            break
                                                        elif e.key == K_BACKSPACE:
                                                            self.enterText = self.enterText[0:-1]
                                                        elif e.key <= 49 and e.key >= 48 and not self.enterText:
                                                            self.enterText = (chr(e.key))
                                                        elif e.key == K_RETURN and self.enterText:
                                                            self.textEnter = 0
                                                            self.openText = 0
                                                            break        
                                                        self.text.setInputText(string.join(self.enterText, ""))     
                                            self.workingMap[self.x/24 - 1][self.y/24 - 1].setCollision(int(self.enterText))
                                        elif self.selection ==2:
                                            self.textEnter = 1
                                            self.enterText = []
                                            if self.workingMap[self.x/24 - 1][self.y/24 - 1].getContents() != "":
                                                if self.workingMap[self.x/24 - 1][self.y/24 - 1].getContents() != "":
                                                    self.size = len(self.workingMap[self.x/24 - 1][self.y/24 - 1].getContents())
                                                    for x in range(self.size):
                                                        self.enterText.append(self.workingMap[self.x/24 - 1][self.y/24 - 1].getContents()[x])       
                                            self.text = TextBox(self.display, self.workingMap[self.x/24 - 1][self.y/24 - 1].getName() + "-Edit Contents", self.x, self.y, 192, 120, 1, self.y + 48, 24)    
                                            self.text.setText("Enter Contents:")   
                                            while self.textEnter == 1:
                                                self.text.show()
                                                self.text.setInputText(string.join(self.enterText, ""))    
                                                for e in pygame.event.get():
                                                    if e.type == QUIT:
                                                        exit()
                                                    elif e.type == KEYDOWN:
                                                        self.mods = pygame.key.get_mods()
                                                        if e.key == K_ESCAPE:
                                                            self.openText = 0
                                                            self.textEnter = 0
                                                            break
                                                        elif e.key == K_BACKSPACE:
                                                            self.enterText = self.enterText[0:-1]
                                                        elif e.key <= 122 and e.key >= 97:
                                                            if self.mods == 4097 or self.mods == 1 or self.mods == 2:
                                                                self.enterText.append(chr(e.key-32))
                                                            else:
                                                                self.enterText.append(chr(e.key))
                                                        elif e.key == K_RETURN:
                                                            self.textEnter = 0
                                                            self.openText = 0
                                                            break        
                                                        elif e.key < 256:
                                                            self.enterText.append(chr(e.key))    
                                            self.workingMap[self.x/24 - 1][self.y/24 - 1].setContents(string.join(self.enterText, ""))
                                        elif self.selection ==3:
                                            self.textEnter = 1
                                            self.enterText = []
                                            if self.workingMap[self.x/24 - 1][self.y/24 - 1].portal != "":
                                                self.size = len(self.workingMap[self.x/24 - 1][self.y/24 - 1].portal)
                                                for x in range(self.size):
                                                    self.enterText.append(self.workingMap[self.x/24 - 1][self.y/24 - 1].portal[x])
                                            self.text = TextBox(self.display, self.workingMap[self.x/24 - 1][self.y/24 - 1].getName() + "-Edit Portal", self.x, self.y, 192, 120, 1, self.y + 48, 24)    
                                            self.text.setText("Enter Portal Map ; startPiece:")   
                                            self.finalText = ""
                                            while self.textEnter == 1:
                                                self.text.show()
                                                
                                                self.text.setInputText(string.join(self.enterText, ""))    
                                                for e in pygame.event.get():
                                                    if e.type == QUIT:
                                                        exit()
                                                    elif e.type == KEYDOWN:
                                                        self.mods = pygame.key.get_mods()
                                                        if e.key == K_ESCAPE:
                                                            self.openText = 0
                                                            self.textEnter = 0
                                                            break
                                                        elif e.key == K_BACKSPACE:
                                                            self.enterText = self.enterText[0:-1]
                                                        elif e.key <= 122 and e.key >= 97:
                                                            if self.mods == 4097 or self.mods == 1 or self.mods == 2:
                                                                self.enterText.append(chr(e.key-32))
                                                            else:
                                                                self.enterText.append(chr(e.key))
                                                        elif e.key == K_MINUS:
                                                            if self.mods == 4097 or self.mods == 1 or self.mods == 2:
                                                                self.enterText.append(chr(e.key+50))
                                                            else:
                                                                self.enterText.append(chr(e.key))        
                                                        elif e.key == K_RETURN:
                                                            self.textEnter = 0
                                                            self.openText = 0
                                                            break        
                                                        elif e.key < 256:
                                                            self.enterText.append(chr(e.key))
                                                        self.finalText = string.join(self.enterText, "")     
                                            self.workingMap[self.x/24 - 1][self.y/24 - 1].portal = self.finalText          
                                    elif key[K_UP]:
                                        if self.selection == 0:
                                            self.selection = 3
                                        elif self.selection == 1:
                                            self.selection = 0
                                        elif self.selection == 2:
                                            self.selection = 1
                                        elif self.selection == 3:
                                            self.selection = 2    
                                    elif key[K_DOWN]:
                                        if self.selection == 0:
                                            self.selection = 1
                                        elif self.selection == 1:
                                            self.selection = 2
                                        elif self.selection == 2:
                                            self.selection = 3
                                        elif self.selection == 3:
                                            self.selection = 0                
                        self.drawTileSpace()
                        self.showTileSet(self.currentTileSet)
            self.prevY = self.y
            self.prevX = self.x
    
    def drawGrid(self):
        for k in range(0, 31):
            pygame.draw.line(self.display.getScreen(), (255,255,255), (24*(k+1), 24), (24*(k+1), 24*(31)))
        for k in range(0, 31):
            pygame.draw.line(self.display.getScreen(), (255,255,255), (24, 24*(k+1)), (24*(31), 24*(k+1)))
        
    def drawTileSpace(self):
        pygame.draw.rect(self.display.getScreen(), (255,255,255), pygame.Rect(24, 768, 24*30, 24*30))
        pygame.draw.rect(self.display.getScreen(), (255,0,0), pygame.Rect(0, 745, 768, 24))
        pygame.draw.rect(self.display.getScreen(), (255,0,0), pygame.Rect(0, 1224, 768, 24))
        pygame.draw.rect(self.display.getScreen(), (255,0,0), pygame.Rect(0, 768, 24, 288+24*8))
        pygame.draw.rect(self.display.getScreen(), (255,0,0), pygame.Rect(744, 744, 24, 288+24*8))                    
                
        
    def loadTileSet(self, mapName, graphicsData, xNum, yNum):
        graphicsData.loadTexture(mapName,"images/" + mapName)
        for y in range(0,yNum):
            for x in range(0,xNum):
                graphicsData.spriteRects[mapName].append(pygame.rect.Rect(x*24,y*24,24,24))        
        
    def showTileSet(self, tileName):
        self.texture = self.textureManager.textures[tileName][0]
        self.currentTileSet = tileName
        self.size = len(self.textureManager.spriteRects[tileName])
        self.x = 24
        self.y = 768
        for k in range(1,16*30):
            self.display.getScreen().blit(self.texture, (self.x, self.y), self.textureManager.spriteRects[tileName][k])
            self.tileArray[self.x/24 - 1][(self.y - 744)/24 - 1].setTileSet(self.texture)
            self.tileArray[self.x/24 - 1][(self.y - 744)/24 - 1].setRect(self.textureManager.spriteRects[tileName][k])
            if self.x >= 30*24:
                self.y += 24
                self.x = 24
            else:
                self.x +=24
        for k in range(0, 31):
            pygame.draw.line(self.display.getScreen(), (0,0,0), (24*(k+1), 24*32), (24*(k+1), 24*(51)))
        for k in range(31, 52):
            pygame.draw.line(self.display.getScreen(), (0,0,0), (24, 24*(k+1)), (24*31, 24*(k+1)))
       
                
    
    def fontNumbering(self):
        self.xCount = 0
        self.yCount = 0
        for x in range(30):
            self.fontSurf = self.font.render(str(self.xCount), 0, (255,255,255))                         
            self.display.getScreen().blit(self.fontSurf, (24*(x+1),6))
            self.xCount +=1
        for x in range(30):
            self.fontSurf = self.font.render(str(self.yCount), 0, (255,255,255))                         
            self.display.getScreen().blit(self.fontSurf, (6,24*(x+1)))
            self.yCount +=1
    
    def menu(self):
        self.SAVE_MAP = 0
        self.LOAD_MAP = 1
        self.LOAD_TILE_SET = 2
        self.FILL = 3
        self.QUIT = 4
        
        self.menuOpen = 1
        self.selection = 0
        self.menuFontSurfs = [self.font.render("Save Map", 0, (255,255,255)), self.font.render("Load Map", 0, (255,255,255)), self.font.render("Load Tile Set", 0, (255,255,255)), self.font.render("Fill With Selected Tile", 0, (255,255,255)), self.font.render("Quit", 0, (255,255,255))]
        self.menuSelectedFontSurfs = [self.font.render("Save Map", 0, (0,255,0)), self.font.render("Load Map", 0, (0,255,0)), self.font.render("Load Tile Set", 0, (0,255,0)), self.font.render("Fill With Selected Tile", 0, (0,255,0)), self.font.render("Quit", 0, (0,255,0))]
        
        while self.menuOpen == 1:
            pygame.draw.rect(self.display.getScreen(), (0,0,255), pygame.Rect(192, 427, 384, 192))
            self.y = 0

            for x in self.menuFontSurfs:   
                self.display.getScreen().blit(x, (336,430 + self.y))
                self.y +=24
            if self.selection == self.SAVE_MAP:
                self.display.getScreen().blit(self.menuSelectedFontSurfs[self.SAVE_MAP], (336,430))
            if self.selection == self.LOAD_MAP:
                self.display.getScreen().blit(self.menuSelectedFontSurfs[self.LOAD_MAP], (336,454))
            if self.selection == self.LOAD_TILE_SET:
                self.display.getScreen().blit(self.menuSelectedFontSurfs[self.LOAD_TILE_SET], (336,478))
            if self.selection == self.FILL:
                self.display.getScreen().blit(self.menuSelectedFontSurfs[self.FILL], (336,502))            
            if self.selection == self.QUIT:
                self.display.getScreen().blit(self.menuSelectedFontSurfs[self.QUIT], (336,526))            
            self.flipScreenBuffer()
            
            for e in pygame.event.get():
                if e.type == QUIT:
                    exit()
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    self.menuOpen = 0   
                elif e.type == KEYDOWN:
                    key = pygame.key.get_pressed()
                    if key[K_RETURN]:
                        if self.selection == self.SAVE_MAP:
                            self.saveMap()
                        elif self.selection == self.LOAD_MAP:
                            self.loadMap()
                        elif self.selection == self.LOAD_TILE_SET:
                            self.tileLoader()
                        elif self.selection == self.FILL:
                            self.fillTile()  
                        elif self.selection == self.QUIT:
                            exit()    
                                       
                    elif key[K_RIGHT]:
                        pass
                    elif key[K_UP]:
                        if self.selection == self.SAVE_MAP:
                            self.selection = self.QUIT
                        elif self.selection == self.LOAD_MAP:
                            self.selection = self.SAVE_MAP
                        elif self.selection == self.LOAD_TILE_SET:
                            self.selection = self.LOAD_MAP
                        elif self.selection == self.FILL:
                            self.selection = self.LOAD_TILE_SET
                        elif self.selection == self.QUIT:
                            self.selection = self.FILL            
                               
                    elif key[K_DOWN]:
                        if self.selection == self.SAVE_MAP:
                            self.selection = self.LOAD_MAP
                        elif self.selection == self.LOAD_MAP:
                            self.selection = self.LOAD_TILE_SET
                        elif self.selection == self.LOAD_TILE_SET:
                            self.selection = self.FILL
                        elif self.selection == self.FILL:
                            self.selection = self.QUIT    
                        elif self.selection == self.QUIT:
                            self.selection = self.SAVE_MAP                 
        self.drawTileSpace()
        self.showTileSet(self.currentTileSet)
    
    def fillTile(self):
        if self.selectedTile != None:
            for x in range(30):
                for y in range(30):
                   self.workingMap[x][y].setTileSet(self.selectedTile.getTileSet())
                   self.workingMap[x][y].setTileSetName(self.currentTileSet)
                   self.workingMap[x][y].setRect(self.selectedTile.getRect())
                   self.workingMap[x][y].setName(self.selectedTile.getName())
                   self.workingMap[x][y].setCollision(self.selectedTile.getCollision())
            self.menuOpen = 0    
        else:
            self.text = TextBox(self.display, "Error", 324, 427, 144, 168)
            self.textOpen = 1
            while self.textOpen == 1:
                self.text.setText("No Selected Tile!")
                self.text.show()
                for e in pygame.event.get():
                    if e.type == QUIT:
                        exit()
                    elif e.type == KEYDOWN:
                        if e.key == K_ESCAPE:
                            self.textOpen = 0
                            break
                    
                                                      
                     
            

    def tileLoader(self):
        self.loader = TextBox(self.display, "Load Tile Set", 324, 427, 144, 168, 1)
        self.loaderOpen = 1
        self.fileName = []
        self.xNum = []
        self.yNum = []

        while self.loaderOpen == 1:
            self.loadFile = 1
            while self.loadFile == 1:
                self.loader.setText("Enter a filename:")
                self.loader.show()
                for e in pygame.event.get():
                    if e.type == QUIT:
                        exit()
                    elif e.type == KEYDOWN:
                        self.mods = pygame.key.get_mods()
                        if e.key == K_ESCAPE:
                            self.loaderOpen = 0
                            self.loadFile = 0
                            break
                        elif e.key == K_BACKSPACE:
                            self.fileName = self.fileName[0:-1]
                        elif e.key <= 122 and e.key >= 97:
                            if self.mods == 4097 or self.mods == 1 or self.mods == 2:
                                self.fileName.append(chr(e.key-32))
                            else:
                                self.fileName.append(chr(e.key))
                        elif e.key == K_MINUS:
                            if self.mods == 4097 or self.mods == 1 or self.mods == 2:
                                self.fileName.append(chr(e.key+50))
                            else:
                                self.fileName.append(chr(e.key))
                        elif e.key == K_RETURN:
                            self.loadFile = 0
                            break        
                        elif e.key < 192:
                            self.fileName.append(chr(e.key))
                        self.loader.setInputText(string.join(self.fileName, ""))          
            self.file = string.join(self.fileName, "")
            self.xVal = 1
            if self.loaderOpen == 0:
                break
            self.loader.setInputText("") 
            while self.xVal == 1:
                self.loader.setText("Enter number of cols:")
                self.loader.show()
                for e in pygame.event.get():
                    if e.type == QUIT:
                        exit()
                    elif e.type == KEYDOWN:
                        self.mods = pygame.key.get_mods()
                        if e.key == K_ESCAPE:
                            self.loaderOpen = 0
                            self.xVal = 0
                            break
                        elif e.key == K_BACKSPACE:
                            self.xNum = self.xNum[0:-1]
                        elif e.key <= 57 and e.key >= 48:
                            self.xNum.append(chr(e.key))
                        elif e.key == K_RETURN:
                            self.xVal = 0
                            break        
                        self.loader.setInputText(string.join(self.xNum, ""))          
            self.x = string.join(self.xNum, "")
            self.yVal = 1
            if self.loaderOpen == 0:
                break
            self.loader.setInputText("") 
            while self.yVal == 1:
                self.loader.setText("Enter number of rows:")
                self.loader.show()
                for e in pygame.event.get():
                    if e.type == QUIT:
                        exit()
                    elif e.type == KEYDOWN:
                        self.mods = pygame.key.get_mods()
                        if e.key == K_ESCAPE:
                            self.loaderOpen = 0
                            self.yVal = 0
                            break
                        elif e.key == K_BACKSPACE:
                            self.yNum = self.yNum[0:-1]
                        elif e.key <= 57 and e.key >= 48:
                            self.yNum.append(chr(e.key))
                        elif e.key == K_RETURN:
                            self.yVal = 0
                            break        
                        self.loader.setInputText(string.join(self.yNum, ""))          
            self.y = string.join(self.yNum, "")
            if self.loaderOpen == 0:
                break
            try:
                self.loadTileSet(self.file, self.textureManager, int(self.x), int(self.y))
                self.loadTileNames(self.file.rstrip('.'), int(self.y), int(self.x))
                self.showTileSet(self.file)
                self.loaderOpen = 0
                self.menuOpen = 0
            except IOError:
                self.text = TextBox(self.display, "Error", 324, 427, 144, 168)
                self.textOpen = 1
                while self.textOpen == 1:
                    self.text.setText("No valid Names File!")
                    self.text.show()
                    for e in pygame.event.get():
                        if e.type == QUIT:
                            exit()
                        elif e.type == KEYDOWN:
                            if e.key == K_ESCAPE:
                                self.showTileSet(self.file)
                                self.menuOpen = 0
                                self.loaderOpen = 0
                                self.textOpen = 0
                                break
                self.loaderOpen = 0
            except KeyError:
                self.text = TextBox(self.display, "Error", 324, 427, 144, 168)
                self.textOpen = 1
                while self.textOpen == 1:
                    self.text.setText("File name KeyError!")
                    self.text.show()
                    for e in pygame.event.get():
                        if e.type == QUIT:
                            exit()
                        elif e.type == KEYDOWN:
                            if e.key == K_ESCAPE:
                                self.loaderOpen = 0
                                self.textOpen = 0
                                break
                self.loaderOpen = 0    
                
            except ValueError:
                self.text = TextBox(self.display, "Error", 324, 427, 144, 168)
                self.textOpen = 1
                while self.textOpen == 1:
                    self.text.setText("File name ValueError!")
                    self.text.show()
                    for e in pygame.event.get():
                        if e.type == QUIT:
                            exit()
                        elif e.type == KEYDOWN:
                            if e.key == K_ESCAPE:
                                self.loaderOpen = 0
                                self.textOpen = 0
                                break
                self.loadTileSet("Exterior_Town1.png", self.textureManager, 30, 20)
                self.showTileSet(self.file)                
                self.loaderOpen = 0    
    
    
    def loadTileNames(self, fileName, xNum, yNum):
        self.file = open("images/" + fileName + str(".txt"), 'r')
        self.tileNames = []
        for line in self.file:
            self.tileNames.append(line)
        self.file.close()
        self.count = 0
        self.size = len(self.tileNames)
        for x in range(xNum):
            for y in range(yNum):  
                if self.count < self.size:
                    #print self.tileNames[self.count]
                    self.tileArray[y][x].setName(self.tileNames[self.count][0:-3])
                    self.tileArray[y][x].setCollision(int(self.tileNames[self.count][-2:]))
                    self.count += 1
                               
                                    
                            
                       
        
    def saveMap(self):
        self.loader = TextBox(self.display, "Save File As:", 324, 427, 144, 168, 1)
        self.loaderOpen = 1
        self.fileName = []
        while self.loaderOpen == 1:
            self.loader.setText("Enter a filename:")
            self.loader.show()
            for e in pygame.event.get():
                if e.type == QUIT:
                    exit()
                elif e.type == KEYDOWN:
                    self.mods = pygame.key.get_mods()
                    print self.mods
                    if e.key == K_ESCAPE:
                        self.loaderOpen = 0
                        break
                    elif e.key == K_BACKSPACE:
                        self.fileName = self.fileName[0:-1]
                    elif e.key <= 122 and e.key >= 97:
                        if self.mods == 4097 or self.mods == 1 or self.mods == 2:
                            self.fileName.append(chr(e.key-32))
                        else:
                            self.fileName.append(chr(e.key))
                    elif e.key == K_MINUS:
                        if self.mods == 4097 or self.mods == 1 or self.mods == 2:
                            self.fileName.append(chr(e.key+50))
                        else:
                            self.fileName.append(chr(e.key))
                    elif e.key == K_RETURN:
                        self.loaderOpen = 0
                        break        
                    elif e.key < 256:
                        self.fileName.append(chr(e.key))
                    self.loader.setInputText(string.join(self.fileName, ""))          
        self.file = string.join(self.fileName, "")
        try:
            self.fileToWrite = open("data/" + self.file[:self.file.find('-')] + "/" + self.file, 'w')
            for x in self.workingMap:
                for y in x:
                    if y.rect is not None and y.backRect is not None:
                        self.fileToWrite.write(str(y.text) + "," + str(y.name) + "," + str(y.collision) + "," + str(y.rect.left) + "," + str(y.rect.top) + "," + str(y.tileSetName) + "," + str(y.contents) + "," + str(y.portal) + "," + str(y.backRect.left) + "," + str(y.backRect.top) + "\n")
                    elif y.rect is not None:
                        self.fileToWrite.write(str(y.text) + "," + str(y.name) + "," + str(y.collision) + "," + str(y.rect.left) + "," + str(y.rect.top) + "," + str(y.tileSetName) + "," + str(y.contents) + "," + str(y.portal) + "," + str(y.backRect) + "\n")
                    else:
                        self.fileToWrite.write(str(y.text) + "," + str(y.name) + "," + str(y.collision) + "," + str(y.rect) + "," + str(y.tileSetName) + "," + str(y.contents) + "," + str(y.portal) + "," + str(y.backRect) + "\n")
            self.fileToWrite.close()            
                            
        except IOError:
                self.text = TextBox(self.display, "Error", 324, 427, 144, 168)
                self.textOpen = 1
                while self.textOpen == 1:
                    self.text.setText("Invalid Filename!")
                    self.text.show()
                    for e in pygame.event.get():
                        if e.type == QUIT:
                            exit()
                        elif e.type == KEYDOWN:
                            if e.key == K_ESCAPE:
                                self.menuOpen = 0
                                self.textOpen = 0
                                break
                self.loaderOpen = 0
        finally:
            self.menuOpen = 0
        
    def loadMap(self):
        self.loader = TextBox(self.display, "Load File:", 324, 427, 144, 168, 1)
        self.loaderOpen = 1
        self.fileName = []
        while self.loaderOpen == 1:
            self.loader.setText("Enter a filename:")
            self.loader.show()
            for e in pygame.event.get():
                if e.type == QUIT:
                    exit()
                elif e.type == KEYDOWN:
                    self.mods = pygame.key.get_mods()
                    if e.key == K_ESCAPE:
                        self.loaderOpen = 0
                        break
                    elif e.key == K_BACKSPACE:
                        self.fileName = self.fileName[0:-1]
                    elif e.key <= 122 and e.key >= 97:
                        if self.mods == 4097 or self.mods == 1 or self.mods == 2:
                            self.fileName.append(chr(e.key-32))
                        else:
                            self.fileName.append(chr(e.key))
                    elif e.key == K_MINUS:
                        if self.mods == 4097 or self.mods == 1 or self.mods == 2:
                            self.fileName.append(chr(e.key+50))
                        else:
                            self.fileName.append(chr(e.key))
                    elif e.key == K_RETURN:
                        self.loaderOpen = 0
                        break        
                    elif e.key < 256:
                        self.fileName.append(chr(e.key))
                    self.loader.setInputText(string.join(self.fileName, ""))          
        self.file = string.join(self.fileName, "")
        try:
            self.tmpList = []
            self.fileToLoad = open("data/" + self.file[:self.file.find('-')] + "/" + self.file, 'r')
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
                        self.workingMap[x][y].rect = pygame.Rect(int(self.tmpList[3]), int(self.tmpList[4]), 24, 24)    
                    if self.tmpList[5] != "":
                        self.workingMap[x][y].tileSetName = self.tmpList[5]
                        if self.currentTileSet != self.tmpList[5]:
                            self.loadTileSet(self.tmpList[5], self.textureManager, 30, 16)
                            #self.loadTileNames(self.tmpList[5].rstrip('.'), 30, 16)
                            self.showTileSet(self.tmpList[5])
                        self.workingMap[x][y].tileSet = self.textureManager.textures[self.tmpList[5]][0]
                        if self.workingMap[x][y].rect is not None:
                            self.display.getScreen().fill((0,0,0), pygame.Rect((x+1)*24, (y+1)*24, 24, 24))      
                    self.workingMap[x][y].contents = self.tmpList[6]
                    self.workingMap[x][y].portal = self.tmpList[7]                   
                    if self.tmpList[8][:-1] == "None":
                        self.workingMap[x][y].backRect = None
                        continue
                    else:        
                        self.workingMap[x][y].backRect = pygame.Rect(int(self.tmpList[8]), int(self.tmpList[9][:-1]), 24, 24) 
            self.fileToLoad.close()                      

                    
            
        except IOError:
                self.text = TextBox(self.display, "Error", 324, 427, 144, 168)
                self.textOpen = 1
                while self.textOpen == 1:
                    self.text.setText("Invalid Filename!")
                    self.text.show()
                    for e in pygame.event.get():
                        if e.type == QUIT:
                            exit()
                        elif e.type == KEYDOWN:
                            if e.key == K_ESCAPE:
                                self.menuOpen = 0
                                self.textOpen = 0
                                break
                self.loaderOpen = 0
        finally:
            self.menuOpen = 0
    
    def printCurrentMap(self):
        self.display.getScreen().fill((0,0,0), pygame.Rect(24, 24, 744, 720)) 
        for x in range(30):
            for y in range(30):
                if self.workingMap[x][y].getRect() is not None:
                    if self.workingMap[x][y].backRect is not None:
                        self.display.getScreen().blit(self.workingMap[x][y].getTileSet(), ((x + 1)*24, (y + 1)*24), self.workingMap[x][y].backRect)           
                    self.display.getScreen().blit(self.workingMap[x][y].getTileSet(), ((x + 1)*24, (y + 1)*24), self.workingMap[x][y].getRect())
                else:
                    self.display.getScreen().fill((0,0,0), pygame.Rect((x + 1)*24, (y + 1)*24, 24, 24))        
               




if __name__=="__main__":
    map = MapLoop()
    map.mainloop()



