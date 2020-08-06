from PIL import Image
import tkinter as tk   # for Python3 use tkinter
import time
root = tk.Tk()
imagelist = ["dog001.gif","dog002.gif","dog003.gif",
             "dog004.gif","dog005.gif","dog006.gif","dog007.gif"]
# extract width and height info
im = tk.PhotoImage(file = "/home/christopher/NSO_LIFE/Practice/831.gif", format="gif")
width = 64
height = 64
canvas = tk.Canvas(root, width=width, height=height)
canvas.pack()
canvas.create_image(width/2.0, height/2.0, image=im)
root.mainloop()