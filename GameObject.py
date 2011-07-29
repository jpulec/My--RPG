
import Position


class GameObject(Position.Position):
    def __init__(self):
        Position.Position.__init__(self)
        self.type = 0  # Type 0 means ... ummm... nothing.
        self.contents = []  # Contents is what this object contains

    def getType(self):
        return self.type

    def setType(self,type):
        self.type = type

    def getContents(self):
        return self.contents

    
    

        

    
        
