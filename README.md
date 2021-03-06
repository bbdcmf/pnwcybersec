# A Deep Learning Malware Detection Module
https://pypi.org/project/pnwcybersec/

For GPU support see: https://pytorch.org/get-started/locally/

## Module Documentation

### **Functions:**

#### **convertToImage(src, dst)**
     Description:
          Converts executable files to images.
     Input:
          src: The source path to the directory containing the executables that will be converted to images. Type: string
          dst: The destination path to the directory where the image(s) will be saved to. Type: string
     Output:
          Converted executable image file(s)						
#### **loadData(trainPath, valid_pct, bs=None, get_items=get_image_files, get_y=parent_label, item_tfms=Resize(224, ResizeMethod.Pad, pad_mode='zeros'), batch_tfms=aug_transforms())**
     Description:
          Loads all of the data that will be used for the CNN model.
     Input:
          trainPath: Directory path containing the train set image file(s). Type: string
          valid_pct: The percent of the train set's files that will be used for the validation set. Type: float
          bs: Batch size, default=None. Type: int
          get_items: The function used to extract the files from the train set, default=get_image_files, which returns the path to all the image files from the specified directory.
          get_y: The function used to extract the labels for each image sample. Default=parent_label, which returns the name of the folder the sample image file is stored in.
          item_tfms: Transforms that will be done to each image sample. Default=Resize(224, ResizeMethod.Pad, pad_mode='zeros'), which will resize the image so that the shorter dimension is matched to the image size of 224 and then padded with zeros. Helps to ensure data is not lost.
          batch_tfms: Transforms that will be done to each sample in a batch. Default=aug_transforms(), which is a utility function to easily create a list of flip, rotate, zoom, warp, and lighting transforms.
     Output:
          dls: A fast.ai DataLoaders object.		
#### **trainModel(dls, arch, path, epoch_ct=1, metrics=error_rate, pretrained=True)**
     Description:
          Creates and trains the CNN model.
     Input:
          dls: A fastai DataLoaders object.
          arch: The architecture that the model will use to train.
          path: The path to where the exported model will be saved. Must specifiy the fileName.pkl.
          epoch_ct: The number of iterations. Default=1. Type: int
          metrics: The metrics used to determine how well the model is training. Default=error_rate.
          pretrained: Whether or not to use a pretrained model. False=Create model from scratch. Default=True. Type: boolean
     Output:
          model: The trained model		
#### **loadModel(exportPath, cpu=False)**
     Description:
          Load an exported trained model
     Input:
          exportPath: The path to the exported model. Type: string
          cpu: Whether or not the model should only use a cpu. False=The model will use a GPU. Type: boolean
     Output:
          model: The trained model		
#### **getBestModel(cpu=False)**
     Description: 
          Loads our most accurate model that was trained to detect malware
     Input:
          cpu: Whether or not the model should only use a cpu. False=The model will use a GPU. Type: boolean
     Output:
          model: The trained model			
#### **showImage(item)**
     Description:
          Displays the specified image file
     Input:
          item: The path to the image file you want displayed. Type: string
#### **confusionMatrix(model)**
     Description:
          Displays a confusion matrix for the specified model
     Input:
          model: The trained model		
#### **def predict(model, testPath, labeled=False, pos_lbl=None, neg_lbl=None, threshold=None)**
     Description:
          Prints the prediction and probability of that prediction, for each sample specified. 
     Input:
          model: The trained model used to predict the samples
          testPath: The path to the directory containing the test set. Type: string
          labeled: Whether or not the test samples' labels can be extracted from the name of the directory they are stored in. If labeled, then this function will print the accuracy of all of its predictions for the test set. Expected labels are: ['malware', 'goodware']. Type: boolean
          pos_lbl = Label that corresponds to positive when determining true positive vs. false positive
          neg_lbl = Label that corresponds to negative when determining true negative vs. false negative
          threshold: The probability threshold for when a prediction should not be trusted. Any prediction's probability below the threshold will be flipped and flagged. Type: float
