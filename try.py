import pathlib
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PredictSerializer
from database.models import Food, Category
import tensorflow as tf
import numpy as np
from .serializers import *
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras import Model
import tensorflow_hub as hub
from django.conf import settings
from rest_framework import status
from tensorflow.keras.preprocessing import image
from rest_framework.permissions import IsAuthenticated
import io
from django.shortcuts import get_object_or_404
from django.http import Http404

# from rest_framework import permissions

img = path() 
img = img.read()  
print("Image read from InMemoryUploadedFile.")
img = tf.image.decode_image(img, channels=3)  
print("Image decoded.")
img = tf.image.resize_with_pad(img, 224, 224) 
print("Image resized with padding.")
img = np.array(img) / 255.0  
print("Image pixel values normalized.")


print("Loading model...")
model = tf.keras.models.load_model('model_ai/model.h5', custom_objects={'KerasLayer': hub.KerasLayer}, compile=False)
model.build((None, 224, 224, 3))
print("Model loaded.")
prediction = model.predict(np.array([img]))
print("Prediction :", prediction)
prediction_class = np.argmax(prediction)
print("prediction_classsssssss:", prediction_class)
predicted_class_index = np.argmax(prediction)
         
class_names = ['Burger', 'Dairy product', 'Donut', 'Egg', 'Meat', 'Noodles-Pasta', 'Pizza',
    'Sandwich', 'Seafood', 'cake', 'hotDog','sushi']   

predicted_class_name = class_names[predicted_class_index]
print("Prediction class:", prediction_class)
print("Prediction NAAAAMAMMMMMMMEEEEEEEEEEE:", predicted_class_name)