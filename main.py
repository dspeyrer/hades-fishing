from tkinter import *
from PIL import ImageTk, Image, ImageGrab
import numpy as np
import cv2
from mss import mss
from PIL import Image
from pynput import keyboard
import time

keycontrol = keyboard.Controller()

sct = mss()

root = Tk()

# Set Title as Image Loader
root.title("Image Loader")

# Set the resolution of window
root.geometry("550x300")

#root.wm_attributes("-transparent", True)
# root.config(bg='systemTransparent')

root.configure(bg='white')

root.wm_attributes("-transparentcolor", "white")

root.attributes('-topmost', True)

borderL = Frame(root, width=5, bg="red")
borderL.pack(expand=False, fill="y", side=LEFT)

borderR = Frame(root, width=5, bg="red")
borderR.pack(expand=False, fill="y", side=RIGHT)

borderT = Frame(root, height=5, bg="red")
borderT.pack(expand=False, fill="x", side=TOP)

borderB = Frame(root, height=5, bg="red")
borderB.pack(expand=False, fill="x", side=BOTTOM)


# Allow Window to be resizable
root.resizable(width=True, height=True)


reading = False


def toggle_graphing(key):
    global reading
    if hasattr(key, "char") and key.char == 'k':
        reading = True
        keycontrol.press(keyboard.Key.shift)


listener = keyboard.Listener(on_press=toggle_graphing)
listener.start()

while True:
    if reading:
        borderB.config(bg="green")
        borderL.config(bg="green")
        borderR.config(bg="green")
        borderT.config(bg="green")
        root.update_idletasks()
        root.update()
        time.sleep(1)
        lastval = 255
        while reading:
            sct_img = sct.grab({'top': root.winfo_y() + 29, 'left': root.winfo_x(
            ) + 1, 'width': root.winfo_width() - 2, 'height': root.winfo_height() - 29})
            arr = np.array(sct_img)
            # cv2.imshow('screen', arr)

            sum = np.sum(arr) / arr.size

            if (sum > lastval + 10):
                print("activated")
                keycontrol.press(keyboard.Key.shift)
                borderB.config(bg="red")
                borderL.config(bg="red")
                borderR.config(bg="red")
                borderT.config(bg="red")
                reading = False

            lastval = sum
    #
    root.update_idletasks()
    root.update()
