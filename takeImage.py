import csv
import os
import cv2
import numpy as np
import pandas as pd
import datetime
import time

# Function to take the image of the user and save it.
def TakeImage(l1, l2, haarcasecade_path, trainimage_path, message, err_screen, text_to_speech):
    if (l1 == "") and (l2 == ""):
        t = 'Please enter your Enrollment Number and Name.'
        text_to_speech(t)
    elif l1 == "":
        t = 'Please enter your Enrollment Number.'
        text_to_speech(t)
    elif l2 == "":
        t = 'Please enter your Name.'
        text_to_speech(t)
    else:
        try:
            cam = cv2.VideoCapture(0)
            detector = cv2.CascadeClassifier(haarcasecade_path)
            Enrollment = l1
            Name = l2
            sampleNum = 0
            directory = Enrollment + "_" + Name
            path = os.path.join(trainimage_path, directory)
            if not os.path.exists(path):
                os.mkdir(path)
            
            while True:
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    sampleNum = sampleNum + 1
                    cv2.imwrite(
                        os.path.join(path, f"{Name}_{Enrollment}_{sampleNum}.jpg"),
                        gray[y : y + h, x : x + w],
                    )
                    cv2.imshow("Frame", img)
                
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
                elif sampleNum > 50:
                    break
            
            cam.release()
            cv2.destroyAllWindows()
            
            # Save student details in CSV
            row = [Enrollment, Name]
            student_file = "StudentDetails/studentdetails.csv"
            if not os.path.exists("StudentDetails"):
                os.mkdir("StudentDetails")
            
            with open(student_file, "a+", newline='') as csvFile:
                writer = csv.writer(csvFile, delimiter=",")
                writer.writerow(row)
            
            res = f"Images saved for Enrollment No: {Enrollment}, Name: {Name}"
            message.configure(text=res)
            text_to_speech(res)
        
        except FileExistsError as F:
            error_message = "Student data already exists"
            err_screen.configure(text=error_message)
            text_to_speech(error_message)
