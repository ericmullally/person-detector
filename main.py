import os
import argparse
import sys
from showWindow import MainWindow
from train import Train


from PyQt5.QtWidgets import *

PROGRAMS = ["demo", "train"]

class Main():
    def __init__(self, args):
        if args.program == "demo":
            app = QApplication(sys.argv)
            root = MainWindow(args.filePath if not args.defaultVideo else args.defaultVideo)
            root.show()
            sys.exit(app.exec())
        else:
           trianer =  Train(args.folderPath, args.trainSize)
           




if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument("program", choices=PROGRAMS, help= "Enter the program you wish to start.\n" )
    # demo arguments
    parse.add_argument("--filePath", help="Enter the path to the file you wish to view. You should use quotes around your paths especially if they have spaces in them.\n")
    parse.add_argument("-p" , action = "store_true", dest="defaultVideo", help="If you wish to see an example but do not have a video use this flag.\n")
    # train arguments
    parse.add_argument("--folderPath", help="Pass the folder of images you want to use for training.")
    parse.add_argument("--trainSize", type=int,  help="Provide the percent of the images you wish to be used for training int only no % needed. The test percent is implicit.")
    

    parsed_args = parse.parse_args()

    if parsed_args.program == "demo":
        if not parsed_args.defaultVideo and (not os.path.isfile(parsed_args.filePath) or not os.path.exists(parsed_args.filePath)):
            parse.error(f"Could not find this directory. {parsed_args.filePath}")
        elif parsed_args.filePath == None and parsed_args.defaultVideo == False:
            parse.error("Demo requires --filePath or you may use -p to see the provided video.")
    else:
        if parsed_args.folderPath == None:
            parse.error("You must provide the path to the folder of images you want to use.")
        elif parsed_args.trainSize == None :
            parse.error("You must provide a size for your trianing set. This number will be a percentage of the images provided.")
      
       
    main = Main(parsed_args)


"""
to train give the folder path to the images you want to use and the split you would like.
"""