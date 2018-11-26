from tkinter import *
from image_util import *
import requests
from urllib import *
from PIL import Image, ImageTk
from io import BytesIO
import cv2
import numpy as np
import os
from sklearn.cluster import KMeans


"""
Things to do:

1: fix trim matching
2. Upload images feature ~~~
3: Find "lobes" of lobed leaves 
4: isolate leaf from a non white background

"""

## Isolates leaf from background that is not white
#returns contours of a leaf with white background
def betterIsolation(leaf):
    #returns contours of the leaf
    ph = cv2.imread(leaf)

    ph = cv2.resize(ph, (300,500))
    ph = cv2.fastNlMeansDenoising(ph)
    
    ph = cv2.cvtColor(ph, cv2.COLOR_BGR2GRAY)
    
    
    th3 = cv2.bitwise_not(ph) #isolate just the leaf

    ret, th3 = cv2.threshold(th3,15,255,cv2.THRESH_BINARY)#get rid of innards of leaf

    # th3 = cv2.adaptiveThreshold(th3,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                # cv2.THRESH_BINARY,11,2) #get outline of leaf
    # cv2.imshow("when you try your best", th3)
    # cv2.waitKey(0)
    # can = cv2.Canny(th3, 300, 600)

    
    im2, contours, hierarchy = cv2.findContours(th3, 2,1)
    cv2.drawContours(im2,contours,-1,(128,255,0),3)
    cv2.imshow("when you try your best", im2)
    cv2.waitKey(0)
   
    # print(contours)
    return contours


def backgroundElim(frame):
    bgSubThreshold = 50
    blurValue = 41
    threshold = 60
    img = cv2.imread(frame)
    frame = cv2.imread(frame)
    bgModel = cv2.createBackgroundSubtractorMOG2(0, bgSubThreshold)
    fgmask = bgModel.apply(frame)
    res = cv2.bitwise_and(frame, frame, mask=fgmask)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # blur = cv2.GaussianBlur(gray, (blurValue, blurValue), 0)
    ret, thresh = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    cv2.imshow("blur", res)
    cv2.waitKey(0)
    
    
# 
# backgroundElim("leafbg.jpg")

    # bgModel = cv2.BackgroundSubtractorMOG2(0, bgSubThreshold)
    # fgmask = bgModel.apply(leaf)
    # res = cv2.bitwise_and(leaf, leaf, mask=fgmask)
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # blur = cv2.GaussianBlur(gray, (blurValue, blurValue), 0)
    # ret, thresh = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)


## Identify major shape of a leaf    
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
        print(closeValue)
        if winValue == None:
            winValue = closeValue
            winLeaf = feuille
        elif closeValue<winValue:
            winValue = closeValue
            winLeaf = feuille
    
    return winLeaf
        
# print(analyzeLeaf("leaftrial.jpg"))

# ph = cv2.imread("leaftrial.jpg")
# ph = cv2.cvtColor(ph, cv2.COLOR_BGR2GRAY)
# edges = cv2.Canny(ph, 100,900)
# cv2.imshow("test", edges)
# print(edges)
# cv2.waitKey(0)
    #see if shape is fanned, sinuate, lobed, heartshaped, ovoid, triangular, rounded or lanceolate

#https://www.pyimagesearch.com/2014/04/07/building-pokedex-python-indexing-sprites-using-shape-descriptors-step-3-6/

## Trying to find "lobes"
#https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_features_harris/py_features_harris.html
def detectCorners(leaf):
    filename = leaf
    
    img = cv2.imread(filename)
    img = cv2.bitwise_not(img)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, gray = cv2.threshold(gray,15,255,cv2.THRESH_BINARY)

    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray,2,3,0.04)
    
    #result is dilated for marking the corners, not important
    dst = cv2.dilate(dst,None)
    
    # Threshold for an optimal value, it may vary depending on the image.
    img[dst>.4*dst.max()]=[255]
    
    cv2.imshow('dst',img)
    cv2.waitKey(0)
    # if cv2.waitKey(0) & 0xff == 27:
    #     cv2.destroyAllWindows()

#https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_contours/py_contours_more_functions/py_contours_more_functions.html
#detectCorners("leaftrial.jpg")

def detectLobes(leaf):
    pass


## Countouring 
#[NOT WORKING] 
#Template from GitHub Autonomous Garden 
#Function to find contours because there's a cv compare contours function 
#
def greenOutline(rlow,rhigh,glow,ghigh,blow,bhigh):
    img = cv2.imread('leafdemo.jpg', 1)
    
    r = (rlow, rhigh)
    g = (glow, ghigh)
    b = (blow, bhigh)
    img_rgb_threshold = cv2.inRange(img, 
        (r[0], g[0], b[0]),
        (r[1], g[1], b[1])
    )
    
    mode = cv2.RETR_EXTERNAL
    method = cv2.CHAIN_APPROX_SIMPLE
    
    im2, contours, hierarchy = cv2.findContours(img_rgb_threshold, mode=mode, method=method)
    
    min_area = 100.0
    max_area = 40000.0
    min_perimeter = 0.0
    min_width = 10.0
    max_width = 5000.0
    min_height = 10.0
    max_height = 5000.0
    
    output_contours = []
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        if (w < min_width or w > max_width):
            continue
        if (h < min_height or h > max_height):
            continue
        area = cv2.contourArea(contour)
        if (area < min_area or area > max_area):
            continue
        if (cv2.arcLength(contour, True) < min_perimeter):
            continue
        output_contours.append(contour)
        
    img_drawn = cv2.drawContours(img, output_contours, -1, (255.0, 0.0, 0.0), 2)
    cv2.imshow('img_drawn', img_drawn)
    cv2.namedWindow("img_drawn", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("img_drawn", 250,375 )
    cv2.waitKey(0)

# greenOutline(0,225,0,200,0,225)

"""
Things to do:
1. Create a database of references (3 each) for each shape category
2. Sort larger database into smaller groups
3. figure out how to interface
"""