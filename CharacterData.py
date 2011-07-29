import Attributes
import Creature
import pygame
pygame.font.init()
import GlobalData
                    

class CharacterData(Creature.Creature):
    def __init__(self, name):
        Creature.Creature.__init__(self, name)    #to be changed for more characters
        self.currentSkin = None
        self.equipment = []
        self.alive = True
 
        
        
