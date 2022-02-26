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

# The keybind in Hades set under "interact" -- this is the keybind used for fishing
interact_key = Key.shift
# The hotkey to start fishing once the window has been aligned
fishing_key = 'k'

keyboard = Controller()
sct = mss()
root = Tk()

root.title("Hades autofish")
root.geometry("200x500")

# Sets the background of the interface to be transparent on MacOS and Windows
if (platform == 'mac'):
    root.wm_attributes("-transparent", True)
    root.config(bg='systemTransparent')
elif platform == 'win':
    root.configure(bg='white')
    root.wm_attributes("-transparentcolor", "white")

# Makes the window resizable and always-on-top
root.attributes('-topmost', True)
root.resizable(width=True, height=True)

# Initializes the colored frame around the window to indicate status
borderL = Frame(root, width=5, bg="red")
borderL.pack(expand=False, fill="y", side=LEFT)

borderR = Frame(root, width=5, bg="red")
borderR.pack(expand=False, fill="y", side=RIGHT)

borderT = Frame(root, height=5, bg="red")
borderT.pack(expand=False, fill="x", side=TOP)

borderB = Frame(root, height=5, bg="red")
borderB.pack(expand=False, fill="x", side=BOTTOM)


# Watches the screen at the boundaries of the window and triggers when the average pixel value jumps up
def watch(key):
    if hasattr(key, "char") and key.char == fishing_key:  # Check if the hotkey is pressed
        keyboard.press(interact_key)  # Begin fishing
        borderB.config(bg="green")
        borderL.config(bg="green")
        borderR.config(bg="green")
        borderT.config(bg="green")
        # Wait for the initial fishing animation to finish to prevent unintentional activation
        time.sleep(1)
        keyboard.release(interact_key)
        lastval = 255
        while True:
            # Grab the screenshot at the boundaries of the window
            sct_img = sct.grab({
                'top': root.winfo_y() + 29,
                'left': root.winfo_x() + 1,
                'width': root.winfo_width() - 2,
                'height': root.winfo_height() - 29
            })

            # Average all pixel values
            arr = np.array(sct_img)
            sum = np.sum(arr) / arr.size

            if (sum > lastval + 10):
                # If the average pixel value has jumped up, activate the keybind
                keyboard.press(interact_key)
                borderB.config(bg="red")
                borderL.config(bg="red")
                borderR.config(bg="red")
                borderT.config(bg="red")
                time.sleep(0.5)
                keyboard.release(interact_key)
                return

            lastval = sum


# Listens globally for all keypresses
listener = Listener(on_press=watch)
listener.start()

# Run the tkinter main loop
root.mainloop()
