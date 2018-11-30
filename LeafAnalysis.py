import cv2
import numpy as np
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from tkinter import *
import os
from sklearn.cluster import KMeans
from urllib import *

## Webscraping Leaf Types Information
# """How to webscrape by class:https://codeburst.io/web-scraping-101-with-python-beautiful-soup-bb617be1f486"""

#Getting the database for types of leaves
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
#getting database of tree species
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

## Trees by State
stateDict = {}
for leaf in totalLeafDict:
    sciname = totalLeafDict[leaf][0]
    g = None
    s = None
    for word in sciname.split(" "):
        if g == None:
            g = word
        else:
            s = word
        
    leafurl = "http://leafsnap.com/species/"+g+"%20"+s+"/"
    website = requests.get(leafurl)
    source = website.text
    parser = BeautifulSoup(source,'html.parser')
    leafDescrip = ""
    states = ""
    count = 1
    for descrip in parser.find_all("div"):
        if "Presence in US" in descrip.text:
            states = descrip.text
    
    states = states.replace("Presence in US:","")
    states = states.strip()
    for state in states.split(" "):
        if "," in state:
            state = state[:len(state)-1]
        if state not in stateDict:
            stateDict[state] = [leaf]
        else:
            stateDict[state].append(leaf)

stateDict["IN"] = stateDict["INKS"]
stateDict["KS"] = stateDict["INKS"]
stateDict["PA"] = stateDict["PE"]
stateDict["AL"].append(stateDict["Al"][0])

del stateDict["Not"]
del stateDict["native"]
del stateDict["to"]
del stateDict["the"]
del stateDict["US"]
del stateDict["but"]
del stateDict["widely"]
del stateDict["cultivated."]
del stateDict[""]
del stateDict["PE"]
del stateDict["Al"]
del stateDict["INKS"]

            
    
##Find a leaf's description
def leafDescrip(leaf, dict = totalLeafDict):
    sciname = dict[leaf][0]
    g = None
    s = None
    for word in sciname.split(" "):
        if g == None:
            g = word
        else:
            s = word
        
    leafurl = "http://leafsnap.com/species/"+g+"%20"+s+"/"
    print(leafurl)
    website = requests.get(leafurl)
    source = website.text
    parser = BeautifulSoup(source,'html.parser')
    leafDescrip = ""
    for descrip in parser.find_all(class_="description"):
        leafDescrip += descrip.text.strip()
        
    return leafDescrip

## Get Trees in a Family
#enter family name into this function and it will return a dictionary of the
#trees mapped to its leaf picture link
def findTreeImages(family, dict = totalLeafDict):
    answer = {}
    for tree in dict:
        if family.lower() in tree.lower():
            answer[tree] = dict[tree]
    if len(answer) == 0:
        return "No tree found"
    else:
        return answer

def findTreeSci(sciname, dict = totalLeafDict):
    answer = {}
    for tree in dict:
        if sciname.lower() in dict[tree][0].lower():
            answer[tree] = dict[tree]
    if len(answer) == 0:
        return "No tree found"
    else:
        return answer

def findSpecies(comName, dict = totalLeafDict):
    answer = {}
    for tree in dict:
        if comName.lower() == tree.lower():
            answer[tree] = dict[tree]
    if len(answer) == 0:
        return "No tree found"
    else:
        return answer

## Get trees by state
def findTreeState(state, dict = stateDict, dict2 = totalLeafDict):
    answer = {}
    state = state.upper()
    if state in dict:
        trees = dict[state]
        for tree in trees:
            answer[tree] = dict2[tree]
        return answer
    else:
        return "No tree found"

## Fetch Generic Outline [NEEDS WORK]
#function will return image of just outlines of an image
def findOutLines(img):
    window_name = "Images"
    image = cv2.imread("leafdemo.jpg") #leafdemo is placeholder
    edges = cv2.Canny(image, 200,500)
    # Error checking to make sure that our image actually loaded properly
    if image is not None:
        # Display our loaded image in a window with window_name
        cv2.imshow(window_name, edges)
        # Wait for any key to be pressed
        cv2.waitKey(0)
    return edges

