import Item

class ItemWrapper(Item.Item):
    def __init__(self, name, initNum):
        Item.Item.__init__(self, name)
        self.quantity = initNum

        
        
