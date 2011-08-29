
import Position


class GameObject(Position.Position):
    def __init__(self):
        Position.Position.__init__(self)
        self.type = 0  # Type 0 means ... ummm... nothing.

    def getType(self):
        return self.type

    def setType(self,type):
        self.type = type


    
    

        

    
        
