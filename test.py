import requests
import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

# URL of the camera feed
url = "http://192.168.0.6:8080/shot.jpg"

# Create a tkinter window
window = tk.Tk()
window.title("Live Camera Feed")
window.geometry("640x480")
window.configure(background="snow")

# Initialize the camera stream
def get_frame():
    # Fetch the camera image
    cam = requests.get(url)
    img_np = np.array(bytearray(cam.content), dtype=np.uint8)
    img = cv2.imdecode(img_np, -1)

    # Convert the OpenCV image (BGR) to PIL format (RGB)
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    img_tk = ImageTk.PhotoImage(img_pil)

    # Update the label with the new frame
    label_img.config(image=img_tk)
    label_img.image = img_tk

    # Call the function again after 10 ms to update the feed
    label_img.after(10, get_frame)

# Create a label to display the camera feed
label_img = tk.Label(window)
label_img.pack()

# Start the frame update
get_frame()

# Run the tkinter event loop
window.mainloop()
