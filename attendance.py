import tkinter as tk
from tkinter import *
import os, cv2
import shutil
import csv
import numpy as np  # Ensure you're using numpy 2.2.2
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.font as font
import pyttsx3

# Project module imports
import show_attendance
import takeImage
import trainImage
import automaticAttedance


def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()


haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = "TrainingImageLabel/Trainner.yml"
trainimage_path = "TrainingImage"

# Ensure the required directories exist
if not os.path.exists(trainimage_path):
    os.makedirs(trainimage_path)

studentdetail_path = "StudentDetails/studentdetails.csv"
attendance_path = "Attendance"

# Main Tkinter Window
window = Tk()
window.title("Face Recognizer")
window.geometry("1280x720")
window.configure(background="black")

# Error message for missing inputs
def err_screen():
    sc1 = tk.Tk()
    sc1.geometry("400x110")
    sc1.title("Warning!")
    sc1.configure(background="black")
    sc1.resizable(0, 0)
    tk.Label(
        sc1,
        text="Enrollment & Name required!",
        fg="yellow",
        bg="black",
        font=("times", 20, "bold"),
    ).pack()
    tk.Button(
        sc1,
        text="OK",
        command=sc1.destroy,
        fg="yellow",
        bg="black",
        width=9,
        height=1,
        font=("times", 20, "bold"),
    ).place(x=110, y=50)

# Validation function for enrollment input
def testVal(inStr, acttyp):
    return acttyp != "1" or inStr.isdigit()

# UI Elements
logo = Image.open("UI_Image/0001.png").resize((50, 47), Image.Resampling.LANCZOS)
logo1 = ImageTk.PhotoImage(logo)

titl = tk.Label(window, bg="black", relief=RIDGE, bd=10, font=("arial", 35))
titl.pack(fill=X)
l1 = tk.Label(window, image=logo1, bg="black")
l1.place(x=470, y=10)

titl = tk.Label(window, text="Smart Attendance!!", bg="black", fg="red", font=("Elephant", 27))
titl.place(x=525, y=12)

a = tk.Label(
    window,
    text="Welcome to the Face Recognition \nAttendance Management System",
    bg="black",
    fg="yellow",
    bd=10,
    font=("arial", 35),
)
a.pack()

# Image Loading
ri = Image.open("UI_Image/register.png")
r = ImageTk.PhotoImage(ri)
ai = Image.open("UI_Image/attendance.png")
a = ImageTk.PhotoImage(ai)
vi = Image.open("UI_Image/verifyy.png")
v = ImageTk.PhotoImage(vi)

Label(window, image=r).place(x=100, y=270)
Label(window, image=a).place(x=980, y=270)
Label(window, image=v).place(x=600, y=270)

# Take Image UI
def TakeImageUI():
    ImageUI = Tk()
    ImageUI.title("Take Student Image")
    ImageUI.geometry("780x480")
    ImageUI.configure(background="black")

    tk.Label(ImageUI, text="Register Your Face", bg="black", fg="green", font=("arial", 30)).pack(fill=X)

    # Input Fields
    lbl1 = tk.Label(ImageUI, text="Enrollment No", bg="black", fg="yellow", font=("times new roman", 12))
    lbl1.place(x=120, y=130)
    txt1 = tk.Entry(ImageUI, validate="key", bg="black", fg="yellow", font=("times", 25, "bold"))
    txt1["validatecommand"] = (txt1.register(testVal), "%P", "%d")
    txt1.place(x=250, y=130)

    lbl2 = tk.Label(ImageUI, text="Name", bg="black", fg="yellow", font=("times new roman", 12))
    lbl2.place(x=120, y=200)
    txt2 = tk.Entry(ImageUI, bg="black", fg="yellow", font=("times", 25, "bold"))
    txt2.place(x=250, y=200)

    lbl3 = tk.Label(ImageUI, text="Notification", bg="black", fg="yellow", font=("times new roman", 12))
    lbl3.place(x=120, y=270)

    message = tk.Label(ImageUI, text="", bg="black", fg="yellow", font=("times", 12, "bold"))
    message.place(x=250, y=270)

    # Functions
    def take_image():
        takeImage.TakeImage(
            txt1.get(),
            txt2.get(),
            haarcasecade_path,
            trainimage_path,
            message,
            err_screen,
            text_to_speech,
        )
        txt1.delete(0, "end")
        txt2.delete(0, "end")

    def train_image():
        trainImage.TrainImage(
            haarcasecade_path,
            trainimage_path,
            trainimagelabel_path,
            message,
            text_to_speech,
        )

    # Buttons
    tk.Button(ImageUI, text="Take Image", command=take_image, bg="black", fg="yellow", font=("times new roman", 18)).place(x=130, y=350)
    tk.Button(ImageUI, text="Train Image", command=train_image, bg="black", fg="yellow", font=("times new roman", 18)).place(x=360, y=350)

# Buttons on Main Window
tk.Button(window, text="Register a new student", command=TakeImageUI, bg="black", fg="yellow", font=("times new roman", 16)).place(x=100, y=520)
tk.Button(window, text="Take Attendance", command=lambda: automaticAttedance.subjectChoose(text_to_speech), bg="black", fg="yellow", font=("times new roman", 16)).place(x=600, y=520)
tk.Button(window, text="View Attendance", command=lambda: show_attendance.subjectchoose(text_to_speech), bg="black", fg="yellow", font=("times new roman", 16)).place(x=1000, y=520)
tk.Button(window, text="EXIT", command=window.quit, bg="black", fg="yellow", font=("times new roman", 16)).place(x=600, y=660)

window.mainloop()
