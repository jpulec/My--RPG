import string
import ImageData
import DisplayInfo
import pygame.time

    #self.maps = self.getMaps()

def getMapData():
    file1 = "data/Data.maps"
    fileToLoad = open(file1, 'r')
    mapData = dict()
    for lines in fileToLoad:
        tmpList = [x.strip() for x in lines.split(';')]
        if tmpList[0][0] == "#":
            continue
        mapData[tmpList[0]] = tmpList[1:]
        #print self.mapData[self.tmpList[0]]
        #print self.mapData[self.tmpList[0]][len(self.mapData[self.tmpList[0]])-1]
        #mapData[tmpList[0]][len(mapData[tmpList[0]])-1]  #does this do anything??? Doesn't appear so....
    fileToLoad.close()
    return mapData   


def getStats():
    file1 = "data/BaseStats.stats"
    fileToLoad = open(file1, 'r')
    statData = dict()
    for lines in fileToLoad:
        tmpList = [x.strip() for x in lines.split(';')]
        if tmpList[0][0] == "#":
            continue
        statData[tmpList[0]] = tmpList[1:]
        statData[tmpList[0]][len(tmpList[1:])-1] = statData[tmpList[0]][len(tmpList[1:])-1][:-1]                   
    fileToLoad.close()
    return statData

def getItemData():
    file1 = "data/Items.data"
    fileToLoad = open(file1, 'r')
    itemData = dict()
    for lines in fileToLoad:
        tmpList = [x.strip() for x in lines.split(';')]
        if tmpList[0][0] == "#":
            continue
        itemData[tmpList[0]] = tmpList[1:]
        itemData[tmpList[0]][len(tmpList[1:])-1] = itemData[tmpList[0]][len(tmpList[1:])-1][:-1]                   
    fileToLoad.close()
    return itemData     


statsData = getStats()
mapsData = getMapData()
itemData = getItemData()
quitFlag = 0
textureManager = ImageData.ImageData()
displayInitialized = 0
display = DisplayInfo.DisplayInfo()
timer =  pygame.time.Clock()
       
