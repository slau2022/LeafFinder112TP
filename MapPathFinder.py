from tkinter import *
from PIL import ImageTk,Image  
import math
# from TreePathFinder import *
# from TreePathFinderMoreEfficient import *
from PathsBetweenTreesTesting import *


class Destination(object):
    def __init__(self, coordx, coordy, color):
        self.x = coordx
        self.y = coordy
        self.color = color
        self.cx = self.x +10
        self.cy = self.y + 10
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
class Button(object):
    def __init__(self, x, y, h,width, text, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = h
        self.text = text
        self.color = color
        

def init(data):
    # load data.xyz as appropriate
    data.img = None
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
    data.treeTypes = ["American Elm", "English Elm", "Siberian Elm", "Japanese Elm", "Cherries", "Holly Bush"," Red Oak"," Pin Oak", "Willow Oak", "Shingle Oak", "White Oak", "Witch Hazel Bush", "Japanese Maple", "Hedge Maple", "Red Maple", "American Sycamore", "London Planetree", "Tulip Poplar", "Honey Locust", "Black Locust", "Chinese Scholar", "Ash", "Osage Orange", "Ginkgo", "Crab Apple", "Hawthorn", "Pear", "Mulberry", "Peach", "Redbud", "Magnolia","Persian Ironwood", "Hornbeam", "Linden", "Dogwood"," Bald Cypress", "Dawn Redwood", "Smoke Tree", "Crape Myrtle", "Viburnum Bush", "Parasol", "Spruce"]
    count = 0
    x = 700
    for tree in data.treeTypes:
        if 40+25*count > 760:
            count = 0
            x = 800
        data.buttons.append(Button(x,40+25*count,25,100,tree,"white"))
        count +=1
    
def mousePressed(event, data):
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
            if button.color=="gray":
                button.color = "white"
                data.trees.remove(button.text)
            elif button.color == "white":
                button.color = "gray"
                data.trees.add(button.text)
    # print(data.startEnd, data.trees)
    
    # use event.x and event.y
    
def keyPressed(event, data):
    if event.keysym == "Return" and None not in data.startEnd and len(data.trees) != 0:
        # data.path = findPath(data.startEnd[0], data.startEnd[1],data.trees)
        data.path = findPath(data.startEnd[0], data.startEnd[1],data.trees)
        print(data.path)
    elif event.keysym == "c":
        data.path = []
        for button in data.buttons:
            button.color = "white"
        for dest in data.destinations:
            data.destinations[dest].color = "blue"
        data.startEnd = [None, None]
        data.trees = set()
        data.countRed = 0
        
    # use event.char and event.keysym
    
    

def redrawAll(canvas, data):
    data.img = ImageTk.PhotoImage(Image.open("TompkinsMap.png"))
    canvas.create_image(0,0,image = data.img, anchor = NW)
    # for i in range(20):
    #     canvas.create_line(0,i*40,800, i*40)
    #     canvas.create_line(i*40,0, i*40,800)

    for dest in data.destinations:
        point = data.destinations[dest]
        canvas.create_oval(point.x, point.y, point.x+20, point.y+20, fill = point.color)
    
    for button in data.buttons:
        canvas.create_rectangle(button.x,button.y,button.x+button.width,button.y+button.height, fill = button.color)
        canvas.create_text(button.x+button.width/2, button.y+button.height/2, text = button.text, font = "Arial 8")
    # draw in canvas
    
    line = [None, None]
    if data.path != None:
        for road in data.path:
            for point in road.split("to"):
                # print(point)
                if line[0] == None:
                    line[0] = data.points[int(point)-1]
                elif line[1] == None:
                    line[1] = data.points[int(point)-1]
            print(line)
            canvas.create_line(line[0][0]+10, line[0][1]+10, line[1][0]+10, line[1][1]+10, fill = "red")
            line = [None, None]
        

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

run(1200, 800)