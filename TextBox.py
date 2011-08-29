import pygame
from pygame.locals import *
import ImageData
import DisplayInfo
import pygame.time
import GlobalData

def loadTextImages(xNum, yNum, alpha = None):
    GlobalData.textureManager.loadTexture("text", "images/textbox/box.PNG", alpha)
    for y in range(0,xNum):
        for x in range(0,yNum):
            GlobalData.textureManager.spriteRects["text"].append(pygame.rect.Rect(x*24,y*24,24,24))


class TextBox:
    def __init__(self, x, y, text = ""):
        self.font = pygame.font.Font(None, 24)
        self.x = x
        self.y = y
        self.maxWidth = GlobalData.display.getScreenWidth() - 96        
        self.maxLength = GlobalData.display.getScreenHeight() - 96
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
                        GlobalData.display.getScreen().blit(GlobalData.textureManager.textures["text"][0], (self.x + x*24, self.y + y*24), GlobalData.textureManager.spriteRects["text"][1])              
                    elif y == len(final_lines)-1:
                        #print "botleft"
                        GlobalData.display.getScreen().blit(GlobalData.textureManager.textures["text"][0], (self.x + x*24, self.y + y*24), GlobalData.textureManager.spriteRects["text"][7])
                    else:
                        #print "midleft"
                        GlobalData.display.getScreen().blit(GlobalData.textureManager.textures["text"][0], (self.x + x*24, self.y + y*24), GlobalData.textureManager.spriteRects["text"][4])
                elif x == self.xCount - 1 :
                    if y == 0:
                        #print "topright"
                        GlobalData.display.getScreen().blit(GlobalData.textureManager.textures["text"][0], (self.x + x*24, self.y + y*24), GlobalData.textureManager.spriteRects["text"][3])              
                    elif y == len(final_lines)-1:
                        #print "botright"
                        GlobalData.display.getScreen().blit(GlobalData.textureManager.textures["text"][0], (self.x + x*24, self.y + y*24), GlobalData.textureManager.spriteRects["text"][9])
                    else:
                        #print "midright"
                        GlobalData.display.getScreen().blit(GlobalData.textureManager.textures["text"][0], (self.x + x*24, self.y + y*24), GlobalData.textureManager.spriteRects["text"][6])
                else:
                    if y == 0:
                        #print "topmid"
                        GlobalData.display.getScreen().blit(GlobalData.textureManager.textures["text"][0], (self.x + x*24, self.y + y*24), GlobalData.textureManager.spriteRects["text"][2])              
                    elif y == len(final_lines)-1:
                        #print "botmid"
                        GlobalData.display.getScreen().blit(GlobalData.textureManager.textures["text"][0], (self.x + x*24, self.y + y*24), GlobalData.textureManager.spriteRects["text"][8])
                    else:
                        #print "center"
                        GlobalData.display.getScreen().blit(GlobalData.textureManager.textures["text"][0], (self.x + x*24, self.y + y*24), GlobalData.textureManager.spriteRects["text"][5])
                      
        self.yPlus = 0
        for x in final_lines:               
            GlobalData.display.getScreen().blit(self.font.render(x, 0, (255,255,255)), (self.x + 6, self.y + self.yPlus + 4))
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
                        GlobalData.display.getScreen().blit(GlobalData.textureManager.textures["text"][0], (self.x + x*24, self.y + y*24), GlobalData.textureManager.spriteRects["text"][1])              
                    elif y == len(final_lines):
                        GlobalData.display.getScreen().blit(GlobalData.textureManager.textures["text"][0], (self.x + x*24, self.y + y*24), GlobalData.textureManager.spriteRects["text"][7])
                    else:
                        GlobalData.display.getScreen().blit(GlobalData.textureManager.textures["text"][0], (self.x + x*24, self.y + y*24), GlobalData.textureManager.spriteRects["text"][4])
                elif x == self.xCount - 1 :
                    if y == 0:
                        GlobalData.display.getScreen().blit(GlobalData.textureManager.textures["text"][0], (self.x + x*24, self.y + y*24), GlobalData.textureManager.spriteRects["text"][3])              
                    elif y == len(final_lines):
                        GlobalData.display.getScreen().blit(GlobalData.textureManager.textures["text"][0], (self.x + x*24, self.y + y*24), GlobalData.textureManager.spriteRects["text"][9])
                    else:
                        GlobalData.display.getScreen().blit(GlobalData.textureManager.textures["text"][0], (self.x + x*24, self.y + y*24), GlobalData.textureManager.spriteRects["text"][6])
                else:
                    if y == 0:
                        GlobalData.display.getScreen().blit(GlobalData.textureManager.textures["text"][0], (self.x + x*24, self.y + y*24), GlobalData.textureManager.spriteRects["text"][2])              
                    elif y == len(final_lines):
                        GlobalData.display.getScreen().blit(GlobalData.textureManager.textures["text"][0], (self.x + x*24, self.y + y*24), GlobalData.textureManager.spriteRects["text"][8])
                    else:
                        GlobalData.display.getScreen().blit(GlobalData.textureManager.textures["text"][0], (self.x + x*24, self.y + y*24), GlobalData.textureManager.spriteRects["text"][5])
                      
        self.yPlus = 0
        for x in final_lines:               
            GlobalData.display.getScreen().blit(self.font.render(x, 0, (255,255,255)), (self.x + 6, self.y + self.yPlus + 4))
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

class QuickBox:
    def __init__(self, x, y, text):
        self.box = TextBox(x, y, text)
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



   





        
