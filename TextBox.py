import pygame
from pygame.locals import *
import ImageData
import DisplayInfo
import pygame.time

def loadTextImages(graphicsData, xNum, yNum, alpha = None):
    graphicsData.loadTexture("text", "images/textbox/box.PNG", alpha)
    for y in range(0,xNum):
        for x in range(0,yNum):
            graphicsData.spriteRects["text"].append(pygame.rect.Rect(x*24,y*24,24,24))


class TextBox:
    def __init__(self, display, graphicsData, x, y, text = ""):
        self.font = pygame.font.Font(None, 24)
        self.x = x
        self.y = y
        self.display = display
        self.graphicsData = graphicsData
        self.maxWidth = self.display.getScreenWidth() - 96        
        self.maxLength = self.display.getScreenHeight() - 96
        self.width = 48
        self.height = 48         
        self.text = text

    def battleShow(self):
        final_lines = ["Attack", "WTC", "HTC", "Item", "Run"]
        self.width = 120    
        self.xCount = self.width/24
        if self.width%24 != 0:
            self.xCount += 1
        self.yCount = len(final_lines)
        if len(final_lines) == 1:
            self.yCount +=1
        for x in range(self.xCount):
            for y in range(self.yCount):
                if x == 0:
                    if y == 0:
                        #print "topleft"
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][1])              
                    elif y == len(final_lines)-1:
                        #print "botleft"
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][7])
                    else:
                        #print "midleft"
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][4])
                elif x == self.xCount - 1 :
                    if y == 0:
                        #print "topright"
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][3])              
                    elif y == len(final_lines)-1:
                        #print "botright"
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][9])
                    else:
                        #print "midright"
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][6])
                else:
                    if y == 0:
                        #print "topmid"
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][2])              
                    elif y == len(final_lines)-1:
                        #print "botmid"
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][8])
                    else:
                        #print "center"
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][5])
                      
        self.yPlus = 0
        for x in final_lines:               
            self.display.getScreen().blit(self.font.render(x, 0, (255,255,255)), (self.x + 6, self.y + self.yPlus + 4))
            self.yPlus += 24        
    
    def draw(self): 
        final_lines = []
        requested_lines = self.text
        while self.font.size(requested_lines)[0]> self.width - 24:     
            if self.width < self.maxWidth:
                self.width += 24
            else:
                words = requested_lines.split(' ')
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
                break
        if self.width < self.maxWidth: 
            final_lines.append(requested_lines)
        self.xCount = self.width/24
        if self.width%24 != 0:
            self.xCount += 1
        self.yCount = len(final_lines)
        if len(final_lines) == 1:
            self.yCount += 1
        for x in range(self.xCount):
            for y in range(self.yCount):
                if x == 0:
                    if y == 0:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][1])              
                    elif y == len(final_lines):
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][7])
                    else:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][4])
                elif x == self.xCount - 1 :
                    if y == 0:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][3])              
                    elif y == len(final_lines):
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][9])
                    else:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][6])
                else:
                    if y == 0:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][2])              
                    elif y == len(final_lines):
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][8])
                    else:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][5])
                      
        self.yPlus = 0
        for x in final_lines:               
            self.display.getScreen().blit(self.font.render(x, 0, (255,255,255)), (self.x + 6, self.y + self.yPlus + 4))
            self.yPlus += 24        
        #pygame.display.flip()
    
        
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

class BattleMenu:
    def __init__(self, display, graphicsData, x, y, lines):
        self.font = pygame.font.Font(None, 24)
        self.x = x
        self.y = y
        self.display = display
        self.graphicsData = graphicsData
        self.maxWidth = self.display.getScreenWidth() - 96        
        self.maxLength = self.display.getScreenHeight() - 96
        self.width = 148
        self.height = 48         
        self.lines = lines
        self.lineNum = len(self.lines)-1
        self.lineOffset = 0

    def show(self):
        final_lines = []
        if self.lineNum < 5:
            final_lines = self.lines
        else:
            for x in range(5):
                final_lines[x] = self.lines[x+self.lineOffset]
     
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
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][1])              
                    elif y == self.yCount-1:
                        #print "botleft"
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][7])
                    else:
                        #print "midleft"
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][4])
                elif x == self.xCount - 1 :
                    if y == 0:
                        #print "topright"
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][3])              
                    elif y == self.yCount-1:
                        #print "botright"
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][9])
                    else:
                        #print "midright"
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][6])
                else:
                    if y == 0:
                        #print "topmid"
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][2])              
                    elif y == self.yCount-1:
                        #print "botmid"
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][8])
                    else:
                        #print "center"
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][5])
                      
        self.yPlus = 0
        for x in final_lines:            
            self.display.getScreen().blit(self.font.render(x, 0, (255,255,255)), (self.x + 6, self.y + self.yPlus + 4))
            self.yPlus += 24     
    



class BattleBox:
    def __init__(self, display, graphicsData, text = ""):
        self.font = pygame.font.Font(None, 24)
        self.x = 24
        self.y = 312
        self.display = display
        self.graphicsData = graphicsData
        self.maxWidth = 312 - 96        
        self.maxLength = 312 - 96
        self.width = 312
        self.height = 312-96      
        self.text = text
        self.lines = []
        self.lineNum = 0
        
    def draw(self):
        final_lines = []
        requested_lines = self.text
        if self.font.size(requested_lines)> self.width - 24:
            words = requested_lines.split(' ')
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
            self.linesLength = len(final_lines)
            for x in final_lines:
                if self.lineNum < 5:
                    self.lines.append(x)
                    self.lineNum += 1
                else:
                    for y in range(len(self.lines)-1):
                        self.lines[y] = self.lines[y+1]
                    self.lines[4] = x
        else: 
            if self.lineNum < 5:
                self.lines.append(requested_lines)
                self.lineNum += 1
            else:
                for x in range(len(self.lines)-1):
                    self.lines[x] = self.lines[x+1]
                self.lines[4] = requested_lines  

    def show(self):
        self.xCount = 14
        self.yCount = 5
        for x in range(self.xCount):
            for y in range(self.yCount):
                if x == 0:
                    if y == 0:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][1])              
                    elif y == self.yCount-1:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][7])
                    else:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][4])
                elif x == self.xCount - 1 :
                    if y == 0:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][3])              
                    elif y == self.yCount-1:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][9])
                    else:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][6])
                else:
                    if y == 0:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][2])              
                    elif y == self.yCount-1:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][8])
                    else:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][5])                  
        self.yPlus = 0
        for x in self.lines:            
            self.display.getScreen().blit(self.font.render(x, 0, (255,255,255)), (self.x + 6, self.y + self.yPlus + 4))
            self.yPlus += 24        
        #pygame.display.flip()
    
        
    def addText(self, text):       
        self.text = text
        self.open = True
        self.draw()
        self.show()
        pygame.display.flip()
        


class StartMenu:
    def __init__(self, display, graphicsData, themap, team):
        self.font = pygame.font.Font(None, 24)
        self.x = 48
        self.y = 48
        self.team = team
        self.display = display
        self.graphicsData = graphicsData
        self.width = 456-96
        self.height = 456-96     
        self.lines = []
        self.map = themap
        self.lineNum = 0
        self.facing = 9
        self.timer = pygame.time.Clock()
        
    def draw(self):
        final_lines = []
        requested_lines = self.text
        if self.font.size(requested_lines)> self.width - 24:
            words = requested_lines.split(' ')
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
            for x in final_lines:
                if self.lineNum < 5:
                    self.lines.append(x)
                    self.lineNum += 1
                else:
                    for y in range(len(self.lines)-1):
                        self.lines[y] = self.lines[y+1]
                    self.lines[4] = x
        else: 
            if self.lineNum < 5:
                self.lines.append(requested_lines)
                self.lineNum += 1
            else:
                for x in range(len(self.lines)-1):
                    self.lines[x] = self.lines[x+1]
                self.lines[4] = requested_lines  

    def show(self):
        self.display.getScreen().fill((0,0,0))
        self.xCount = 15
        self.yCount = 15
        for x in range(self.xCount):
            for y in range(self.yCount):
                if x == 0:
                    if y == 0:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][1])              
                    elif y == self.yCount-1:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][7])
                    else:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][4])
                elif x == self.xCount - 1 :
                    if y == 0:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][3])              
                    elif y == self.yCount-1:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][9])
                    else:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][6])
                else:
                    if y == 0:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][2])              
                    elif y == self.yCount-1:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][8])
                    else:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (self.x + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][5])                  
        self.yPlus = 0
        for x in self.lines:            
            self.display.getScreen().blit(self.font.render(x, 0, (255,255,255)), (self.x + 6, self.y + self.yPlus + 4))
            self.yPlus += 24        


        self.menuLines = ["Item", "Equipment", "HTC", "Status", "Settings", "Order", "Save", "Quit"]
        self.otherxCount = 6
        self.otheryCount = 11
        for x in range(self.otherxCount):
            for y in range(self.otheryCount):
                if x == 0:
                    if y == 0:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (456-48 + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][1])              
                    elif y == self.otheryCount-1:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (456-48 + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][7])
                    else:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (456-48 + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][4])
                elif x == self.otherxCount - 1:
                    if y == 0:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (456-48 + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][3])              
                    elif y == self.otheryCount-1:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (456-48 + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][9])
                    else:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (456-48 + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][6])
                else:
                    if y == 0:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (456-48 + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][2])              
                    elif y == self.otheryCount-1:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (456-48 + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][8])
                    else:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (456-48 + x*24, self.y + y*24), self.graphicsData.spriteRects["text"][5])                  
        self.yPlus = 0
        for x in self.menuLines:            
            self.display.getScreen().blit(self.font.render(x, 0, (255,255,255)), (456-48 + 6, self.y + self.yPlus + 4))
            self.yPlus += 32        

        self.yPlus = 0
        for x in self.team.team:
            self.display.getScreen().blit(self.graphicsData.textures[x.currentSkin][0], (96,96), self.graphicsData.spriteRects[x.currentSkin][self.facing])
            self.display.getScreen().blit(self.font.render(x.name, 0, (255,255,255)), (144, 96 + self.yPlus))
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
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (456-48 + x*24, 312 + y*24), self.graphicsData.spriteRects["text"][1])              
                    elif y == self.otheryCount-1:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (456-48 + x*24, 312 + y*24), self.graphicsData.spriteRects["text"][7])
                    else:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (456-48 + x*24, 312 + y*24), self.graphicsData.spriteRects["text"][4])
                elif x == self.otherxCount - 1:
                    if y == 0:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (456-48 + x*24, 312 + y*24), self.graphicsData.spriteRects["text"][3])              
                    elif y == self.otheryCount-1:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (456-48 + x*24, 312 + y*24), self.graphicsData.spriteRects["text"][9])
                    else:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (456-48 + x*24, 312 + y*24), self.graphicsData.spriteRects["text"][6])
                else:
                    if y == 0:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (456-48 + x*24, 312 + y*24), self.graphicsData.spriteRects["text"][2])              
                    elif y == self.otheryCount-1:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (456-48 + x*24, 312 + y*24), self.graphicsData.spriteRects["text"][8])
                    else:
                        self.display.getScreen().blit(self.graphicsData.textures["text"][0], (456-48 + x*24, 312 + y*24), self.graphicsData.spriteRects["text"][5])                  
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


        
