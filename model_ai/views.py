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

class PredictAPIView(APIView):
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PredictSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            img = serializer.validated_data['image']
            img = img.read()  
            print("Image read from InMemoryUploadedFile.")
            img = tf.image.decode_image(img, channels=3)  
            print("Image decoded.")
            img = tf.image.resize_with_pad(img, 224, 224) 
            print("Image resized with padding.")
            img = np.array(img) / 255.0  
            print("Image pixel values normalized.")
            print("Loading model...")
            model_path = 'model_ai/model.h5'
            model = tf.keras.models.load_model(model_path, custom_objects={'KerasLayer': hub.KerasLayer}, compile=False)
            # model = tf.keras.models.load_model('model_ai/model.h5', custom_objects={'KerasLayer': hub.KerasLayer}, compile=False)
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
        try:
            f_id = Food.objects.get(englishName = predicted_class_name)
            # if not f_id.exists():
            #     return Response({"message":"This food is not supported"})
            print(f_id)
            print(predicted_class_name)
            category = Category.objects.filter(food=f_id.id)[0]
            print(category)
            food = category.food.first()
            
            allergies = category.allergy.all()
            allergy_names = ""
            for allergy in allergies:
                allergy_names = allergy_names + str(allergy.englishName) +' ,'
            food_name = food.englishName
            print("Food Found:", food)
               
            data = {
                    'category_name': category.englishName,
                    'food_name': food_name,
                    'allergies': f'This meal may cause a {allergy_names.rstrip(allergy_names[-1])}',
                }
            print("Returning the response...")
            return Response(data, status=status.HTTP_200_OK)
            
        except Http404:
            print("Category not found.")
            return Response({'error': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': 'This meal is not supported'}, status=status.HTTP_404_NOT_FOUND)

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             img = serializer.validated_data['image']
#             img = img.read()  
#             print("Image read from InMemoryUploadedFile.")
#             img = tf.image.decode_image(img, channels=3)  
#             print("Image decoded.")
#             img = tf.image.resize_with_pad(img, 224, 224) 
#             print("Image resized with padding.")
#             img = np.array(img) / 255.0  
#             print("Image pixel values normalized.")
#             print("Loading model...")
#             model_path = 'model_ai/model.h5'
#             model = tf.keras.models.load_model(model_path, custom_objects={'KerasLayer': hub.KerasLayer}, compile=False)
#             # model = tf.keras.models.load_model('model_ai/model.h5', custom_objects={'KerasLayer': hub.KerasLayer}, compile=False)
#             model.build((None, 224, 224, 3))
#             print("Model loaded.")
#             prediction = model.predict(np.array([img]))
#             print("Prediction :", prediction)
#             prediction_class = np.argmax(prediction)
#             print("prediction_classsssssss:", prediction_class)
#             predicted_class_index = np.argmax(prediction)
         
#             class_names = ['Burger', 'Dairy product', 'Donut', 'Egg', 'Meat', 'Noodles-Pasta', 'Pizza',
#             'Sandwich', 'Seafood', 'cake', 'hotDog','sushi']   

#             predicted_class_name = class_names[predicted_class_index]
#             print("Prediction class:", prediction_class)
#             print("Prediction NAAAAMAMMMMMMMEEEEEEEEEEE:", predicted_class_name)

           
#         try:
#             f_id = Food.objects.get(englishName = predicted_class_name)
#             print(f_id)
#             print(predicted_class_name)
#             category = Category.objects.filter(food= f_id.id)[0]
#             print(category)
#             food = category.food.first()
            
#             allergies = category.allergy.all()
#             allergy_names = [allergy.englishName for allergy in allergies]
#             food_name = food.englishName
#             print("Food Found:", food)
               
#             data = {
#                     'category_name': category.englishName,
#                     'food_name': food_name,
#                     'allergies': allergy_names,
#                 }
                
               
#             print("Returning the response...")
#             return Response(data, status=status.HTTP_200_OK)
            
#         except Http404:
#             print("Category not found.")
#             return Response({'error': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)

