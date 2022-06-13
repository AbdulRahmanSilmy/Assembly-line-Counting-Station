#!/usr/bin/env python
# coding: utf-8

# In[4]:
import tensorflow as tf
from PIL import Image
import time
from matplotlib import pyplot as plt
from tensorflow import keras
import cv2
import numpy as np

#Loading the tensorflow lite model
with open('model.tflite', 'rb') as fid:
    tflite_model = fid.read()
    
print("Model loades successfully")

#Extracting image dimensions necessary for the model
_,height,width,_=interpreter.get_input_details()[0]['shape']
print("Image Shape (", width, ",", height,")")

#Setting up of the model
input_index = interpreter.get_input_details()[0]["index"]
output_index = interpreter.get_output_details()[0]["index"]

#Starting video capture 
cap = cv2.VideoCapture(0)

#setting up the dimensions for the capture frame
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
print(cap.get(3),cap.get(4))

#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1400)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1000)

reg1_pred,reg2_pred=[],[]

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # boundary boxes for image classification region 
    cv2.rectangle(frame, (460, 50), (670, 900), (255, 255, 255), 2)
    cv2.rectangle(frame, (690, 50), (910, 900), (255, 255, 255), 2)
    
    # extract region 1 of image where ml classfication will be applied
    img1=frame[50:900,460:670]
    img1=cv2.cvtColor(img1,cv2.COLOR_BGR2RGB)
    img1=cv2.resize(img1,(30,100))
    
    
    # extract region 2 of image where ml classfication will be applied
    img2=frame[50:900,690:910]
    img2=cv2.cvtColor(img2,cv2.COLOR_BGR2RGB)
    img2=cv2.resize(img2,(30,100))
    
    # converting images to numpy array 
    img1=np.array(img1,dtype="float32")
    img2=np.array(img2,dtype="float32")
    

    #adding extra dimension to the image necessary for the model
    img1 = np.expand_dims(img1, axis=0)
    img2 = np.expand_dims(img2, axis=0)
    
    #running inference 
    interpreter.set_tensor(input_index, img1)
    interpreter.invoke()
    pred1=interpreter.get_tensor(output_index)
    class_pred1=list(pred1).index(np.max(pred1))
    reg1_pred.append(class_pred1)
    
    print("Region 1 count: ", class_pred1)
    

    interpreter.set_tensor(input_index, img2)
    interpreter.invoke()
    pred2=interpreter.get_tensor(output_index)
    class_pred2=list(pred2).index(np.max(pred2))
    reg2_pred.append(class_pred2)
    
    
    print("Region 2 count: ", class_pred2)
    
    
    cv2.imshow("camera feed", frame)
    #shows the image seen in region1
    #cv2.imshow("region 1",img1)
    #shows the  image seen in region2
    #cv2.imshow("region 2",img2)
    

    k = cv2.waitKey(1)
    if k == ord('q') or k==ord('Q'):
        break
        

        
cap.release()
cv2.destroyAllWindows()

