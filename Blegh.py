from tkinter import *
from image_util import *
import requests
from urllib import *
from PIL import Image, ImageTk
from io import BytesIO
import cv2
import numpy as np
import os

def validContours(edges):
    for line in edges:
        for point in line:
            if point !=0:
                return True
    return False
    
def betterIsolation(leaf):
    #returns contours of the leaf
    ph = cv2.imread(leaf)
    ph = cv2.resize(ph, (300,500))
    ph = cv2.cvtColor(ph, cv2.COLOR_BGR2GRAY)

    th3 = cv2.bitwise_not(ph) #isolate just the leaf

    ret, th3 = cv2.threshold(th3,15,255,cv2.THRESH_BINARY)#get rid of innards of leaf

    can = cv2.Canny(th3, 300, 600)
    

   #   th3 = cv2.adaptiveThreshold(th3,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
    #             cv2.THRESH_BINARY,11,2) #get outline of leaf
    
    im2, contours, hierarchy = cv2.findContours(can, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.imshow("when you try your best", can)
    cv2.waitKey(0)
   
    print(contours)
    return contours
    
def compareOutlines(leaf1, leaf2):
    
    # ph = cv2.imread(leaf1) #leaf1
    # ph2 = cv2.imread(leaf2) #leaf2
    # ph = cv2.resize(ph, (300, 500))
    # ph2 = cv2.resize(ph2, (300,500))
    #  
    # 
    # ph = cv2.cvtColor(ph, cv2.COLOR_BGR2GRAY)
    # ph2 = cv2.cvtColor(ph2, cv2.COLOR_BGR2GRAY)
    # 
    # edges = cv2.Canny(ph, 300,600)
    # edges2 = cv2.Canny(ph2, 300,600)

   ##   
    # modify = 0
    # 
    # while not validContours(edges2):
    #     edges2 = cv2.Canny(ph2, 100,1000-100*modify)
    #     modify +=1
    # 
    # img, cont, hierarchy = cv2.findContours(edges,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # img2, cont2, hierarchy2 = cv2.findContours(edges2,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # 
    # cv2.imshow("base", img)
    # cv2.waitKey(0)
    # cv2.imshow("compare", img2)
    # cv2.waitKey(0)
    
    cont = betterIsolation(leaf1)
    cont2 = betterIsolation(leaf2)
    
    ret = cv2.matchShapes(cont[0],cont2[0],1,0.0)
    print(ret)
    # cv2.drawContours(img, cont, -1, (255,0,255), 3)
    # cv2.drawContours(img2, cont2, -1, (255,0,255), 3)
    # print(ret, retsame)
    # cv2.imshow("oy", img)
    # cv2.waitKey(0)
    # cv2.imshow("oy", img2)
    # cv2.waitKey(0)
    
    return ret

def analyzeLeaf(leaf):
    leaftypes = ["Fanned","Sinuate", "Lobed", "Heartshaped", "Ovoid", "Triangular","Rounded","Lanceolate"]
    winValue = None
    winLeaf = None
    for feuille in leaftypes:
        similar = feuille
        closeValue = 0
        for num in range(1,4):
            other = "LeafShapescopy/"+feuille+"/"+feuille+str(num)+".jpg"
            print(other)
            closeValue += compareOutlines(leaf, other )
        closeValue = closeValue/3 #averages the values for each type
        if winValue == None:
            winValue = closeValue
            winLeaf = feuille
        elif closeValue<winValue:
            winValue = closeValue
            winLeaf = feuille
    
    return winLeaf
        
print(analyzeLeaf("leaftrial2.jpg"))

# ph = cv2.imread("leaftrial.jpg")
# ph = cv2.cvtColor(ph, cv2.COLOR_BGR2GRAY)
# edges = cv2.Canny(ph, 100,900)
# cv2.imshow("test", edges)
# print(edges)
# cv2.waitKey(0)
    #see if shape is fanned, sinuate, lobed, heartshaped, ovoid, triangular, rounded or lanceolate

#https://www.pyimagesearch.com/2014/04/07/building-pokedex-python-indexing-sprites-using-shape-descriptors-step-3-6/





def countLobes(leaf):
    pass

def detectTrim(leaf):
    pass

def detectColor(leaf):
    pass

def detectComposite(leaf):
    pass

"""
Things to do:
1. Create a database of references (3 each) for each shape category
2. Sort larger database into smaller groups
3. figure out how to interface
"""