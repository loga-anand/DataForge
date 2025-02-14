import csv
import os, cv2
import numpy as np
import pandas as pd
import datetime
import time
from PIL import ImageTk, Image

# Train Image Function
def TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, message, text_to_speech):
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    detector = cv2.CascadeClassifier(haarcasecade_path)
    
    faces, Id = getImagesAndLables(trainimage_path)
    recognizer.train(faces, np.array(Id))
    recognizer.save(trainimagelabel_path)
    
    res = "Images Trained successfully"  # +",".join(str(f) for f in Id)
    message.configure(text=res)
    text_to_speech(res)

# Function to get images and labels from the training folder
def getImagesAndLables(path):
    newdir = [os.path.join(path, d) for d in os.listdir(path)]  # Get subfolders (students' directories)
    imagePath = [
        os.path.join(newdir[i], f)
        for i in range(len(newdir))
        for f in os.listdir(newdir[i])  # Get all images from each student's folder
    ]
    
    faces = []
    Ids = []
    for imagePath in imagePath:
        pilImage = Image.open(imagePath).convert("L")  # Convert image to grayscale
        imageNp = np.array(pilImage, "uint8")
        
        # Assuming the image filename format is 'Name_Enrollment_#.jpg'
        Id = int(os.path.split(imagePath)[-1].split("_")[1])  # Extract Enrollment Number (ID) from filename
        
        faces.append(imageNp)
        Ids.append(Id)
    
    return faces, Ids
