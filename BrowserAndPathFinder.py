from LeafAnalysis import *
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import string
from tkinter import * 
import math
from TryingToGetRidOfAliasing import *

#main file combining the browser and path pages
        
class Button(object):
    def __init__(self, x, y, h,width, text, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = h
        self.text = text
        self.color = color

#For pathfinder
class Destination(object):
    def __init__(self, coordx, coordy, color):
        self.x = coordx
        self.y = coordy
        self.color = color
        self.cx = self.x +10
        self.cy = self.y + 10
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

#building the interface
def init(data):
    #leaf browser stuff
    data.cHeight = 700
    data.cWidth = 1250
    data.listNames = {}
    data.listPhotos = []
    data.families = True
    data.analyze = False
    data.upLeaf = None
    data.leafColor = None
    data.leafType = None
    data.newFamily = False
    data.drawSearch = ""
    data.drawSciSearch = ""
    data.comNameSearch = ""
    data.state = ""
    data.notFound = False
    data.notes = ""
    data.reformNotes = ""
    data.stateDescrip = ""
   
    data.searchFam = False
    data.searchSci = False
    data.searchCom = False
    data.searchState = False
    data.photoCoords ={}
    
    data.browserButtons = []
    
    data.browserButtons.append(Button(data.cWidth-200+50, 25, 50, 100, "Search by Common Family", "gray"))
    data.browserButtons.append(Button(data.cWidth-200+50, 85, 50, 100, "Search by Scientific Name", "gray"))
    data.browserButtons.append(Button(data.cWidth-200+50, 145, 50, 100, "Search by Common Name", "gray"))
    data.browserButtons.append(Button(data.cWidth-200+50, 205, 50,100,"Search by State", "gray" ))
    data.browserButtons.append(Button(data.cWidth-200+50,265,25,100, "Go To Map", "white"))
    
    
    #pathfinderstuff
    data.img = None
    data.imkey1 = None
    data.imkey2 = None
    data.points = [(40,70), (140,60),(550,60), (660,70), (40,265), (80, 265),(280, 210), \
    (300, 110), (300, 190),(350,140),(400, 110), (400,190), (440, 110), (440, 210), (550, 210), \
    (440, 250),(580,280),(660,270),(350,300),(230,390),(40,485),(80,485),(170,455),(450,400),\
    (520,380),(540,465),(660,485),(440,500), (420,540), (280,540),(220,580),(140,635), (40,685),\
    (350,630),(350,685),(660, 685),(500,580),(570,620)]
    data.destinations = {}
    count = 1
    for point in data.points:
        data.destinations[count] = Destination(point[0], point[1], "blue")
        count += 1
    data.countRed = 0
    data.startEnd = [None,None]
    data.path = None
    data.buttons = []
    data.trees = set()
    data.treeTypes = ["American Elm", "Siberian Elm", "Japanese Elm", "Cherries", "Holly Bush","Red Oak","Pin Oak", "Willow Oak", "Shingle Oak", "White Oak", "Witch Hazel Bush", "Japanese Maple", "Hedge Maple", "Red Maple", "American Sycamore", "London Planetree", "Tulip Poplar", "Honey Locust", "Black Locust", "Chinese Scholar", "Ash", "Osage Orange", "Ginkgo", "Crab Apple", "Hawthorn", "Pear", "Mulberry", "Peach", "Redbud", "Magnolia","Persian Ironwood", "Hornbeam", "Linden", "Dogwood","Bald Cypress", "Dawn Redwood", "Smoke Tree", "Crape Myrtle", "Viburnum Bush", "Parasol", "Spruce"]
    count = 0
    x = 750
    for tree in data.treeTypes:
        if 150+25*count > 400:
            count = 0
            x +=100
        data.buttons.append(Button(x,150+25*count,25,100,tree,"white"))
        count +=1
    
    data.buttons.append(Button(750,115,25,100,"Back to Browser", "white"))
    
    #switching between mapfinder and browser
    data.browser = True
    data.map = False
    
    #preventing any more clicking after three 
    data.stopClicking = False
    data.stopEverything = False
    
def mousePressed(event, data):
    # use event.x and event.y
    if data.browser:
        y = 0
        count = 0
        for key in data.photoCoords:
            x,ylim = data.photoCoords[key]
            if event.x > x and event.x <x+125 and event.y>ylim and event.y<ylim+150:
                data.notes = leafDescrip(key)
                data.reformNotes = "\n"+key
                count =0
                for c in data.notes:
                    if count%21 == 0:
                        if c != " " and count !=0:
                            data.reformNotes += "-\n"+c
                        else:
                            data.reformNotes+="\n"+c
                    else:
                        data.reformNotes +=c
                    count+=1  
        
        #list trees in particular family chosen
        for button in data.browserButtons:
            if event.x >= button.x and event.x <= button.x+button.width and event.y >= button.y and event.y <= button.y+button.height:
                if button.text == "Search by Common Family":
                    print("comfam")
                    data.searchFam = True
                    data.searchSci = False
                    data.newFamily = False
                    data.searchState = False
                    
                    data.families = True
                    data.analyze = False
                    
                    
                elif button.text == "Search by Scientific Name":
                    print("scifam")
                    data.searchFam = False
                    data.searchSci = True
                    data.searchCom = False
                    
                    data.families = True
                    data.analyze = False
                    data.searchState = False
                elif button.text == "Search by Common Name":
                    data.searchCom = True
                    data.searchFam = False
                    data.searchSci = False
                    data.searchState = False
                    
                    data.families = True
                    data.analyze = False
                elif button.text == "Search by State":
                    data.searchCom = False
                    data.searchFam = False
                    data.searchSci = False
                    data.searchState = True
                    
                    data.families = True
                    data.analyze = False
                    
                elif button.text == "Go To Map":
                    data.map = True
                    data.browser = False
    elif data.map:
        for dest in data.destinations:
            point = data.destinations[dest]
            if math.sqrt((point.cx-event.x)**2 +(point.cy-event.y)**2) <= 10:
                if point.color == "red":
                    point.color = "blue"
                    if dest == data.startEnd[0]:
                        data.startEnd[0] = None
                    elif dest == data.startEnd[1]:
                        data.startEnd[1] = None
                    data.countRed -=1
                elif point.color == "blue" and data.countRed !=2:
                    point.color = "red"
                    if data.startEnd[0] == None:
                        data.startEnd[0] = dest
                    else:
                        data.startEnd[1] = dest
                    data.countRed +=1
        for button in data.buttons:
            if button.x<event.x and button.x+button.width>event.x and button.y<event.y \
            and button.y+button.height > event.y:
                if button.text == "Back to Browser":
                    data.map = False
                    data.browser = True
                else:
                    if not data.stopEverything:
                        if not data.stopClicking:
                            if button.color=="gray":
                                button.color = "white"
                                data.trees.remove(button.text)
                            elif button.color == "white":
                                button.color = "gray"
                                data.trees.add(button.text)
                        else:
                            if button.text in data.trees:
                                if button.color=="gray":
                                    button.color = "white"
                                    data.trees.remove(button.text)
                                    data.stopClicking = False
        
        if len(data.trees)>2:
            data.stopClicking = True
            
def keyPressed(event, data):
    if data.browser:
        if event.keysym in string.ascii_letters:
            if data.searchFam:
                data.drawSearch += event.keysym
            elif data.searchSci:
                data.drawSciSearch += event.keysym
            elif data.searchCom:
                data.comNameSearch += event.keysym
            elif data.searchState:
                data.state += event.keysym
        elif event.keysym == "Return":
            data.photoCoords = {}
            if data.searchFam:
                data.stateDescrip = ""
                data.listPhotos = []
                maybeList = findTreeImages(data.drawSearch)
                if type(maybeList) == str:
                    data.listNames = []
                    data.notFound = True
                    data.families = False
                    data.analyze = False
                elif type(maybeList) == dict:
                    data.notes = ""
                    data.drawSearch = ""
                    data.listNames = maybeList
                    data.families = True
                    data.analyze = False
                    data.notFound = False
                    data.newFamily = True
            elif data.searchSci:
                data.stateDescrip = ""
                data.listPhotos = []
                maybeList = findTreeSci(data.drawSciSearch)
                if type(maybeList) == str:
                    data.listNames = []
                    data.notFound = True
                    data.families = False
                    data.analyze = False
                elif type(maybeList) == dict:
                    data.notes = ""
                    data.drawSciSearch = ""
                    data.listNames = maybeList

                    data.families = True
                    data.analyze = False
                    data.notFound = False
                    data.newFamily = True
            elif data.searchCom:
                data.stateDescrip = ""
                data.listPhotos = []
                maybeList = findSpecies(data.comNameSearch)
                if type(maybeList) == str:
                    data.listNames = []
                    data.notFound = True
                    data.families = False
                    data.analyze = False
                elif type(maybeList) == dict:
                    data.notes = ""
                    data.comNameSearch = ""
                    data.listNames = maybeList
                    
                    data.families = True
                    data.analyze = False
                    data.notFound = False
                    data.newFamily = True
            elif data.searchState:
                data.listPhotos = []
                data.reformNotes = ""
                maybeList = findTreeState(data.state)
                if type(maybeList) == str:
                    data.listNames = []
                    data.notFound = True
                    data.families = False
                    data.analyze = False
                elif type(maybeList) == dict:
                    data.notes = ""
                    data.stateDescrip = "Trees found in "+ data.state
                    data.state = ""
                    data.comNameSearch = ""
                    data.listNames = maybeList
                    
                    data.families = True
                    data.analyze = False
                    data.notFound = False
                    data.newFamily = True
                
            
        elif event.keysym == "BackSpace":
            if data.searchFam:
                data.drawSearch = data.drawSearch[:len(data.drawSearch)-1]
            elif data.searchSci:
                data.drawSciSearch = data.drawSciSearch[:len(data.drawSciSearch)-1]
            elif data.searchCom:
                data.comNameSearch = data.comNameSearch[:len(data.comNameSearch)-1]
            elif data.searchState:
                data.state = data.state[:len(data.state)-1]
        elif event.keysym == "space":
            if data.searchFam:
                data.drawSearch += " "
            elif data.searchSci:
                data.drawSciSearch += " "
            elif data.searchCom:
                data.comNameSearch += " "
            elif data.searchState:
                data.state += " "
    elif data.map:
        if not data.stopEverything:
            if event.keysym == "Return" and None not in data.startEnd and len(data.trees) != 0:
                # data.path = findPath(data.startEnd[0], data.startEnd[1],data.trees)
                data.path = copy.copy(findPath(data.startEnd[0], data.startEnd[1],data.trees))
                data.stopEverything = True
            elif event.keysym == "c":
                data.path = []
                for button in data.buttons:
                    button.color = "white"
                for dest in data.destinations:
                    data.destinations[dest].color = "blue"
                data.startEnd = [None, None]
                data.trees = set()
                data.countRed = 0
        else:
            if event.keysym == "c":
                data.stopEverything = False
                data.path = []
                for button in data.buttons:
                    button.color = "white"
                for dest in data.destinations:
                    data.destinations[dest].color = "blue"
                data.startEnd = [None, None]
                data.trees = set()
                data.countRed = 0

def timerFired(data):
    pass

def redrawAll(canvas, data):
    if data.browser:
        from PIL import Image, ImageTk
        canvas.create_rectangle(0,0,data.cWidth, 50, fill = "green")
        canvas.create_text(data.cWidth/2, 25, text = "Leaf Finder | Search for Trees By different Categories | Click on a box and start typing!")
        canvas.create_rectangle(data.cWidth-200, 0, data.cWidth, data.cHeight, fill = "dark green")
    
        for button in data.browserButtons:
            canvas.create_rectangle(button.x,button.y,button.x+button.width,button.y+button.height, fill = button.color)
            if button.text == "Go To Map":
                canvas.create_text(button.x+button.width/2, button.y+button.height/2, text = button.text, font = "Arial 8")
            else:
                canvas.create_text(button.x+button.width/2, button.y+button.height/4, text = button.text, font = "Arial 8")
        
        #search common family white space
        canvas.create_rectangle(data.cWidth-200+50, 50,data.cWidth-200+50+100, 75, fill = "white" )
    
        #search scientific name space
        canvas.create_rectangle(data.cWidth-200+50, 110,data.cWidth-200+50+100, 135, fill = "white" )
        
        #search rectangle space
        canvas.create_rectangle(data.cWidth-200+50, 170, data.cWidth-200+150, 195, fill = "white")
        
        #search state rectangle
        canvas.create_rectangle(data.cWidth-200+50, 230, data.cWidth-200+150, 255, fill = "white")
       
        
        canvas.create_text(data.cWidth-200+50, 50, font = "Arial 11", anchor = NW, text = data.drawSearch)
        canvas.create_text(data.cWidth-200+50, 110, font = "Arial 11", anchor = NW, text = data.drawSciSearch)
        canvas.create_text(data.cWidth-200+50, 170, font = "Arial 11", anchor = NW, text = data.comNameSearch)
        canvas.create_text(data.cWidth-200+50, 230, font = "Arial 11", anchor = NW, text = data.state)
    

        #Notes area
        canvas.create_rectangle(data.cWidth-200+25, 300, data.cWidth-25, 680, fill = "white")
        canvas.create_text(data.cWidth-200+30, 305,anchor=NW, text = "Notes:", font = "Arial 12 bold")
        canvas.create_text(data.cWidth-200+30, 315, anchor =NW, text = data.reformNotes)
        canvas.create_text(data.cWidth-200+30, 315, anchor =NW, text = data.stateDescrip)
        
        #drawing photos
        count = 0
        if data.families:
            data.photoCords ={}
            y = 0
            for key in data.listNames:
                x = ((30+(count)*160))
                if x%(data.cWidth-300)<165:
                    y += 1
                    x = 30
                    count = 0
                if y>=4:
                    break
                #list trees in particular family chosen
                canvas.create_text(x, -130+y*200 , text = key, anchor = NW)
                #placeholder for image b/c links from current database are not gifs
                if data.newFamily:
                    filePath = requests.get(data.listNames[key][1])
                    fileSize = Image.open(BytesIO(filePath.content))
                    photoLeaf = ImageTk.PhotoImage(fileSize)
                    data.listPhotos.append(photoLeaf) 
                data.photoCoords[key] = (x-5,-100+y*200)
                count +=1
            data.newFamily = False
            count = 0
            y = 0
            for photo in data.listPhotos:
                x = (25+160*(count))
                if x%(data.cWidth-300)<165:
                    y += 1
                    x = 25
                    count = 0
                if y>=4:
                    break
                canvas.create_image(x, -110+y*200,image = photo, anchor = NW)
                count += 1
        elif data.analyze:
            canvas.create_text(50,100, text = data.leafColor, anchor = NW)
            canvas.create_text(50,200, text = data.leafType, anchor = NW)
            canvas.create_image(400,100,image = data.upLeaf, anchor = NW)
        elif data.notFound:
            canvas.create_text(100,100, text="Trees not found in database.")
#pathfinder portion
    elif data.map:
        from PIL import Image, ImageTk
        im = Image.open("TompkinsMap.png")
        data.img = ImageTk.PhotoImage(im)
        canvas.create_image(0,0,image = data.img, anchor = NW)
        canvas.create_text(750, 20, text = "Plan Your Walk!", font = "Arial 36", anchor = NW)
        canvas.create_text(750, 65, text = "1) Choose 1-3 trees you'd like to see on your walk", font = "Arial 14", anchor = NW)
        canvas.create_text(750, 80, text = "2) Click on your start and end points", font = "Arial 14", anchor = NW)
        canvas.create_text(750, 95,text = "3) Press enter and watch your path get drawn!(blue = tree on path)", anchor = NW, font = "Arial 14")
        #how to show images not in .gif form: https://stackoverflow.com/questions/27599311/tkinter-photoimage-doesnt-not-support-png-image
        canvas.create_text(750, 435, text = "4) To make a new path, press 'c'!", anchor = NW)
        imkey1 = Image.open("LeafKeyPt1.png")
        data.imkey1 = ImageTk.PhotoImage(imkey1)
        canvas.create_image(750, 460, image = data.imkey1, anchor = NW)
        imkey2 = Image.open("LeafKeyPt2.png")
        data.imkey2 = ImageTk.PhotoImage(imkey2)
        canvas.create_image(990, 460, image = data.imkey2, anchor = NW)
        
        
        for dest in data.destinations:
            point = data.destinations[dest]
            canvas.create_oval(point.x, point.y, point.x+20, point.y+20, fill = point.color)
        
        for button in data.buttons:
            canvas.create_rectangle(button.x,button.y,button.x+button.width,button.y+button.height, fill = button.color)
            canvas.create_text(button.x+button.width/2, button.y+button.height/2, text = button.text, font = "Arial 8")
        
        
        
        line = [None, None]
        if data.path != None:
            for road in data.path:
                for point in road.split("to"):
                    # print(point)
                    if line[0] == None:
                        line[0] = data.points[int(point)-1]
                    elif line[1] == None:
                        line[1] = data.points[int(point)-1]
                canvas.create_line(line[0][0]+10, line[0][1]+10, line[1][0]+10, line[1][1]+10, fill = "red",width = 5)
                line = [None, None]
        
        highlightline = [None, None]
        if data.path != None:
            for tree in data.trees:
                for path in pathsWithTree(tree):
                    if path in data.path:
                        for point in path.split("to"):
                            if highlightline[0] == None:
                                highlightline[0] = data.points[int(point)-1]
                            elif highlightline[1] == None:
                                highlightline[1] = data.points[int(point)-1]
                    
                        canvas.create_line(highlightline[0][0]+10, highlightline[0][1]+10, highlightline[1][0]+10, highlightline[1][1]+10, fill = "cyan", width = 5)
                    
        # print(data.startEnd)
        if data.startEnd[0] != None:
            canvas.create_text(data.destinations[data.startEnd[0]].x,data.destinations[data.startEnd[0]].y, text = "start")
        if data.startEnd[1] != None:
            canvas.create_text(data.destinations[data.startEnd[1]].x, data.destinations[data.startEnd[1]].y, text = "end")
           
                
    

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    root = Tk()
    root.title("Leaf Finder")
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    redrawAll(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1250, 800)