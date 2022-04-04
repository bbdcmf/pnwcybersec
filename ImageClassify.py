from fastai.vision.all import *
from fastai.metrics import accuracy
import numpy as np
import os
import PIL.Image as Image
import matplotlib.pyplot as plt

Image.MAX_IMAGE_PIXELS = 933120000 # Change the max pixels to avoid warnings

# src = Path to the folder containing the files you want to become images. dst = Path to folder where you want the images saved.
def convertToImage(src, dst):
    files=os.listdir(src)
    print('Source:', src)
    print('Destination', dst)
    print('Converting...')
    for file in files:
        srcPath = src+file
        dstPath = dst+file+'.png'
        f = open(srcPath, 'rb')
        ln = os.path.getsize(srcPath)
        width = int(ln**0.5)
        a = bytearray(f.read())
        f.close()
        g = np.reshape(a[:width * width], (width, width))
        g = np.uint8(g)
        img = Image.fromarray(g)
        img.save(dstPath)
    print('Files converted successfully')
    
# trainPath = directory containing the train set. valid_pct = Percent of data used for validation set. bs = batch size. get_items = Function used extract the train set. get_p = Function used to classify the train set. item_tfms = Transforms to be performed on all of the data. batch_tfms = Transforms to be performed on each batch.
# Returns a dataloader object
def loadData(trainPath, valid_pct, bs=None, get_items=get_image_files, get_y = parent_label, item_tfms = Resize(224, ResizeMethod.Pad, pad_mode='zeros'), batch_tfms = aug_transforms()):
    #aug_transforms(pad_mode='zeros', mult=2, min_scale=0.5)
    # parent_label -->> simply gets the name of the folder a file is in
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

# dls = DataLoaders object, arch = architecture, path = path to where the trained model should be exported, epoch_ct = number of iterations, metrics = the metrics used to train the model, pretrained = whether or not to use a pretrained model (False = Create model from scratch)
def trainModel(dls, arch, path, epoch_ct=1, metrics=[error_rate, accuracy], pretrained=True):
    model = cnn_learner(dls, arch, metrics=metrics, pretrained=pretrained)
    base_lr = model.lr_find()[0]
    model.fine_tune(epochs=epoch_ct, base_lr = base_lr)
    model.dls.train = dls.train
    model.dls.valid = dls.valid
    model.export(path)
    return model

# exportPath = path to the exported model, cpu = whether the model should use the cpu or gpu
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
    # Show the images that are being predicted
    img = plt.imread(item)
    plt.imshow(img)
    plt.axis('off')
    plt.title(item)
    plt.show()
    
def confusionMatrix(model):
    interp = ClassificationInterpretation.from_learner(model)
    interp.plot_confusion_matrix()
    plt.show()

# model = the trained model, testPath = the path containing the test set of images, labeled = whether or not the data has labels we can extract
def predict(model, testPath, threshold=None, labeled=False):
    warning = ''
    path = Path(testPath)
    dirs = os.listdir(path)
    files = get_image_files(Path(testPath))
    modeltotal = 0
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    for item in files:
        actual = parent_label(item)
        prediction, prediction_index, probabilities = model.predict(item)
        if(threshold is not None):
            if(prediction == 'goodware' and probabilities[prediction_index] < threshold):
                prediction = 'malware'
                warning = '| this prediction was flipped'
            elif(prediction == 'malware' and probabilities[prediction_index] < threshold):
                prediction = 'goodware'
                warning = '| this prediction was flipped'
            else:
                warning = ''
        print(f"Item: {item} | Prediction: {prediction} | Probability: {probabilities[prediction_index]:.04f} {warning}")
        if(labeled):
            if(prediction == 'malware'):
                if(actual == 'malware'):
                    true_positive += 1
                elif(actual == 'goodware'):
                    false_positive += 1
            elif(prediction == 'goodware'):
                if(actual == 'goodware'):
                    true_negative += 1
                elif(actual == 'malware'):
                    false_negative += 1
            modeltotal += 1

    if(labeled):
        accuracy = (true_positive + true_negative) / modeltotal
        precision = true_positive / (true_positive + false_positive)
        recall = true_positive / (true_positive + false_negative)
        f1_score = 2 * ((precision * recall) / (precision + recall))
        print("Accuracy", str(round(accuracy*100, 2)) + "%\nPrecision:", str(round(precision*100, 2)) + "%\nRecall:", str(round(recall*100, 2)) + "%\nF1 Score:", round(f1_score, 4))
