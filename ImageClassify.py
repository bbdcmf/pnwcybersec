import os, warnings
import numpy as np
import PIL.Image as Image
import matplotlib.pyplot as plt
from fastai.vision.all import *
from fastai.metrics import accuracy
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

Image.MAX_IMAGE_PIXELS = 933120000 # Change the max pixels to avoid warnings

'''
src = Path to the folder containing the files you want to become images
dst = Path to folder where you want the images saved.
'''
def convertToImage(src, dst):
    files=os.listdir(src)
    print('Source:', src)
    print('Destination', dst)
    print('Converting...')
    for file in files:
        srcPath = src+file
        dstPath = dst+file+'.png'
        with open(srcPath, 'rb') as f:
            ln = os.path.getsize(srcPath)
            width = int(ln**0.5)
            imgByteArr = bytearray(f.read()) # Copy exe data to bytearray
        g = np.reshape(imgByteArr[:width * width], (width, width)) # Reshape bytearray so it is square
        g = np.uint8(g) # Ensure data is between 0 and 255, where 0=black and 1=white
        img = Image.fromarray(g)
        img.save(dstPath)
    print('Files converted successfully')
    
'''
trainPath = directory containing the train set
valid_pct = Percent of data used for validation set
bs = batch size
get_items = Function used extract the train set
get_y = Function used to classify the train set
item_tfms = Transforms to be performed on all of the data
batch_tfms = Transforms to be performed on each batch
'''
def loadData(trainPath, valid_pct, bs=None, get_items=get_image_files, get_y=parent_label, item_tfms=Resize(224, ResizeMethod.Pad, pad_mode='zeros'), batch_tfms=aug_transforms()):
    # parent_label --> simply gets the name of the folder a file is in
    loader = DataBlock(
        blocks = (ImageBlock, CategoryBlock),
        get_items = get_items,
        splitter = RandomSplitter(valid_pct=valid_pct, seed=24),
        get_y = get_y,
        item_tfms = item_tfms,
        batch_tfms= batch_tfms
    )
    dls = loader.dataloaders(trainPath, bs=bs)
    return dls

'''
dls  = Fastai DataLoaders object
arch = Architecture, e.g. resnet50
path = Path to where the trained model should be exported
epoch_ct = Number of iterations
metrics = Metrics to print while training
pretrained = Whether or not to use a pretrained model (False = Create model from scratch)
'''
def trainModel(dls, arch, path, epoch_ct=1, metrics=[error_rate, accuracy], pretrained=True):
    model = cnn_learner(dls, arch, metrics=metrics, pretrained=pretrained)
    base_lr = model.lr_find()[0]
    model.fine_tune(epochs=epoch_ct, base_lr = base_lr)
    model.dls.train = dls.train
    model.dls.valid = dls.valid
    model.export(path)
    return model 
    
'''
exportPath = Path to the exported model
cpu = Whether the model should use the CPU or GPU
'''
def loadModel(exportPath, cpu=False):
    model = load_learner(exportPath, cpu)
    return model

def getBestModel(cpu=False):
    this_dir, this_filename = os.path.split(__file__)
    modelPath = os.path.join(this_dir, 'bestModel.pkl')
    model = load_learner(modelPath, cpu)
    return model

# item = the specific image you want to show
def showImage(item):
    img = plt.imread(item)
    plt.imshow(img)
    plt.axis('off')
    plt.title(item)
    plt.show()
    
def confusionMatrix(model):
    interp = ClassificationInterpretation.from_learner(model)
    interp.plot_confusion_matrix()
    plt.show()

'''
model = The trained model
testPath = Path containing the test set of images
labeled = Whether or not the data has labels that can be extracted
pos_lbl = Label that corresponds to positive (only necessary if labeled=True)
neg_lbl = Label that corresponds to negative (only necessary if threshold not None)
threshold = Probability threshold, any prediction with a probability less than this will be flipped
'''
def predict(model, testPath, labeled=False, pos_lbl=None, neg_lbl=None, threshold=None):
    warning = ''
    path = Path(testPath)
    dirs = os.listdir(path)
    files = get_image_files(Path(testPath))
    y_test = []
    y_pred = []
    widths = []
    for item in files:
        with Image.open(item) as im:
            width, _height = im.size # Since perfect square only need 1
            widths.append(width)
        actual = parent_label(item)
        prediction, prediction_index, probabilities = model.predict(item)
        if(threshold is not None): # If the user set a threshold
            if(prediction == neg_lbl and probabilities[prediction_index] < threshold):
                prediction = pos_lbl
                warning = '| this prediction was flipped'
            elif(prediction == pos_lbl and probabilities[prediction_index] < threshold):
                prediction = neg_lbl
                warning = '| this prediction was flipped'
            else:
                warning = ''
        fmtItem = str(item).split('/')[-1].split('\\')[-1] # Get just the name of the image, ignore the path
        print(f"Item: {fmtItem.ljust(72)} | Actual: {actual.ljust(8)} | Prediction: {prediction.ljust(8)} | Probability: {probabilities[prediction_index]:.04f} {warning}")
        y_test.append(actual)
        y_pred.append(prediction)
    print(
        "-"*25,
        "\nImage Width Statistics:",
        "\nCnt:", len(widths),
        "\nMin:", min(widths),
        "\nMax:", max(widths),
        "\nAvg:", np.average(widths),
        "\nStd:", round(np.std(widths), 3),
    )
    if(labeled):
        with warnings.catch_warnings():
            warnings.simplefilter(action='ignore')
            print(
                "-"*25,
                "\nPerformance Metrics:",
                "\nAccuracy:", round(accuracy_score(y_test, y_pred), 4),
                "\nPrecision:", round(precision_score(y_test, y_pred, pos_label=pos_lbl), 4),
                "\nRecall:", round(recall_score(y_test, y_pred, pos_label=pos_lbl), 4),
                "\nF1:", round(f1_score(y_test, y_pred, pos_label=pos_lbl), 4),
                "\n"+"-"*25
            )
