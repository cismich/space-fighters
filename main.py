from random import randint, choice
import math
import time
import tkinter as tk
import os

class hra:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x400")
        self.root.title("Space fighters")
        self.root.resizable(width=False, height=False)
        self.root.configure(background="black")

        #input
        self.root.bind("w", lambda e : self.CaptureInput("up"))
        self.root.bind("s", lambda e : self.CaptureInput("down"))
        self.root.bind("a", lambda e : self.CaptureInput("left"))
        self.root.bind("d", lambda e : self.CaptureInput("right"))
        self.root.bind("e", lambda e : self.CaptureInput("interact"))
        self.root.bind("q", lambda e : self.CaptureInput("back"))
        self.root.bind("<space>", lambda e : self.CaptureInput("shoot"))


        self.root.after(1000, self.update)
        self.root.mainloop()
    def update(self):
        self.inputUpdate()
        self.GameUpdate()
        self.WindowUpdate()

        self.root.after(100, self.update)

    def inputUpdate(self):
        #print("update")
        return
    
    def GameUpdate(self):
        #print("game")
        return
    
    def WindowUpdate(self):
        #print("window")
        return

    def CaptureInput(self, inputStr : str):
        print(inputStr)

    
hra()
