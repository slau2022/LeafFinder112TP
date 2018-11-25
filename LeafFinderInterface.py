from tkinter import *
from image_util import *
import requests
from urllib import *
from PIL import Image, ImageTk
from io import BytesIO

#color = 6ee22f

root = Tk()
class main(Frame):
    def __init__(self, master):
        self.master = master
        # self.display = Frame(master, height = 50, width = 1250, bg = "#6ee22f", bd = 5, relief = RIDGE, highlightbackground = "black")
        # self.display.place(x = 0, y = 0)
        # 
        
        
        # self.search = Frame(master, height = 950, width = 1000, bg = "blue" )
        # self.search.place(x=0, y = 50)
        
        displayCanvas = Canvas(self.master, width = 500, height = 500)
        displayCanvas.place(x=50,y=50)
        
        url = "http://api.leafsnap.com/v1/static/cache/leafdb/images/findingspecies/fagus_grandifolia/LTV-RBD-00221.jpg__crop-4_86_1067_1148_w-400_h-400.jpg"
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img = ImageTk.PhotoImage(img)


        displayCanvas.create_image(0,0, anchor = NW, image = img)
        
        
    
app = main(root)

root.mainloop()