
import cv2
import joblib
import numpy as np


classes = {0: 'colgate',
           1: 'jbl'}

ROWS=COLS=125
CHANNELS=3
def predict():
    model = joblib.load("JORC_classifier.joblib.pkl")
    image=cv2.imread(r'image.jpeg')
    image=image.reshape(4,46875)
    
    class_number=model.predict(image)
    
    image_class = classes[class_number[-1]]

    
    return {
        "prediction":class_number,
        "category":  image_class
    }
