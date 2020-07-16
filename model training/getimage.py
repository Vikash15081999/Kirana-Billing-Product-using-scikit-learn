import os, cv2, itertools # cv2 -- OpenCV
import numpy as np 
import pandas as pd 
from sklearn.linear_model import LogisticRegressionCV
import matplotlib.pyplot as plt 
import joblib
#%matplotlib inline
TRAIN_DIR = './train/'
TEST_DIR = './test1/'
ROWS =125 
COLS = 125
CHANNELS = 3

train_images = [TRAIN_DIR+i for i in os.listdir(TRAIN_DIR)]
test_images = [TEST_DIR+i for i in os.listdir(TEST_DIR)]

def read_image(file_path):
  img = cv2.imread(file_path, cv2.IMREAD_COLOR)
  return cv2.resize(img, (ROWS, COLS),interpolation=cv2.INTER_CUBIC)

def prep_data(images):
  m = len(images)
  n_x = ROWS*COLS*CHANNELS
  
  X = np.ndarray((n_x,m), dtype=np.uint8)
  y = np.zeros((1,m))
  #print("X.shape is {}".format(X.shape))
  
  for i,image_file in enumerate(images) :
    image = read_image(image_file)
    X[:,i] = np.squeeze(image.reshape((n_x,1)))
    if 'jbl' in image_file.lower() :
      y[0,i] = 1
    elif 'colgate' in image_file.lower() :
      y[0,i] = 0
    else : # for test data
      y[0,i] = image_file.split('/')[-1].split('.')[0]
    
  return X,y

X_train, y_train = prep_data(train_images)
X_test, test_idx = prep_data(test_images)

#print("Train shape: {}".format(X_train.shape))
#print("Test shape: {}".format(X_test.shape))



classes = {0: 'colgate',
           1: 'jbl'}

def show_images(X, y, idx) :
  image = X[idx]
  image = image.reshape((ROWS, COLS, CHANNELS))
  plt.figure(figsize=(4,2))
  plt.imshow(image)
  plt.title("This is a {}".format(classes[y[idx,0]]))
  plt.show()

#show_images(X_train.T, y_train.T, 3)

clf = LogisticRegressionCV()
X_train_lr, y_train_lr = X_train.T, y_train.T.ravel()

clf.fit(X_train_lr, y_train_lr)
#print("Model accuracy: {:.2f}%".format(clf.score(X_train_lr, y_train_lr)*100))

"""
def show_image_prediction(X, idx, model) :
  image = X[idx].reshape(1,-1)
  image_class = classes[model.predict(image).item()]
  image = image.reshape((ROWS, COLS, CHANNELS))
  plt.figure(figsize = (4,2))
  plt.imshow(image)
  plt.title("Test {} : I think this is {}".format(idx, image_class))
  plt.show()

X_test_lr, test_idx = X_test.T, test_idx.T

for i in np.random.randint(0, len(X_test_lr), 10) :
  show_image_prediction(X_test_lr, i, clf)
"""
filename='JORC_classifier.joblib.pkl'
joblib.dump(clf, filename)

