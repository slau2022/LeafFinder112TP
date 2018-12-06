import copy
import math

#path finding and map database

## Map Database
#points that connect to each point
dictConnPoints = {1:{5,2}, 2:{1,3,6,7}, 3:{2,4,15,13}, 4:{3,18}, 5:{1,6,21},6:{5,2,7,19,20,22},7:{2,6,9},\
8:{9,10},9:{7,10, 8}, 10:{11,12,9,8}, 11:{10,12}, 12:{10,11,14}, 13:{14,3}, 14:{13,15,12,16},\
15:{3,14,17}, 16:{14,17,19}, 17:{16,15,18,25},18:{4,17,27},19:{16,24,20,6}, 20:{19,6,30,23},21:{22,5,33},22:{21,23,6,32},23:{20,22,31},24:{19,25,28},25:{24,17,26},26:{25,27,37,38},27:{26,18,36},28:{24,29,37},29:{37,28,30,34},30:{20,31,29,34},31:{23,30,34,32},32:{31,22,33},33:{21,35,32},34:{31,35,38,30,29,37},35:{34,36,33},36:{38,27,35},37:{28,29,38,34,26}, 38:{26,34,37,36}}

#coordinate points of all of the possible starts and destinatinos
coordPoints = [(40,70), (140,60),(550,60), (660,70), (40,265), (80, 265),(280, 210), \
    (300, 110), (300, 190),(350,140),(400, 110), (400,190), (440, 110), (440, 210), (550, 210), \
    (440, 250),(580,280),(660,270),(350,300),(230,390),(40,485),(80,485),(170,455),(450,400),\
    (520,380),(540,465),(660,485),(440,500), (420,540), (280,540),(220,580),(140,635), (40,685),\
    (350,630),(350,685),(660, 685),(500,580),(570,620)]

#all of the trees on each path    
dictPaths = {"1to2":{"American Sycamore","London Planetree", "Willow Oak","American Elm"},"2to3":{"Crab Apple","American Sycamore","Shingle Oak", "Linden", "Dogwood", "Red Oak", "Cherries", "Hedge Maple", "American Elm","London PlaneTree", "Willow Oak"}, "3to4":{"Honey Locust","Crab Apple", "Shingle Oak", "American Elm", "Dogwood"}, "4to18": {"Dogwood","London Planetree", "Shingle Oak", "American Elm", "Chinese Scholar"}, "18to27": {"American Elm", "Shingle Oak","Honey Locust","Hedge Maple","Chinese Scholar", "Holly Bush"}, "27to36": {"Crab Apple","Red Oak","American Elm", "Black Locust","Honey Locust"},"35to36":{"Japanese Maple", "Black Locust", "Ash","Ginkgo", "Crab Apple", "American Elm","Pear", "Mulberry", "Cherries"}, "33to35":{"Ash", "London Planetree", "Black Locust", "Honey Locust", "Cherries","Chinese Scholar", "Japanese Elm"},"21to33":{"Hawthorn","American Elm", "Shingle Oak", "Pear", "Chinese Scholar"}, "5to21":{"Pear","Hawthorn", "Linden","American Sycamore", "Chinese Scholar"}, "1to5":{"London Planetree", "Pear", "Linden", "Chinese Scholar", "American Sycamore", "Viburnum Bush"}, "5to6":{"Dogwood", "Witch Hazel Bush", "Viburnum Bush", "Chinese Scholar"}, "2to6":{"Americna Sycamore", "London Planetree"}, "2to7":{"Honey Locust", "Hedge Maple", "American Elm", "Red Oak"}, "8to9":{"Red Oak", "Hedge Maple", "American Elm"}, "8to10":{"Hedge Maple", "Pin Oak", "Cherries"}, "10to11": {"Honey Locust", "Pin Oak", "American Elm", "Red Oak"}, "11to12": {"Pin Oak", "Hedge Maple", "American Elm", "Red Oak"}, "10to12":{"Crab Apple", "Red Oak", "Spruce"}, "9to10":{"Pin Oak", "American Elm", "Sprue"}, "7to9":{"Cherries"}, "12to14":{"Red Oak", "Hedge Maple", "Cherries"}, "13to14":{"Hedge Maple", "American Elm"}, "3to13":{"Honey Locust","American Elm"}, "3to15":{"American Elm", "Mulberry", "Dogwood", "Red Oak"},"14to15":{"Red Oak", "White Oak", "London Planetree", "Dogwood"}, "6to7":{"London Planetree", "Pin Oak", "American Elm", "Red Oak", "Crape Myrtle"},"6to22":{"Cherries", "London Planefield","Chinese Scholar","Linden", "Redbud", "Ginkgo", "Dogwood"},"6to20":{"Dogwood", "Pin Oak", "American Elm", "Honey Locust", "Bald Cypress"}, "6to19":{"Cherries", "White Oak", "Parasol", "Red Oak", "Viburnum Bush", "Honey Locust", "Willow Oak", "Magnolia", "Pear"}, "16to19":{"Crape Myrtle", "Magnolia"}, "16to17":{"Red Oak", "Black Locust", "Crape Myrtle", "Viburnum Bush", "Red Maple"}, "14to16": {"Pin Oak", "Red Oak"}, "17to18":{"Black Locust"}, "17to25": {"Viburnum Bush", "Japanese Maple", "Witch Hazel Bush", "Black Locust", "Siberian Elm", "Cherry Trees", "Red Oak", "Osage Orange"}, "19to24":{"Japanese Maple", "Chinese Scholar","Honey Locust", "Cherry", "Tulip Poplar","American Elm", "Dawn Redwood"}, "24to25":{"American Elm", "Crab Apple", "Osage Orange"},"19to20": {"Willow Oak", "Chinese Scholar", "American Elm", "Bald Cypress"}, "20to23":{"Honey Locust", "Linden","Crab Apple", "Red Oak"}, "20to23":{"Honey Locust", "Linden","Crab Apple", "Red Oak"}, "22to23":{"Willow Oak", "American Elm", "Crab Apple"},"21to22":{"Crab Apple"}, "22to32":{"Crab Apple", "London Planetree", "Red Oak", "American  Elm", "Pear"}, "32to33":{"Crab Apple", "Hawthorn"}, "31to32":{"Crab Apple","American Elm", "Pin Oak", "Dogwood"}, "23to31": {"Honey Locust","Persian Ironwood", "Red Oak", "American Elm"}, "20to30":{"Willow Oak", "Red Oak", "White Oak"}, "30to31":{"Dogwood", "Pin Oak"}, "31to34":{"Pin Oak", "Dogwood", "Red Oak"}, "30to34":{"Pin Oak", "American Elm", "White Oak", "Holly Bush"}, "29to34":{"Viburnum Bush", "Pin Oak"}, "29to30":{"Spruce", "Chinese Scholar", "American Elm"}, "24to28":{"Pin Oak", "American Elm", "Willow Oak", "Dawn Redwood", "Spruce"}, "28to37": {"Crape Myrtle", "Viburnum Bush", "Willow Oak", "Holly Bush"}, "28to29":{"Holly Bush", "Spruce"}, "29to37":{"Holly Bush", "Pin Oak","Magnolia", "Crab Apple"}, "34to37":{"Pin Oak", "Holly Bush", "American Elm"}, "34to38":{"Cherries", "Red Oak", "American Elm", "Dogwood"}, "37to38":{"Ginkgo", "Pin Oak","Crab Apple"}, "26to38":{"Pin Oak","Hornbeam", "Willow Oak"}, "36to38":{"American Elm", "Dogwood", "Crab Apple"}, "26to37":{"Pin Oak", "Smoke Tree", "Willow Oak", "Ginkgo"},"26to27":{"Chinese Scholar", "Japanese Maple", "Peach", "Holly Bush", "Crab Apple"}, "25to26": {"American Elm", "Chinese Scholar", "Willow Oak", "Cherries"}, "15to17":{"Magnolia", "Black Locust", "White Oak"}, "34to35": {"Cherries", "Magnolia"}}

#approximate lengths of paths
dictPathLengths = {"1to2": 10 ,"2to3": 45,"3to4":14,"4to18":23,"18to27":24,"27to36":24,"35to36":32,"33to35":31,"21to33":22,"5to21":24,"1to5":20,"5to6":5,"2to6":22,"2to7":23,"8to9":9,"8to10":5,"10to11":5,"11to12":9,"10to12":5,"9to10":5,"7to9":5,"12to14":10,"13to14":15,"3to13":13,"3to15":14,"14to15":13,"6to7":20,"6to22":26,"6to20":20,"6to19":28,"16to19":10,"16to17":14,"14to16":7,"17to18":10,"17to25":12,"19to24":12,"24to25":8,"19to20":15,"20to23":11,"22to23":10,"21to22":6,"22to32":20,"32to33":15,"31to32":10,"23to31":15,"20to30":17,"30to31":7,"31to34":15,"30to34":15,"29to34":15,"29to30":18,"24to28":17,"28to37":10,"28to29":5,"29to37":11,"34to37":16,"34to38":23,"37to38":9,"26to38":18,"36to38":15,"26to37":14,"26to27":12,"25to26":12,"15to17":8, "34to35":10}

##
#finds the weighted length of a given path
def pathLength(pathList, lengths = dictPathLengths):
    size  = 0
    for path in pathList:
        size += lengths[path]
    return size

#find all the paths with a particular tree on it
def pathsWithTree(tree, dict = dictPaths):
    pathsWithTree = []
    for path in dict:
        if tree in dict[path]:
            pathsWithTree.append(path)
    return pathsWithTree
    """Returns list...have to go through this list of pathnames and figure out
        which one is closest to start and closest to destination"""
    
#find midpoint of a path
def findMidpoint(p1,p2, pointCoords = coordPoints):
    d1 = pointCoords[p1-1] 
    d2 = pointCoords[p2-1]
    xM = (d1[0]+10+d2[0]+10)/2
    yM = (d1[1]+10+d2[1]+10)/2
    return (xM, yM)
 
#find distance between two points
def distance(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

#################
#WORKS Find Path With Trees Closest to Destination and to StartPoint
#################
#find which of the paths with the tree you want is closest to destination
def findPathNearDest(end,tree, pointCoords = coordPoints):
    possibleTargets = pathsWithTree(tree) #list of paths that the tree is contained in
    midpoints = {}
    for path in possibleTargets:
        p1, p2 = path.split("to")
        midpoints[path] = findMidpoint(int(p1),int(p2))
    bestDistance = None
    bestPath = None
    pE = pointCoords[end-1]
    for path in midpoints:
        dist = distance(pE, midpoints[path])
        if bestDistance == None:
            bestDistance = dist
            bestPath = path
        elif dist < bestDistance:
            bestDistance = dist
            bestPath = path
    return bestPath
    """Gives you name of path with tree in it closest to destination"""

#find which of the paths with the tree you want is closest to the you
def findPathNearStart(start,tree, pointCoords = coordPoints):
    possibleTargets = pathsWithTree(tree) #list of paths that the tree is contained in
    midpoints = {}
    for path in possibleTargets:
        p1, p2 = path.split("to")
        midpoints[path] = findMidpoint(int(p1),int(p2))
    bestDistance = None
    bestPath = None
    pS = pointCoords[start-1]
    for path in midpoints:
        dist = distance(pS, midpoints[path])
        if bestDistance == None:
            bestDistance = dist
            bestPath = path
        elif dist < bestDistance:
            bestDistance = dist
            bestPath = path
    return bestPath

########
#WORKS: Returns dictionary of trees listed to their possible locations for the trip
########

#returns a list of the nearest path to current position and nearest path to destination with the trees you want
def possibleMoves(start, end, treeSet):
    possMoves = {}
    for tree in treeSet:
        tree = tree.strip()
        pathNearStart = {findPathNearStart(start, tree)}
        pathNearDest = {findPathNearDest(end,tree)}
        possMoves[tree] = pathNearStart.union(pathNearDest)
    return possMoves
    """maps every tree to shortest possible places to see it"""

#########
#WORKS: Takes the current possibleMoves dictionary and creates a set out of them
#########
def updateMoves(possMoves):
    moves = set()
    for key in possMoves:
        moves.update(possMoves[key])
    return moves

def treesLeft(possMoves):
    count = 0
    for tree in possMoves:
        count +=1
    return count

######################
#This definitely works
######################
#taken is a set of paths that should not be used

#for some reason, not responding to outside restriction, still taking the path, just not listing it
#anytime come across a path that's been taken already, adds the first two paths to the end
def findShortestPath(start,end,minlength, pathListWin, outsideTaken, pathList, possibleMoves = dictConnPoints):
    if pathList == None:
        pathList = []
    if start == end:
        minlength = pathLength(pathList)
        pathListWin = copy.copy(pathList)
        return (minlength, pathListWin)
    else:
        for nextPoint in possibleMoves[start]:
            first = min(start, nextPoint)
            other = max(start, nextPoint)
            path = str(first)+"to"+str(other)
            taken = copy.copy(pathList)
            pathList.append(path)
            if path not in outsideTaken:
                if (minlength == None or pathLength(pathList)<minlength) and path not in taken:
                    taken.append(path)
                    minlengthNew, pathListWinNew = findShortestPath(nextPoint, end, minlength, pathListWin,outsideTaken, copy.copy(pathList))
                    minlength = minlengthNew
                    pathListWin = pathListWinNew
                    taken.remove(path)
                    pathList.remove(path)
                else:
                    pathList.remove(path)
            else:
                pathList.remove(path)
        return (minlength, pathListWin)
        
########
#WORKS: Finds path to two sides of the target path
########

#find shortest path to the first point of the path
def findShortestPathOne(start, pathTarget, minlength, pathListWin, pathList, outsideTaken, possibleMoves = dictConnPoints, taken = set()):
    # print(int(pathTarget.split("to")[0]))
    if pathList == None:
        pathList =[]
    if start == int(pathTarget.split("to")[0]):
        minlength = pathLength(pathList)
        pathListWin = copy.copy(pathList)
        # if pathTarget not in pathListWin:
        #     pathListWin.append(pathTarget)
        return (minlength, pathListWin)
    else:
        for nextPoint in possibleMoves[start]:
            first = min(start, nextPoint)
            other = max(start, nextPoint)
            path = str(first)+"to"+str(other)
            pathList.append(path)
            if (minlength == None or pathLength(pathList)<minlength) and path not in taken and path not in outsideTaken:
                taken.add(path)
                minlengthNew, pathListWinNew = findShortestPathOne(nextPoint, pathTarget, minlength, pathListWin, copy.copy(pathList), outsideTaken)
                minlength = minlengthNew
                pathListWin = pathListWinNew
                taken.remove(path)
                pathList.remove(path)
            else:
                pathList.remove(path)
        return (minlength, pathListWin)

#find shortest path to the second point of the path
def findShortestPathTwo(start, pathTarget, minlength, pathListWin, pathList, outsideTaken, possibleMoves = dictConnPoints, taken = set()):
    # print(pathTarget)
    if pathList == None:
        pathList = []
    if start == int(pathTarget.split("to")[1]):
        minlength = pathLength(pathList)
        pathListWin = copy.copy(pathList)
        # if pathTarget not in pathListWin:
        #     pathListWin.append(pathTarget)
        return (minlength, pathListWin)
    else:
        for nextPoint in possibleMoves[start]:
            first = min(start, nextPoint)
            other = max(start, nextPoint)
            path = str(first)+"to"+str(other)
            pathList.append(path)
            if (minlength == None or pathLength(pathList)<minlength) and path not in taken and path not in outsideTaken:
                taken.add(path)
                minlengthNew, pathListWinNew = findShortestPathTwo(nextPoint, pathTarget, minlength, pathListWin, copy.copy(pathList), outsideTaken)
                minlength = minlengthNew
                pathListWin = pathListWinNew
                taken.remove(path)
                pathList.remove(path)
            else:
                pathList.remove(path)
        return (minlength, pathListWin)

#######
#WORKS: Keeps track of other trees seen on the way to destination
#######
#returns a list of trees from your target list that have been seen in a path already
def otherTreesSeen(pathList, treeSet, dict = dictPaths):
    seen = set()
    for path in pathList:
        for tree in dict[path]:
            if tree in treeSet:
                seen.add(tree)
    return seen
    
#So i got to pass down this list of trees mapped to their locations try 1 of the two of them
    #when i'm trying one of the two of them I have two more options, one side or the other side
    #try one side then back track
    #try the other side then back track
        #Then each time I move down a depth, I remove that tree from that dictionary and from the set
        #then I update the locations of the trees i want to go to(recall possibleMoves)
#then back track to the choice of the tree
#also have to keep track of current point

#what if two trees belong to the same spot path, i think should be fine...?just also check if you see any of the other trees on that path and then remove them too
#what if a tree's nearest spot is also its farthest
#tree's spot is closest and farthest, should be cancelled b/c sets

#for all shortest path finders, have to add another parameter of paths you can't take anymore
def findMegaPaths(possMoves, start, end, minlength, treeSet, pathListWin, pathList):
    if pathList == None:
        pathList = []
    if start == end and len(treeSet) == 0:
        minlength = pathLength(pathList)
        pathListWin = copy.copy(pathList)
        # print("winner", pathListWin)
        
        return (minlength, pathListWin)
    else:
        #once you've seen all the trees, find shortest path to the end
        if len(possMoves) == 0:
            length, lastpath = findShortestPath(start,  end, None, [],  set(copy.copy(pathList)), None) #pathlist put in as taken
            if len(lastpath) == 0:
                return (minlength, pathListWin)
            slice = len(pathList)
            pathList.extend(lastpath)
            if minlength == None or pathLength(pathList)<= minlength:
                minlengthNew, pathListWinNew = findMegaPaths(possMoves, end, end, minlength, treeSet, pathListWin, pathList = copy.copy(pathList))
                minlength = minlengthNew
                pathListWin = copy.copy(pathListWinNew)
                pathList = pathList[:slice]
            else:
                pathList = pathList[:slice]
        else:
            possMoves = possibleMoves(start,end,treeSet)
            
            for treeLocation in possMoves:
                for treeInstance in possMoves[treeLocation]:
                    #try with the first side of the path
                    #found the way to one side of the path
                    length, maybeTheWay = findShortestPathOne(start, treeInstance, None,  [], None, copy.copy(pathList))
                    
                    #save where you're adding in case the path doesn't work out
                    slice = len(pathList) 
                    pathList.extend(maybeTheWay)
                    if minlength == None or pathLength(pathList) < minlength:
                        save = {}
                        save[treeLocation] = copy.copy(possMoves[treeLocation])
                        del possMoves[treeLocation]
                        treeSet.remove(treeLocation)
                        #remove any other trees seen
                        othersSeen = otherTreesSeen(copy.copy(pathList), treeSet)
                        for otherSeenTree in othersSeen:
                            save[otherSeenTree] = copy.copy(possMoves[otherSeenTree])
                            del possMoves[otherSeenTree]
                            treeSet.remove(otherSeenTree)
                        #location is now on the other side of the path
                        if treeInstance in pathList:
                            minlengthNew, pathListWinNew = findMegaPaths(possMoves, int(treeInstance.split("to")[0]), end, minlength,treeSet, pathListWin, pathList = copy.copy(pathList))
                        else:
                            pathList.append(treeInstance)
                            minlengthNew, pathListWinNew = findMegaPaths(possMoves, int(treeInstance.split("to")[1]), end, minlength,treeSet, pathListWin, pathList = copy.copy(pathList))
                        #update minlength and pathListWin
                        minlength = minlengthNew
                        pathListWin = copy.copy(pathListWinNew)
                        #put everything back
                        for savedRemovedTree in save:
                            possMoves[savedRemovedTree] = save[savedRemovedTree]
                            treeSet.add(savedRemovedTree)
                        save.clear()
                        pathList = pathList[:slice]
                    else:
                        pathList = pathList[:slice]
                    
                    #do everything above but now with the second side of the path
                    length, maybeTheWayAgain = findShortestPathTwo(start, treeInstance, None, [], None, copy.copy(pathList))
                    sliceAgain = len(pathList)
                    pathList.extend(maybeTheWayAgain)
                    if minlength == None or pathLength(pathList) <minlength:
                        save = {}
                        save[treeLocation] = copy.copy(possMoves[treeLocation])
                        del possMoves[treeLocation]
                        treeSet.remove(treeLocation)
                        othersSeen = otherTreesSeen(copy.copy(pathList), treeSet)
                        for otherSeenTree in othersSeen:
                            save[otherSeenTree] = copy.copy(possMoves[otherSeenTree])
                            del possMoves[otherSeenTree]
                            treeSet.remove(otherSeenTree)
                        #location is now at the other side of the path
                        if treeInstance in pathList:
                            minlengthNew, pathListWinNew = findMegaPaths(possMoves, int(treeInstance.split("to")[1]), end, minlength,treeSet, pathListWin, pathList = copy.copy(pathList))
                        else:
                            pathList.append(treeInstance)
                            minlengthNew, pathListWinNew = findMegaPaths(possMoves, int(treeInstance.split("to")[0]), end, minlength,treeSet, pathListWin, pathList = copy.copy(pathList))
                        minlength = minlengthNew
                        pathListWin = copy.copy(pathListWinNew)
                        #put everything back
                        for savedRemovedTree in save:
                            possMoves[savedRemovedTree] = save[savedRemovedTree]
                            treeSet.add(savedRemovedTree)
                        save.clear()
                        pathList = pathList[:sliceAgain]
                    else:
                        pathList = pathList[:sliceAgain]
        return (minlength, pathListWin)
        


#finds path
def findPath(start, end, treeSet):
    win = None
    possMoves = possibleMoves(start,end,treeSet)
    min, win = findMegaPaths(copy.copy(possMoves), start, end, None, treeSet, [], None)
    return win