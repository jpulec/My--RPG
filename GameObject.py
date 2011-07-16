
import Position
import pygame

class GameObject(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.position = Position.Position()
        self.type = 0  # Type 0 means ... ummm... nothing.
        self.contents = []  # Contents is what this object contains

    def getType(self):
        return self.type

    def setType(self,type):
        self.type = type
    
    def position(self):
        return self.position

    def setPosition(self,posX,posY):
        self.position.X = posX
        self.position.Y = posY

    def getContents(self):
        return self.contents

    def display(self, offsetX, offsetY, displayInfo, graphicsData):
        pass
    
    

        

    
        
