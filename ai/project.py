#import pnwcybersec.ImageClassify as ic
import ImageClassify as ic
import pathlib, os, torch, gc
import matplotlib.pyplot as plt
from fastai.vision.models import resnet50
from fastai.metrics import error_rate, accuracy
from fastai.vision.all import *

gc.collect() # Garbage collection
torch.cuda.empty_cache() # Empty PyTorch cache

#####***Uncomment these if running on Windows***#####
#temp = pathlib.PosixPath
#pathlib.PosixPath = pathlib.WindowsPath
#####################################################

isRyan = False

if isRyan:
    path = '/run/media/bbdcmf/T7/ITS490-Project/' # Path to the project folder
    exportPath = path+'github/ai/models/3-21-22-resnet50-train2-pretrained-epoch_50-bs-32-98.21%.pkl' # If training, this is the path to where your model will be exported. If loading a trained model, this is the path to that model.
else: # if Joey
    path = './'
    exportPath = path+'ai/models/3-21-22-resnet50-train2-pretrained-epoch_50-bs-32-98.21%.pkl'
#####################################***Training a new model***#####################################
#
#trainPath = '/home/bbdcmf/Downloads/archive(1)/images/train/'
#dls = ic.loadData(trainPath, valid_pct=0.2, bs=32, get_y=parent_label)
#dls.valid.show_batch(max_n=8, nrows=2)
#plt.show()
#model = ic.trainModel(dls, resnet50, path=exportPath, epoch_ct=10, metrics=[error_rate, accuracy], pretrained=True)
#ic.confusionMatrix(isModel=True, model=model)
#
####################################################################################################

##################################***Loading a Trained Model***##################################
#
model = ic.loadModel(exportPath, cpu=False)
#
#model = ic.getBestModel(cpu=False)
#
#################################################################################################

'''
If using default options, your file struction should look like this:
path/to/dataset/:
				path/to/dataset/label1/:
										path/to/dataset/label1/label1file1
										path/to/dataset/label1/label1file2 ...
				path/to/dataset/label2:
										path/to/dataset/label2label2file1
										path/to/dataset/label2label2file2 ...
				...
'''
answered = False
while not answered:
    should_convert = input("Does your test set need to be converted to images?[y/n] ")
    if should_convert.lower() == 'y':
        # If the files have not been converted to images yet
        srcPath = input("Enter the folder containing the files that will be converted:\n")
        isDir1 = os.path.isdir(srcPath)
        if(isDir1):
            dstPath = input("Enter the folder you'd like the image(s) to be saved to:\n")
            isDir2 = os.path.isdir(dstPath)
            if(isDir2):
                ic.convertToImage(srcPath, dstPath)
                answered = True
            else:
                print("Error: Directory not found, please try again")
        else:
            print("Error: Directory not found, please try again")
    elif should_convert.lower() == 'n':
        # If the files are already images
        dstPath = input("Enter the folder containing the images you'd like to predict:\n")
        isDir3 = os.path.isdir(dstPath)
        if(not isDir3):
            print("Error: Directory not found, please try again")
        answered = isDir3
    else:
        print("Error, you must enter either y or n")

ic.predict(model, dstPath, labeled=True, pos_lbl='malware', neg_lbl='goodware')
