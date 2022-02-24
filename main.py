from tkinter import *
import numpy as np
from mss import mss
from pynput.keyboard import Key, Listener, Controller
import time
import sys

if sys.platform == 'win32':
    platform = 'win'
elif sys.platform == 'darwin':
    platform = 'mac'
else:
    print("Unsupported platform")
    exit(1)

interact_key = Key.space
fishing_key = 'k'

keycontrol = Controller()
sct = mss()
root = Tk()

root.title("Hades autofish")
root.geometry("200x500")

if (platform == 'mac'):
    root.wm_attributes("-transparent", True)
    root.config(bg='systemTransparent')
elif platform == 'win':
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

root.resizable(width=True, height=True)

reading = False


def read(key):
    global reading
    if hasattr(key, "char") and key == fishing_key:
        reading = True
        keycontrol.press(interact_key)
        borderB.config(bg="green")
        borderL.config(bg="green")
        borderR.config(bg="green")
        borderT.config(bg="green")
        time.sleep(1)
        keycontrol.release(interact_key)
        lastval = 255
        while reading:
            sct_img = sct.grab({
                'top': root.winfo_y() + 29,
                'left': root.winfo_x() + 1,
                'width': root.winfo_width() - 2,
                'height': root.winfo_height() - 29
            })

            arr = np.array(sct_img)
            sum = np.sum(arr) / arr.size

            if (sum > lastval + 10):
                keycontrol.press(interact_key)
                borderB.config(bg="red")
                borderL.config(bg="red")
                borderR.config(bg="red")
                borderT.config(bg="red")
                time.sleep(0.5)
                keycontrol.release(interact_key)
                return

            lastval = sum


listener = Listener(on_press=read)
listener.start()

root.mainloop()
