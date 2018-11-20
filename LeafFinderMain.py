from LeafAnalysis import *
from tkinter import *
from image_util import *

## Display image from online in tkinter
# myurl = totalLeafDict["Allegheny Serviceberry"][1]
# response = requests.get(myurl)
# img = Image.open(BytesIO(response.content))
# on = cv2.imread(img)
# cv2.imshow("online",on)
#trees to look up: maple, oak, birch, spruce 
#or by scientific name

## Interface (taken fro 15112 template)
####################################
# customize these functions
####################################

class Button(object):
    def __init__(self, x, y, h,width, canvas, text, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = h
        self.text = text
        self.color = color
        canvas.create_rectangle(self.x,self.y,self.x+self.width,self.y+self.height, fill = self.color)
        canvas.create_text(self.x+self.width/2, self.y+self.height/2, text = self.text)


def init(data):
    # load data.xyz as appropriate
    data.cHeight = 600
    data.cWidth = 1000
    data.buttons = []
    data.listNames = {}
    
    
    
def mousePressed(event, data):
    # use event.x and event.y
    for button in data.buttons:
        if event.x >= button.x and event.x <= button.x+button.width and event.y >= button.y and event.y <= button.y+button.height:
            if button.text != "Search":
                data.listNames = findTreeImages(button.text)
    

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def timerFired(data):
    pass

def redrawAll(canvas, data):
    canvas.create_rectangle(0,0,data.cWidth, 50, fill = "green")
    canvas.create_text(data.cWidth/2, 25, text = "Leaf Finder")
    canvas.create_rectangle(data.cWidth-200, 0, data.cWidth, data.cHeight, fill = "dark green")
    searchButton = Button(data.cWidth-200+25, 25, 25, 100,canvas, "Search", "white" )
    maple = Button(data.cWidth-200+25,50,25,100,canvas, "Maple", "white")
    birch = Button(data.cWidth-200+25,75,25,100,canvas, "Birch", "white")
    oak = Button(data.cWidth-200+25,100,25,100,canvas, "Oak", "white")
    data.buttons.append(searchButton)
    data.buttons.append(maple)
    data.buttons.append(birch)
    data.buttons.append(oak)
    count = 0
    for key in data.listNames:
        canvas.create_text(100, 100+count*20, text = key )
        canvas.create_image(200,100+count*50, PhotoImageFromLink("https://www.cs.cmu.edu/~112/notes/hw6-112-icon.gif"), anchor = NW)
        count += 1
    
    #cite stack overflow
    

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

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
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
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1000, 600)






































