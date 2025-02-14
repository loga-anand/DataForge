import pandas as pd
from glob import glob
import os
import tkinter as tk
from tkinter import *
import csv

# Function to take attendance
def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.get().strip()  # Remove leading/trailing spaces
        if Subject == "":
            t = "Please enter the subject name."
            text_to_speech(t)
            return  # Exit function if subject is empty

        subject_path = os.path.join("Attendance", Subject)
        if not os.path.exists(subject_path):
            os.makedirs(subject_path)  # Create directory if it does not exist

        filenames = glob(os.path.join(subject_path, f"{Subject}*.csv"))
        if not filenames:
            text_to_speech("No attendance records found for this subject.")
            return  # Exit if no CSV files found

        # Read CSV files and merge them properly
        df_list = []
        for f in filenames:
            if os.path.getsize(f) > 0:  # Ensure file is not empty
                df = pd.read_csv(f)
                if not df.empty:
                    df_list.append(df)

        if not df_list:
            text_to_speech("Attendance files are empty!")
            return

        # Merge attendance records
        newdf = pd.concat(df_list, ignore_index=True)
        newdf.fillna(0, inplace=True)

        if newdf.empty:
            text_to_speech("No data available to calculate attendance.")
            return

        # Calculate attendance percentage
        newdf["Attendance"] = newdf.iloc[:, 2:].mean(axis=1).apply(lambda x: f"{int(round(x * 100))}%")

        # Save updated attendance records
        attendance_file = os.path.join(subject_path, "attendance.csv")
        newdf.to_csv(attendance_file, index=False)

        # Display Attendance in Tkinter Window
        show_attendance(attendance_file, Subject)

    # Function to show attendance in Tkinter table
    def show_attendance(file_path, subject):
        root = tk.Tk()
        root.title(f"Attendance of {subject}")
        root.configure(background="black")

        try:
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
        except Exception as e:
            text_to_speech(f"Error opening attendance file: {str(e)}")

        root.mainloop()

    # Tkinter GUI for entering subject name
    subject = Tk()
    subject.title("Subject Selection")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="black")

    # Title
    titl = tk.Label(subject, bg="black", relief=RIDGE, bd=10, font=("arial", 30))
    titl.pack(fill=X)

    tk.Label(
        subject,
        text="Which Subject Attendance?",
        bg="black",
        fg="green",
        font=("arial", 25),
    ).place(x=100, y=12)

    # Check Sheets Button
    def Attf():
        sub = tx.get().strip()
        if sub == "":
            text_to_speech("Please enter the subject name!")
        else:
            subject_path = os.path.join("Attendance", sub)
            if os.path.exists(subject_path):
                os.startfile(subject_path)
            else:
                text_to_speech("No records found for this subject!")

    attf = tk.Button(
        subject,
        text="Check Sheets",
        command=Attf,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=10,
        relief=RIDGE,
    )
    attf.place(x=360, y=170)

    # Subject Label & Entry
    tk.Label(
        subject,
        text="Enter Subject",
        width=10,
        height=2,
        bg="black",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("times new roman", 15),
    ).place(x=50, y=100)

    tx = tk.Entry(
        subject,
        width=15,
        bd=5,
        bg="black",
        fg="yellow",
        relief=RIDGE,
        font=("times", 30, "bold"),
    )
    tx.place(x=190, y=100)

    # View Attendance Button
    fill_a = tk.Button(
        subject,
        text="View Attendance",
        command=calculate_attendance,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=12,
        relief=RIDGE,
    )
    fill_a.place(x=195, y=170)

    subject.mainloop()
