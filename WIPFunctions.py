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

1: fix trim matching (..no idea)
2. Upload images feature ~~~  (DONE-ish)
3: Find "lobes" of lobed leaves  (can try contour hull or find corners compared to a pentagon or something)
4: isolate leaf from a non white background (Can ignore until next week)

"""

## Isolates leaf from background that is not white
# """Syntax for how to threshold: https://docs.opencv.org/3.4/d7/d4d/tutorial_py_thresholding.html"""
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
    cv2.imshow("when you try your best", th3)
    cv2.waitKey(0)
    # can = cv2.Canny(th3, 300, 600)

    
    im2, contours, hierarchy = cv2.findContours(th3, 2,1)
    # cv2.drawContours(im2,contours,-1,(128,255,0),3)
    # cv2.imshow("when you try your best", im2)
    # cv2.waitKey(0)
   
    # print(contours)
    return contours


def backgroundElim(frame):
    # """Syntax for using MOG2: https://docs.opencv.org/3.4/db/d5c/tutorial_py_bg_subtraction.html"""
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
    # cv2.imshow("blur", res)
    # cv2.waitKey(0)

# backgroundElim("leafbg.jpg")

    # bgModel = cv2.BackgroundSubtractorMOG2(0, bgSubThreshold)
    # fgmask = bgModel.apply(leaf)
    # res = cv2.bitwise_and(leaf, leaf, mask=fgmask)
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # blur = cv2.GaussianBlur(gray, (blurValue, blurValue), 0)
    # ret, thresh = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)


#[NOT WORKING] 
#To find contours from a nonwhite background
def greenOutline(rlow,rhigh,glow,ghigh,blow,bhigh):
    # """Template from GitHub Autonomous Garden: https://github.com/CodingEZ/Automated-Garden """
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


## Identify major shape of a leaf    
def compareOutlines(leaf1, leaf2):
    # """Syntax how to use cv2.matchshapes(): https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_contours/py_contours_more_functions/py_contours_more_functions.html"""

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
    # print(ret) 
    # cv2.drawContours(img, cont, -1, (255,0,255), 3)
    # cv2.drawContours(img2, cont2, -1, (255,0,255), 3)
    # print(ret, retsame)
    # cv2.imshow("oy", img)
    # cv2.waitKey(0)
    # cv2.imshow("oy", img2)
    # cv2.waitKey(0)
    
    return ret

def analyzeLeaf(leaf):
#best value algorithm
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
        
# print(analyzeLeaf("oak2.jpg"))

# ph = cv2.imread("leaftrial.jpg")
# ph = cv2.cvtColor(ph, cv2.COLOR_BGR2GRAY)
# edges = cv2.Canny(ph, 100,900)
# cv2.imshow("test", edges)
# print(edges)
# cv2.waitKey(0)
    #see if shape is fanned, sinuate, lobed, heartshaped, ovoid, triangular, rounded or lanceolate

#https://www.pyimagesearch.com/2014/04/07/building-pokedex-python-indexing-sprites-using-shape-descriptors-step-3-6/

## Trying to find "lobes"
    # """Syntax on how to find corners: #https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_features_harris/py_features_harris.html"""
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
    print(dst, len(dst))
    # Threshold for an optimal value, it may vary depending on the image.
    img[dst>.4*dst.max()]=[255]
    
    cv2.imshow('dst',img)
    cv2.waitKey(0)
    # if cv2.waitKey(0) & 0xff == 27:
    #     cv2.destroyAllWindows()


# detectCorners("leaftrial.jpg")
# """Syntax on how to use countour hull: https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_contours/py_contours_more_functions/py_contours_more_functions.html"""
def detectLobes(leaf):
    img = cv2.imread(leaf)
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img_gray, 127, 255, 0)
    img2, contours,hierarchy = cv2.findContours(thresh,2,1)
    print(len(contours))
    cnt = contours[0]
    
    hull = cv2.convexHull(cnt,returnPoints = False)
    defects = cv2.convexityDefects(cnt,hull)
    
    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0]
        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])
        cv2.line(img,start,end,[0,255,0],2)
        cv2.circle(img,far,5,[0,0,255],-1)
    
    cv2.imshow('img',img)
    cv2.waitKey(0)

# detectLobes("leaftrial.jpg")

## Isolating parts within a Green Color Range
#colors are different between thresholding a color between a range
def convertHSV(rgb):
    rP = rgb[0]/255
    gP = rgb[1]/225
    bP = rgb[2]/225
    cmax = max((rP,gP,bP))
    cmin = min((rP,gP,bP))
    V = Cmax
    cD = cmax-cmin
    if cD == 0:
        H = 0
    elif cmax == rP:
        H = 60 * (((gP-bP)/cD)%6)
    elif cmax == gP:
        H = 60 * (((bP-rP)/cD)+2)
    elif cmax == bP:
        H = 60 * (((rP-gP)/cD)+4)
    
    if cmax == 0:
        S = 0
    else:
        S = cD/cmax
    
    V = V/100*255
    S = S/100*255
    
    return (H,S,V)


def isolateColor(lower, upper):
# """How to use inrange to isolate color: https://www.geeksforgeeks.org/detection-specific-colorblue-using-opencv-python/"""
    #isolates colors in range, upper is rgb
    img = cv2.imread("leafdemo.jpg")
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    lowerGreen = np.array(lower) #[0,100,0]
    upperGreen = np.array(upper) #placeholder range [120,255,127]
    mask = cv2.inRange(hsv, lowerGreen, upperGreen)
    res = cv2.bitwise_and(img,img,mask=mask)
    cv2.imshow("only one color", res)
    cv2.waitKey(0)


## Find Most Common Color
# """How to analyze pixel colors of an image from: https://code.likeagirl.io/finding-dominant-colour-on-an-image-b4e075f98097"""

def find_histogram(clt):
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    hist = hist.astype("float")
    hist /= hist.sum()

    return hist
    
def findColor(hist, centroids):
    maxPerc = None
    comCol = None
    for (percent, color) in zip(hist, centroids):
        if maxPerc == None:
            maxPerc = percent
            comCol = color
        elif percent > maxPerc:
            maxPerc = percent
            comCol = color
    
    maxPerc2 = None
    comCol2 = comCol  
    for (percent, color) in zip(hist, centroids):
        if comCol2.all() == comCol.all() and color.astype("uint8").tolist() != comCol.astype("uint8").tolist():
            maxPerc2 = percent
            comCol2 = color
        elif color.astype("uint8").tolist() != comCol.astype("uint8").tolist() and percent > maxPerc2:
            maxPerc2 = percent
            comCol2 = color
        
    color = comCol2.astype("uint8").tolist()
    return color

def detectColor(leaf):
    img = cv2.imread(leaf)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    img = img.reshape((img.shape[0] * img.shape[1],3)) #represent as row*column,channel number
    clt = KMeans(n_clusters=4) #cluster number
    clt.fit(img)
    
    hist = find_histogram(clt)
    col = tuple(findColor(hist, clt.cluster_centers_))
    return str(col)+ " is the most common color in this leaf."

# print(detectColor("leafdemo.jpg"))
