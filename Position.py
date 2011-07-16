
class Position:

    def __init__(self):
        self.containerType = 0    
        self.containerID = 0     # ContainerID = 0 means nowhere
        self.roomID = 0          # Room 0 is always the default - the "non-room"
        self.X = 0
        self.Y = 0
        
        
    def setPosition(self,x,y):
        self.X = x
        self.Y = y
        return

    def putInContainer(self,id, type=0):
        self.containerID = id
        self.containerType = type

    def moveToRoom(self,roomNumber):
        self.roomID = roomNumber

    def getContainer():
        return self.containerID

    def getContainerType():
        return self.containerType

    def getRoomID():
        return self.roomID

    def getLocation():
        return (x,y)

    

        

    

        
    
