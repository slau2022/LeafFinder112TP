import cv2
import numpy as np
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import tkinter as tk

## Canny Edge Algorithm
window_name = "Images"

def findOutlines(img):
    # Importantly, images are stored as BGR
    # Use the following function to read images.
    image = cv2.imread("leafdemo.jpg")
    edges = cv2.Canny(image, 200,500)
    # Error checking to make sure that our image actually loaded properly
    # Might fail if we have an invalid file name (or otherwise)
    if image is not None:
        # Display our loaded image in a window with window_name
        cv2.imshow(window_name, edges)
        # Wait for any key to be pressed
        cv2.waitKey(0)

## Isolating parts within a Green Color Range

def isolateColor():
    img = cv2.imread("leafdemo.jpg")
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    lowerGreen = np.array([0,100,0])
    upperGreen = np.array([120,255,127])
    mask = cv2.inRange(hsv, lowerGreen, upperGreen)
    res = cv2.bitwise_and(img,img,mask=mask)
    cv2.imshow("only one color", res)
    cv2.waitKey(0)


## Webscraping Leaf Types Information

leafData = "https://gardenerdy.com/different-kinds-of-leaves"

website = requests.get(leafData)
source = website.text
parser = BeautifulSoup(source,'html.parser')

leafNames = []
leafDescrip = []
leafDict = {}

#finds all the types of leaves and adds their names to a list
count = 0
for leafDes in parser.find_all("span"):
    leafDes = leafDes.text
   
    wordcount = 0
    for word in leafDes.split(" "):
        wordcount +=1

    if ("leaf" in leafDes or "leaves" in leafDes or "Leaf" in leafDes or "Leaves" in leafDes) and wordcount <=4 and "Types" not in leafDes and leafDes[0].isupper() and wordcount >1:
        leafNames.append(leafDes)

#finds all the descriptions of the leaves and adds the description to the list
descrip = ""
for i in range(len(parser.find_all("span"))):
    
    if i != 17 and i>8 and i<33 and parser.find_all("span")[i].text not in leafNames:
        descrip += parser.find_all("span")[i].text
        
    if parser.find_all("span")[i].text in leafNames :
        leafDescrip.append(descrip)
        descrip = ""

leafDescrip.append(descrip)

#makes sure to get rid of any empty items
for i in range(len(leafDescrip)-1,-1,-1):
    if leafDescrip[i] == "":
        leafDescrip.pop(i)
    
#correlate each description to name
for i in range(len(leafNames)):
    leafDict[leafNames[i]] = leafDescrip[i]
    

links = []
#find all of the image links
for i in range(len(parser.find_all("img"))):
    if "https:" in parser.find_all("img")[i]["src"] and i>2 and i<12:
        links.append(parser.find_all("img")[i]["src"])
        

#add the links to the leaf dictionary
i = 0
for key in leafDict:
    desc = leafDict[key]
    leafDict[key] = [desc, links[i]]
    i+=1
    
## Database of Trees Webscraping

#creating reference tree database
#just trees in northeast region

leafDataNorthEast = "http://leafsnap.com/species/"

website = requests.get(leafDataNorthEast)
source = website.text
parser = BeautifulSoup(source,'html.parser')

northEastLeaves = []

#getting a database of leaves
for leafName in parser.find_all(class_="popnameTd"):
    if leafName.text.strip() not in northEastLeaves:
        northEastLeaves.append(leafName.text.strip())
    

#create a list of all of the links
northEastLeavesimg = []
i = 0
for link in parser.find_all(class_= "speciesImg"):
    northEastLeavesimg.append(link["src"])
    i += 1
    if i >659:
        break
    
#create a list of all of the scinames
leafSciNames = []
for leafSciName in parser.find_all(class_="scinameTd"):
    leafSciNames.append(leafSciName.text.strip())
    
#map each tree name to image link of only the leaf and scientific name
totalLeafDict = {}
for i in range(len(northEastLeaves)):
    totalLeafDict[northEastLeaves[i]] = [leafSciNames[i], northEastLeavesimg[i*3]]
    

#enter family name into this function and it will return a dictionary of the
#trees mapped to its leaf picture link
def findTreeImages(family, dict = totalLeafDict):
    answer = {}
    for tree in dict:
        if family in tree:
            answer[tree] = dict[tree]
        
    return answer
    

## Countouring parts within a Green Color Range
# Trying to outline because there's a cv compare contours function 
#
# def greenOutline(rlow,rhigh,glow,ghigh,blow,bhigh):
#     img = cv2.imread('leafdemo.jpg', 1)
#     
#     r = (rlow, rhigh)
#     g = (glow, ghigh)
#     b = (blow, bhigh)
#     img_rgb_threshold = cv2.inRange(img, 
#         (r[0], g[0], b[0]),
#         (r[1], g[1], b[1])
#     )
#     
#     mode = cv2.RETR_EXTERNAL
#     method = cv2.CHAIN_APPROX_SIMPLE
#     
#     im2, contours, hierarchy = cv2.findContours(img_rgb_threshold, mode=mode, method=method)
#     
#     min_area = 100.0
#     max_area = 40000.0
#     min_perimeter = 0.0
#     min_width = 10.0
#     max_width = 5000.0
#     min_height = 10.0
#     max_height = 5000.0
#     
#     output_contours = []
#     for contour in contours:
#         x,y,w,h = cv2.boundingRect(contour)
#         if (w < min_width or w > max_width):
#             continue
#         if (h < min_height or h > max_height):
#             continue
#         area = cv2.contourArea(contour)
#         if (area < min_area or area > max_area):
#             continue
#         if (cv2.arcLength(contour, True) < min_perimeter):
#             continue
#         output_contours.append(contour)
#         
#     img_drawn = cv2.drawContours(img, output_contours, -1, (255.0, 0.0, 0.0), 2)
#     cv2.imshow('img_drawn', img_drawn)
#     cv2.namedWindow("img_drawn", cv2.WINDOW_NORMAL)
#     cv2.resizeWindow("img_drawn", 250,375 )
#     cv2.waitKey(0)
# 
# greenOutline(0,225,0,200,0,225)
