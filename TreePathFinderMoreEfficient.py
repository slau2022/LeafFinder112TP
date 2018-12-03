import copy
import math

## Map Database

dictConnPoints = {1:{5,2}, 2:{1,3,6,7}, 3:{2,4,15,13}, 4:{3,18}, 5:{1,6,21},6:{5,2,7,19,20,22},7:{2,6,9},\
8:{9,10},9:{7,10, 8}, 10:{11,12,9,8}, 11:{10,12}, 12:{10,11,14}, 13:{14,3}, 14:{13,15,12,16},\
15:{3,14,17}, 16:{14,17,19}, 17:{16,15,18,25},18:{4,17,27},19:{16,24,20,6}, 20:{19,6,30,23},21:{22,5,33},22:{21,23,6,32},23:{20,22,31},24:{19,25,28},25:{24,17,26},26:{25,27,37,38},27:{26,18,36},28:{24,29,37},29:{37,28,30,34},30:{20,31,29,34},31:{23,30,34,32},32:{31,22,33},33:{21,35,32},34:{31,35,38,30,29,37},35:{34,36,33},36:{38,27,35},37:{28,29,38,34,26}, 38:{26,34,37,36}}

coordPoints = [(40,70), (140,60),(550,60), (660,70), (40,265), (80, 265),(280, 210), \
    (300, 110), (300, 190),(350,140),(400, 110), (400,190), (440, 110), (440, 210), (550, 210), \
    (440, 250),(580,280),(660,270),(350,300),(230,390),(40,485),(80,485),(170,455),(450,400),\
    (520,380),(540,465),(660,485),(440,500), (420,540), (280,540),(220,580),(140,635), (40,685),\
    (350,630),(350,685),(660, 685),(500,580),(570,620)]
    
dictPaths = {"1to2":{"American Sycamore","London Planetree", "Willow Oak","American Elm"},"2to3":{"Crab Apple","American Sycamore","Shingle Oak", "Linden", "Dogwood", "Red Oak", "Cherries", "Hedge Maple", "American Elm","London PlaneTree", "Willow Oak"}, "3to4":{"Honey Locust","Crab Apple", "Shingle Oak", "American Elm", "Dogwood"}, "4to18": {"Dogwood","London Planetree", "Shingle Oak", "American Elm", "Chinese Scholar"}, "18to27": {"American Elm", "Shingle Oak","Honey Locust","Hedge Maple","Chinese Scholar", "Holly Bush"}, "27to36": {"Crab Apple","Red Oak","American Elm", "Black Locust","Honey Locust"},"35to36":{"Japanese Maple", "Black Locust", "Ash","Ginkgo", "Crab Apple", "American Elm","Pear", "Mulberry", "Cherries"}, "33to35":{"Ash", "London Planetree", "Black Locust", "Honey Locust", "Cherries","Chinese Scholar", "Japanese Elm"},"21to33":{"Hawthorn","American Elm", "Shingle Oak", "Pear", "Chinese Scholar"}, "5to21":{"Pear","Hawthorn", "Linden","American Sycamore", "Chinese Scholar"}, "1to5":{"London Planetree", "Pear", "Linden", "Chinese Scholar", "American Sycamore", "Viburnum Bush"}, "5to6":{"Dogwood", "Witch Hazel Bush", "Viburnum Bush", "Chinese Scholar"}, "2to6":{"Americna Sycamore", "London Planetree"}, "2to7":{"Honey Locust", "Hedge Maple", "American Elm", "Red Oak"}, "8to9":{"Red Oak", "Hedge Maple", "American Elm"}, "8to10":{"Hedge Maple", "Pin Oak", "Cherries"}, "10to11": {"Honey Locust", "Pin Oak", "American Elm", "Red Oak"}, "11to12": {"Pin Oak", "Hedge Maple", "American Elm", "Red Oak"}, "10to12":{"Crab Apple", "Red Oak", "Spruce"}, "9to10":{"Pin Oak", "American Elm", "Sprue"}, "7to9":{"Cherries"}, "12to14":{"Red Oak", "Hedge Maple", "Cherries"}, "13to14":{"Hedge Maple", "American Elm"}, "3to13":{"Honey Locust","American Elm"}, "3to15":{"American Elm", "Mulberry", "Dogwood", "Red Oak"},"14to15":{"Red Oak", "White Oak", "London Planetree", "Dogwood"}, "6to7":{"London Planetree", "Pin Oak", "American Elm", "Red Oak", "Crape Myrtle"},"6to22":{"Cherries", "London Planefield","Chinese Scholar","Linden", "Redbud", "Ginkgo", "Dogwood"},"6to20":{"Dogwood", "Pin Oak", "American Elm", "Honey Locust", "Bald Cypress"}, "6to19":{"Cherries", "White Oak", "Parasol", "Red Oak", "Viburnum Bush", "Honey Locust", "Willow Oak", "Magnolia", "Pear"}, "16to19":{"Crape Myrtle", "Magnolia"}, "16to17":{"Red Oak", "Black Locust", "Crape Myrtle", "Viburnum Bush", "Red Maple"}, "14to16": {"Pin Oak", "Red Oak"}, "17to18":{"Black Locust"}, "17to25": {"Viburnum Bush", "Japanese Maple", "Witch Hazel Bush", "Black Locust", "Siberian Elm", "Cherry Trees", "Red Oak", "Osage Orange"}, "19to24":{"Japanese Maple", "Chinese Scholar","Honey Locust", "Cherry", "Tulip Poplar","American Elm", "Dawn Redwood"}, "24to25":{"American Elm", "Crab Apple", "Osage Orange"},"19to20": {"Willow Oak", "Chinese Scholar", "American Elm", "Bald Cypress"}, "20to23":{"Honey Locust", "Linden","Crab Apple", "Red Oak"}, "20to23":{"Honey Locust", "Linden","Crab Apple", "Red Oak"}, "22to23":{"Willow Oak", "American Elm", "Crab Apple"},"21to22":{"Crab Apple"}, "22to32":{"Crab Apple", "London Planetree", "Red Oak", "American  Elm", "Pear"}, "32to33":{"Crab Apple", "Hawthorn"}, "31to32":{"Crab Apple","American Elm", "Pin Oak", "Dogwood"}, "23to31": {"Honey Locust","Persian Ironwood", "Red Oak", "American Elm"}, "20to30":{"Willow Oak", "Red Oak", "White Oak"}, "30to31":{"Dogwood", "Pin Oak"}, "31to34":{"Pin Oak", "Dogwood", "Red Oak"}, "30to34":{"Pin Oak", "American Elm", "White Oak", "Holly Bush"}, "29to34":{"Viburnum Bush", "Pin Oak"}, "29to30":{"Spruce", "Chinese Scholar", "American Elm"}, "24to28":{"Pin Oak", "American Elm", "Willow Oak", "Dawn Redwood", "Spruce"}, "28to37": {"Crape Myrtle", "Viburnum Bush", "Willow Oak", "Holly Bush"}, "28to29":{"Holly Bush", "Spruce"}, "29to37":{"Holly Bush", "Pin Oak","Magnolia", "Crab Apple"}, "34to37":{"Pin Oak", "Holly Bush", "American Elm"}, "34to38":{"Cherries", "Red Oak", "American Elm", "Dogwood"}, "37to38":{"Ginkgo", "Pin Oak","Crab Apple"}, "26to38":{"Pin Oak","Hornbeam", "Willow Oak"}, "36to38":{"American Elm", "Dogwood", "Crab Apple"}, "26to37":{"Pin Oak", "Smoke Tree", "Willow Oak", "Ginkgo"},"26to27":{"Chinese Scholar", "Japanese Maple", "Peach", "Holly Bush", "Crab Apple"}, "25to26": {"American Elm", "Chinese Scholar", "Willow Oak", "Cherries"}, "15to17":{"Magnolia", "Black Locust", "White Oak"}, "34to35": {"Cherries", "Magnolia"}}

dictPathLengths = {"1to2": 10 ,"2to3": 45,"3to4":14,"4to18":23,"18to27":24,"27to36":24,"35to36":32,"33to35":31,"21to33":22,"5to21":24,"1to5":20,"5to6":5,"2to6":22,"2to7":23,"8to9":9,"8to10":5,"10to11":5,"11to12":9,"10to12":5,"9to10":5,"7to9":5,"12to14":10,"13to14":15,"3to13":13,"3to15":14,"14to15":13,"6to7":20,"6to22":26,"6to20":20,"6to19":28,"16to19":10,"16to17":14,"14to16":7,"17to18":10,"17to25":12,"19to24":12,"24to25":8,"19to20":15,"20to23":11,"22to23":10,"21to22":6,"22to32":20,"32to33":15,"31to32":10,"23to31":15,"20to30":17,"30to31":7,"31to34":15,"30to34":15,"29to34":15,"29to30":18,"24to28":17,"28to37":10,"28to29":5,"29to37":11,"34to37":16,"34to38":23,"37to38":9,"26to38":18,"36to38":15,"26to37":14,"26to27":12,"25to26":12,"15to17":8, "34to35":10}

##Find Path Using Backtracking

#takes a starting point an ending point and a list of trees to determine shortest possible paths 

#finds the weighted length of a given path
def pathLength(pathList, lengths = dictPathLengths):
    size  = 0
    for path in pathList:
        size += lengths[path]
    return size

def orderMoves(moves, end):
    pass

def pathsWithTree(tree, dict = dictPaths):
    pathsWithTree = []
    for path in dict:
        if tree in dict[path]:
            pathsWithTree.append(path)
    return pathsWithTree

def findMidpoint(p1,p2, pointCoords = coordPoints):
    d1 = pointCoords[p1-1] 
    d2 = pointCoords[p2-1]
    xM = (d1[0]-d2[0])/2
    yM = (d1[1]-d2[1])/2
    return (xM, yM)
    
def distance(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)
    
def findPathNearDest(end,tree, pointCoords = coordPoints):
    possibleTargets = pathsWithTree(tree)
    midpoints = {}
    for path in possibleTargets:
        p1, p2 = path.split("to")
        midpoints[path] = findMidpoint(p1,p2)
    bestDistance = None
    bestPath = None
    p1 = pointCoords(end-1)
    for path in midpoints:
        dist = distance(p1, midpoints[path])
        if bestDistance = None:
            bestDistance = dist
            bestPath = path
        elif dist < bestDistance:
            bestDistance = dist
            bestPath = ptah
    return path
        
def findPathNearStart(start,tree):
    possibleTargets = pathsWithTree(tree)
    midpoints = {}
    for path in possibleTargets:
        p1, p2 = path.split("to")
        midpoints[path] = findMidpoint(p1,p2)
    bestDistance = None
    bestPath = None
    p1 = pointCoords(start-1)
    for path in midpoints:
        dist = distance(p1, midpoints[path])
        if bestDistance = None:
            bestDistance = dist
            bestPath = path
        elif dist < bestDistance:
            bestDistance = dist
            bestPath = ptah
    return path

def possibleMoves(start, end, treeSet):
    possMoves = []
    for tree in treeSet:
        possMoves.append(findPathNearStart(start, tree))
        possMoves.append(findPathNearDest(start,tree))
    return possMoves

def findShortestPath(start, pathEnd.split("to"), minlength, pathListWin, path = [], possibleMoves = dictConnPoints, taken = set()):
    if start in pathEnd.split("to"):
        minlength = len(path)
        pathListWin = copy.deepcopy(path)
        return (minlength, pathListWin)
    else:
        for nextPoint in possibleMoves[start]:
            first = min(start, nextPoint)
            other = max(start, nextPoint)
            path = str(first)+"to"+str(other)
            if (minlength == None or pathLength(pathList)<minlength) and path not in taken:
                taken.add(path)
                minlengthNew, pathListWinNew = findShortestPath(nextPoint, pathEnd.split("to"), minlength, pathListWin, path = path)


def findPathToTree(start,tree):
    treePaths = set()
    for path in dictPath:
        if tree in dictPath[path]:
            treePaths.add(path)
            
    return treePaths

        
#find path wrapper
def findPathWrapper(start, end, treeSet, pathListWin,minlength, possibleMoves = dictConnPoints, possiblePaths = dictPaths, pathList = [], taken = set()):
    if len(treeSet) == 0 and end == start:
        if minlength == None:
            minlength = pathLength(pathList)
            pathListWin = copy.deepcopy(pathList)
            # print("yay", pathListWin)
            return (minlength, pathListWin)
            
        else:
            pathListWin = copy.deepcopy(pathList)
            minlength = pathLength(pathList)
            # print("yayagain", pathList, pathListWin)
            return (minlength, pathListWin)
    else:
        for nextPoint in possibleMoves[start]:
            first = min(start, nextPoint)
            other = max(start, nextPoint)
            path = str(first)+"to"+str(other)
            pathList.append(path)
            if (minlength == None or pathLength(pathList) <minlength) and path not in taken:  
                taken.add(path)
                save = []
                for tree in possiblePaths[path]:
                    if tree in treeSet:
                        treeSet.remove(tree)
                        save.append(tree)
                        
                        
                minlengthNew, pathListWinNew = findPathWrapper(nextPoint, end, treeSet,pathListWin, minlength, pathList = pathList)

                minlength = minlengthNew
                pathListWin = pathListWinNew
                
                taken.remove(path)
                pathList.remove(path)
                for tree in save:
                    treeSet.add(tree)
            else:
                pathList.remove(path)
        return (minlength, pathListWin)
#finds path
def findPath(start, end, treeSet):
    pathListWin = []
    minlength = None
    min, win = findPathWrapper(start, end, treeSet, pathListWin, minlength, possibleMoves = dictConnPoints, possiblePaths = dictPaths, pathList = [], taken = set())
    return win














