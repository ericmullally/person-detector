import os
import sys
import tensorflow 
from dataCleaner import resizeImg, xmlToCsv, removeUnusedImages

class Train():
    def __init__(self, folderpath, trainSize):
        self.folderPath = folderpath
        self.testSize =  int(len(os.listdir(folderpath)) * (100 - (int(trainSize)) / 100))
        self.trainSize =  int(len(os.listdir(folderpath)) *  int(trainSize) / 100)
        self.split()
        self.startLabelImg()
        
      
    def startLabelImg(self):
        """
            Opens the labelImg tool to assit in data labeling.
            Be sure to select the images from the directory in this project as resize has placed them in training and test respectivly.
            and save the xml in the same folder.
            Note for helpful hints like selecting default save loaction use the help bar to see the tutorials.
        """
        os.system(f"labelImg = labelImg.labelImg:main")
        os.system(f"labelImg = labelImg.labelImg:main")
        removeUnusedImages()

        xmlToCsv("training", True)
        xmlToCsv("test", False)


    def split(self):
        # split the images into training and test
        # need list of each strings only
        train = os.listdir(self.folderPath)[:self.trainSize]
        test = os.listdir(self.folderPath)[self.trainSize:]
        resizeImg(self.folderPath, train, True )
        resizeImg(self.folderPath, test, False )
        

