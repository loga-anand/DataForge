import tkinter as tk
from tkinter import *
import os, cv2
import csv
import pandas as pd
import datetime
import time
import numpy as np
from PIL import Image
import tkinter.ttk as tkk

haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = "TrainingImageLabel/Trainner.yml"
trainimage_path = "TrainingImage"
studentdetail_path = "StudentDetails/studentdetails.csv"
attendance_path = "Attendance"

# Define Entry widget correctly for the subject input
def subjectChoose(text_to_speech):
    def FillAttendance():
        sub = tx.get().strip()  # Ensure no spaces
        if not sub:
            t = "Please enter the subject name!!!"
            text_to_speech(t)
            return

        try:
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            if not os.path.exists(trainimagelabel_path):
                e = "Model not found, please train the model."
                Notifica.configure(text=e, bg="black", fg="yellow", font=("times", 15, "bold"))
                Notifica.place(x=20, y=250)
                text_to_speech(e)
                return

            recognizer.read(trainimagelabel_path)
            faceCascade = cv2.CascadeClassifier(haarcasecade_path)
            df = pd.read_csv(studentdetail_path)

            cam = cv2.VideoCapture(0)
            if not cam.isOpened():
                text_to_speech("Error: Camera not found!")
                return

            font = cv2.FONT_HERSHEY_SIMPLEX
            col_names = ["Enrollment", "Name"]
            attendance = pd.DataFrame(columns=col_names)

            end_time = time.time() + 20  # 20 seconds to take attendance

            while time.time() < end_time:
                ret, frame = cam.read()
                if not ret:
                    continue

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = faceCascade.detectMultiScale(gray, 1.2, 5)

                for (x, y, w, h) in faces:
                    Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
                    if conf < 70:
                        name = df.loc[df["Enrollment"] == Id, "Name"].values
                        if len(name) > 0:
                            name = name[0]
                            attendance.loc[len(attendance)] = [Id, name]
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
                            cv2.putText(frame, f"{Id}-{name}", (x, y-10), font, 1, (255, 255, 0), 2)
                        else:
                            continue
                    else:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 4)
                        cv2.putText(frame, "Unknown", (x, y-10), font, 1, (0, 0, 255), 2)

                attendance.drop_duplicates(subset=["Enrollment"], keep="first", inplace=True)
                cv2.imshow("Filling Attendance...", frame)

                if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit early
                    break

            cam.release()
            cv2.destroyAllWindows()

            # Save attendance record
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            timestamp = datetime.datetime.now().strftime("%H-%M-%S")
            attendance[date] = 1  # Mark present
            subject_path = os.path.join(attendance_path, sub)

            if not os.path.exists(subject_path):
                os.makedirs(subject_path)

            fileName = f"{subject_path}/{sub}_{date}_{timestamp}.csv"
            attendance.to_csv(fileName, index=False)

            m = f"Attendance Filled Successfully for {sub}"
            Notifica.configure(text=m, bg="black", fg="yellow", font=("times", 15, "bold"))
            Notifica.place(x=20, y=250)
            text_to_speech(m)

            # Display attendance records
            showAttendance(fileName, sub)

        except Exception as e:
            text_to_speech(f"Error: {str(e)}")
            cv2.destroyAllWindows()

    # Function to display attendance
    def showAttendance(file_path, subject):
        if not os.path.exists(file_path):
            text_to_speech("Attendance file not found!")
            return

        root = tk.Tk()
        root.title(f"Attendance of {subject}")
        root.configure(background="black")

        with open(file_path, newline="") as file:
            reader = csv.reader(file)
            for r, row in enumerate(reader):
                for c, value in enumerate(row):
                    label = tk.Label(
                        root,
                        width=12,
                        height=1,
                        fg="yellow",
                        font=("times", 15, "bold"),
                        bg="black",
                        text=value,
                        relief=tk.RIDGE,
                    )
                    label.grid(row=r, column=c)

        root.mainloop()

    # Tkinter GUI for entering subject name
    subject = Tk()
    subject.title("Subject Selection")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="black")

    # Title
    tk.Label(subject, text="Enter the Subject Name", bg="black", fg="green", font=("arial", 25)).place(x=160, y=12)

    Notifica = tk.Label(subject, text="Attendance filled Successfully", bg="yellow", fg="black",
                        width=33, height=2, font=("times", 15, "bold"))

    # Function to check attendance sheets
    def Attf():
        sub = tx.get().strip()
        if sub == "":
            text_to_speech("Please enter the subject name!")
        else:
            subject_folder = os.path.join(attendance_path, sub)
            if os.path.exists(subject_folder):
                os.startfile(subject_folder)
            else:
                text_to_speech("No records found for this subject!")

    attf = tk.Button(subject, text="Check Sheets", command=Attf, bd=7, font=("times new roman", 15),
                     bg="black", fg="yellow", height=2, width=10, relief=RIDGE)
    attf.place(x=360, y=170)

    # Subject Label & Entry
    tk.Label(subject, text="Enter Subject", width=10, height=2, bg="black", fg="yellow",
             bd=5, relief=RIDGE, font=("times new roman", 15)).place(x=50, y=100)

    tx = tk.Entry(subject, width=15, bd=5, bg="black", fg="yellow", relief=RIDGE, font=("times", 30, "bold"))
    tx.place(x=190, y=100)

    # Fill Attendance Button
    fill_a = tk.Button(subject, text="Fill Attendance", command=FillAttendance, bd=7, font=("times new roman", 15),
                       bg="black", fg="yellow", height=2, width=12, relief=RIDGE)
    fill_a.place(x=195, y=170)

    subject.mainloop()
