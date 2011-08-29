
import pygame,sys

class ImageData:
    def __init__(self):
        self.textures = dict()
        self.spriteRects = dict()

    def loadTexture(self, dictionaryEntry, textureFilename, colorKey = None):
        try:
            #completeName = os.path.join('images',textureFilename)
            if colorKey == -1:
                texture = pygame.image.load(textureFilename)
                texture.set_colorkey(texture.get_at((0,0)))
                sheetRect = texture.get_rect()
                self.textures[dictionaryEntry] = [texture,sheetRect]
                self.spriteRects[dictionaryEntry] = [sheetRect]  # Sprite 0 = whole page
                #print "Successfully loaded texture file '%s' (%s)."%(textureFilename,str(sheetRect))
            else:
                texture = pygame.image.load(textureFilename)
                sheetRect = texture.get_rect()
                self.textures[dictionaryEntry] = [texture,sheetRect]
                self.spriteRects[dictionaryEntry] = [sheetRect]  # Sprite 0 = whole page
                #print "Successfully loaded texture file '%s' (%s)."%(textureFilename,str(sheetRect))    
        except:
            print "Failed to load texture file '%s'!"%textureFilename
            return


    def assignTexture(self, dictionaryEntry, surface):
        sheetRect = surface.get_rect()
        self.textures[dictionaryEntry] = [surface,sheetRect]
        self.spriteRects[dictionaryEntry] = [sheetRect]
        

                

                    

                    
            
        
        
        
