
import Position


class GameObject(Position.Position):
    def __init__(self):
        Position.Position.__init__(self)
        self.type = 0  # Type 0 means ... ummm... nothing.
<<<<<<< HEAD
=======
        self.contents = []  # Contents is what this object contains
>>>>>>> ca2130befcd2831510f8fded56024422daa3eae2

    def getType(self):
        return self.type

    def setType(self,type):
        self.type = type

<<<<<<< HEAD
=======
    def getContents(self):
        return self.contents
>>>>>>> ca2130befcd2831510f8fded56024422daa3eae2

    
    

        

    
        
