from LeafAnalysis import *
from tkinter import *
from tkinter import filedialog
from image_util import *
from WIPFunctions import *
from PIL import Image, ImageTk
import string

## Display image from online in tkinter
# myurl = totalLeafDict["Allegheny Serviceberry"][1]
# response = requests.get(myurl)
# img = Image.open(BytesIO(response.content))
# on = cv2.imread(img)
# cv2.imshow("online",on)
#trees to look up: maple, oak, birch, spruce 
#or by scientific name


####################################
# Interface (taken from 15112 template)
####################################

#creating personal button class
class Button(object):
    def __init__(self, x, y, h,width, canvas, text, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = h
        self.text = text
        self.color = color
        canvas.create_rectangle(self.x,self.y,self.x+self.width,self.y+self.height, fill = self.color)
        canvas.create_text(self.x+self.width/2, self.y+self.height/2, text = self.text, font = "Arial 8")
       
#building the interface
def init(data, root):
    # load data.xyz as appropriate
    data.cHeight = 700
    data.cWidth = 1250
    data.buttons = []
    data.listNames = {}
    data.listPhotos = []
    data.photo = PhotoImage(file = "2n2a8n.gif")
    data.families = True
    data.analyze = False
    data.upLeaf = None
    data.leafColor = None
    data.leafType = None
    data.newFamily = False
    data.drawSearch = ""
    data.drawSciSearch = ""
    data.comNameSearch = ""
    data.notFound = False
    data.notes = ""
    data.reformNotes = ""
   
    data.searchFam = False
    data.searchSci = False
    data.searchCom = False
    
    data.photoCoords ={}
    
    notes = Text(root, height = 450, width = 150)
    notes.insert(END, "hey")
    notes.place(x=data.cWidth-200+25, y =250)
    
def mousePressed(event, data, root):
    # use event.x and event.y

    y = 0
    count = 0
    for key in data.photoCoords:
        x,ylim = data.photoCoords[key]
        if event.x > x and event.x <x+125 and event.y>ylim and event.y<ylim+150:
            data.notes = leafDescrip(key)
            data.reformNotes = key+"\n"
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
    for button in data.buttons:
        if event.x >= button.x and event.x <= button.x+button.width and event.y >= button.y and event.y <= button.y+button.height:
            if button.text == "Search by Common Family":
                print("comfam")
                data.searchFam = True
                data.searchSci = False
                data.newFamily = False
                
                data.families = True
                data.analyze = False
                
            elif button.text == "Search by Scientific Name":
                print("scifam")
                data.searchFam = False
                data.searchSci = True
                data.searchCom = False
                
                data.families = True
                data.analyze = False
            elif button.text == "Search by Common Name":
                print("comnam")
                data.searchCom = True
                data.searchFam = False
                data.searchSci = False
                
                data.families = True
                data.analyze = False
            elif button.text == "Upload":
                print("upload")
                filePath = str(filedialog.askopenfilename())
                data.analyze = True
                data.families = False
                fileSize = Image.open(filePath)
                width, height = fileSize.size
                print(width, height)
                # data.leafColor = detectColor(filePath)
                # data.leafType = analyzeLeaf(filePath)
                if width > 150:
                    scale = width/150
                    img = fileSize.resize((int(width/scale), int(height/scale)), Image.ANTIALIAS)
                width2, height2 = img.size
                data.upLeaf = ImageTk.PhotoImage(img)
                print(data.upLeaf, type(data.upLeaf))
                break
                
def keyPressed(event, data):
    if event.keysym in string.ascii_letters:
        if data.searchFam:
            data.drawSearch += event.keysym
        elif data.searchSci:
            data.drawSciSearch += event.keysym
        elif data.searchCom:
            data.comNameSearch += event.keysym
    elif event.keysym == "Return":
        data.photoCoords = {}
        if data.searchFam:
            data.listPhotos = []
            maybeList = findTreeImages(data.drawSearch)
            if type(maybeList) == str:
                data.notFound = True
                data.families = False
                data.analyze = False
            elif type(maybeList) == dict:
                data.drawSearch = ""
                data.listNames = maybeList
                data.families = True
                data.analyze = False
                data.notFound = False
                data.newFamily = True
        elif data.searchSci:
            data.listPhotos = []
            maybeList = findTreeSci(data.drawSciSearch)
            if type(maybeList) == str:
                data.notFound = True
                data.families = False
                data.analyze = False
            elif type(maybeList) == dict:
                data.searchSci = ""
                data.listNames = maybeList
                
                data.families = True
                data.analyze = False
                data.notFound = False
                data.newFamily = True
        elif data.searchCom:
            data.listPhotos = []
            maybeList = findSpecies(data.comNameSearch)
            if type(maybeList) == str:
                data.notFound = True
                data.families = False
                data.analyze = False
            elif type(maybeList) == dict:
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
    elif event.keysym == "space":
        if data.searchFam:
            data.drawSearch += " "
        elif data.searchSci:
            data.drawSciSearch += " "
        elif data.searchCom:
            data.comNameSearch += " "
    

def timerFired(data):
    pass

def redrawAll(canvas, data):
    canvas.create_rectangle(0,0,data.cWidth, 50, fill = "green")
    canvas.create_text(data.cWidth/2, 25, text = "Leaf Finder")
    canvas.create_rectangle(data.cWidth-200, 0, data.cWidth, data.cHeight, fill = "dark green")
   
    searchButton = Button(data.cWidth-200+50, 25, 25, 100,canvas, "Search by Common Family", "gray")
    canvas.create_rectangle(data.cWidth-200+50, 50,data.cWidth-200+50+100, 75, fill = "white" )
   
    sciButton = Button(data.cWidth-200+50, 85, 25, 100,canvas, "Search by Scientific Name", "gray")
    canvas.create_rectangle(data.cWidth-200+50, 110,data.cWidth-200+50+100, 135, fill = "white" )
    
    comButton = Button(data.cWidth-200+50, 145, 25, 100, canvas, "Search by Common Name", "gray")
    canvas.create_rectangle(data.cWidth-200+50, 170, data.cWidth-200+150, 195, fill = "white")
    
    stateButton = Button(data.cWidth-200+50,205, 25,100,canvas,"Search by State", "gray" )
    canvas.create_rectangle(data.cWidth-200+50, 230, data.cWidth-200+150, 255, fill = "white")
    
    canvas.create_text(data.cWidth-200+50, 50, font = "Arial 11", anchor = NW, text = data.drawSearch)
    canvas.create_text(data.cWidth-200+50, 110, font = "Arial 11", anchor = NW, text = data.drawSciSearch)
    canvas.create_text(data.cWidth-200+50, 170, font = "Arial 11", anchor = NW, text = data.comNameSearch)

    
    
    # maple = Button(data.cWidth-200+50,50,25,100,canvas, "Maple", "white")
    # birch = Button(data.cWidth-200+50,75,25,100,canvas, "Birch", "white")
    # oak = Button(data.cWidth-200+50,100,25,100,canvas, "Oak", "white")
    upload = Button(data.cWidth-200+50,265,25,100,canvas, "Upload", "white")
    data.buttons.append(searchButton)
    data.buttons.append(sciButton)
    data.buttons.append(comButton)
    data.buttons.append(stateButton)
    # data.buttons.append(maple)
    # data.buttons.append(birch)
    # data.buttons.append(oak)
    data.buttons.append(upload)
    
    canvas.create_rectangle(data.cWidth-200+25, 300, data.cWidth-25, 680, fill = "white")
    canvas.create_text(data.cWidth-200+30, 305,anchor=NW, text = "Notes:", font = "Arial 12 bold")
    canvas.create_text(data.cWidth-200+30, 315, anchor =NW, text = data.reformNotes)
    count = 0
    # print(data.listNames)
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

    def mousePressedWrapper(event, canvas, data, root):
        mousePressed(event, data, root)
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
    init(data, root)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data, root))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1250, 700)






































