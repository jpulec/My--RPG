
import pygame

class DisplayInfo:
    def __init__(self):
        self.screenheight = 456
        self.screenwidth = 600
        self.isFullscreen = 0 # changed for testing
        self.window = pygame.rect.Rect(0, 0, self.screenwidth-1, self.screenheight-1)
        self.screen = None
        self.iconSurface = None
        pygame.mouse.set_visible(0) 

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
        self.iconSurface = pygame.image.load("images/sword.gif")
        pygame.display.set_icon(self.iconSurface)
        
        self.screen = pygame.display.set_mode((self.screenwidth,
                                                self.screenheight),
                                                (pygame.FULLSCREEN * self.isFullscreen))
            
        self.screen.convert()
        pygame.display.set_caption("RPG!")
        self.checkWindowSize()
        self.displayInitilized = 1

    def getScreen(self):
        return self.screen

    def getWindow(self):
        return self.window
        
        
