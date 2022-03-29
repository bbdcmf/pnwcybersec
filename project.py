#import pnwcybersec.ImageClassify as ic
import ImageClassify as ic
import pathlib, os
import matplotlib.pyplot as plt
from fastai.vision.models import resnet50
from fastai.metrics import error_rate, accuracy
from fastai.vision.all import *

#####***For running on a Windows Machine***#####
#temp = pathlib.PosixPath
#pathlib.PosixPath = pathlib.WindowsPath
#################################################

path = '/run/media/bbdcmf/T7/ITS490-Project/' # Path to the project folder
#path = 'E:/ITS490-Project/'
exportPath = path+'github/3-21-22-resnet50-train2-pretrained-epoch_50-bs-32-98.21%.pkl' # Path to our exported model/where we will export the model
trainPath = path+'dataset/train2/'

#####################################***Training a new model***#####################################
#
#dls = ic.loadData(trainPath, valid_pct=0.2, bs=32)
#dls.valid.show_batch(max_n=8, nrows=2)
#plt.show()
#model = ic.trainModel(dls, resnet50, path=exportPath, epoch_ct=1, metrics=[error_rate, accuracy], pretrained=True)
#ic.confusionMatrix(model)
#
####################################################################################################

##################################***Loading a PreTrained Model***##################################
#
model = ic.loadModel(exportPath, cpu=True)
#model = ic.getBestModel(cpu=False)
#
####################################################################################################
def isDir(path):
    if(not os.path.isdir(path)):
        print("Error: Directory not found, please try again")
        return False
    else:
        return True
answered = False
while answered == False:
    should_convert = input("Does your test set need to be converted to images?[y/n] ")
    if should_convert.lower() == 'y':
        # If the files have not been converted to images yet
        srcPath = input("Enter the folder containing the files that will be converted:\n")
        isDir1 = isDir(srcPath)
        if(isDir1):
            dstPath = input("Enter the folder you'd like the image(s) to be saved to:\n")
            isDir2 = isDir(dstPath)
            if(isDir2):
                ic.convertToImage(srcPath, dstPath)
                answered = True
                
    elif should_convert.lower() == 'n':
        # If the files are already images
        dstPath = input("Enter the folder containing the images you'd like to predict:\n")
        answered = isDir(dstPath)
    else:
        print("Error, you must enter either y or n")

ic.predict(model, dstPath, labeled=True)
