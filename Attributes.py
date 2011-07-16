attributeNames = ["HP","HTC","WTC","ATK","ACC","DEF","DEX","SPD","LUCK","ASS"]
skills = []


class Attributes:
    def __init__(self):
        self.stats = [0,0,0,0,0,0,0,0,0,0]
        self.skills = dict()  
     
    def increaseAttr(self, attr, amount):
        attrInd = attributeNames.index(attr)
        self.stats[attrInd] += amount
      
    def increaseSkill(self, skill, amount):
        skill = skill.capitalize()
        skillInd = skills.has_key(skill)
        self.skills[skillInd] += amount
        
    def maxHP(self):
        return self.stats[0]            
     
    def maxHTC(self):
        return self.stats[1]
        
    def maxWTC(self):
        return self.stats[2]
        
    def getAttr(self, attr):
        return self.stats[attributeNames.index(attr)]
        
        
        
                   
