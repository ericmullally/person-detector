import cv2
import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
from moviepy.editor import *

def resizeMovie(filePath):
    """Parameters:
            filePath: string -> Path to clip 
    Resizes and writes files to the appropriate folder before viewing.
    """
    name = filePath.split("\\")[-1].split(".")[0] # filter out the name from the path
    extension = filePath.split("\\")[-1].split(".")[-1] # filter out the extension from the path
    try:
        clip1 = VideoFileClip(filePath)
        clip2 = clip1.resize(0.5)
    except Exception as ex: 
        print(ex)
        raise ex.with_traceback()

    newPath = "Subject\\" + name + "." + extension
    clip2.write_videofile(newPath) # Subject is a temp folder all videos should be deleted after use
  
    return newPath

def resizeImg(folderPath, imageNames:list, training:bool):
    """
        Resizes any images larger than 500x600. and saves them to the appropriate directory.
        Parameters:
            imgPath: string.
            training: bool. 
    """
    for img in imageNames:
        newPath = f"training/{img}" if training else f"test/{img}"
        image=cv2.imread( folderPath + "\\" + img , cv2.IMREAD_UNCHANGED)
        scale_percent = 50 # percent of original size
        width = image.shape[1]
        height = image.shape[0]
            
        if width > 600 or height > 500:
            newWidth = int(image.shape[1] * scale_percent / 100)
            newHeight = int(image.shape[0] * scale_percent / 100)
            dim = (newWidth, newHeight)
            newImg = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
            cv2.imwrite(newPath  , newImg)
        else: 
            cv2.imwrite(newPath  , image)
           
def xmlToCsv(folderPath, training:bool):
    """
     converts all xml in the givien directory to csv.
     Parameters: 
        folderPath: path to xml files you wish to convert.
        training: bool. is this the training set.
    """
    xmlList = []
    for xmlFile in glob.glob(folderPath + '/*.xml'):
        tree = ET.parse(xmlFile)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xmlList.append(value)
        os.remove(xmlFile)
            
    columnNames = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xmlDf = pd.DataFrame(xmlList, columns=columnNames)
    fileName = 'data/train.csv' if training else "data/test.csv"
    xmlDf.to_csv(fileName, index=None)

def removeUnusedImages():
    testXmlList = [file.split("\\")[1] for file in glob.glob("test\*xml")]
    trainXmlList = [file.split("\\")[1] for file in glob.glob("training\*xml")]
    
    for file in glob.glob("test\*jpg"):
        imageName = file.split("\\")[1].split(".")[0] + ".xml"
        if not imageName in testXmlList:
            os.remove(file)
    
    for file in glob.glob("training\*jpg"):
        imageName = file.split("\\")[1].split(".")[0] + ".xml"
        if not imageName in trainXmlList:
            os.remove(file)
