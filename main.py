from random import randint, choice
import math
import time
import tkinter as tk
import os

class scena:

    def __init__(self, root, nazev : str):
        self.root = root
        self.objects = []
        self.widgets = []
        self.window = tk.Frame(self.root, background = "black")
        self.window.grid(row=1, column=1, sticky="nsew")
        self.isloaded = False

        self.nazev = nazev

    def load(self):
        self.isloaded = True
        return

    def unload(self):
        self.window.destroy()

    def update(self):
        return



class hra:
   def __init__(self):
       self.root = tk.Tk()
       self.root.geometry("800x400")
       self.root.title("Space fighters")
       self.root.resizable(width=False, height=False)


       self.root.columnconfigure(1, weight = 1)
       self.root.rowconfigure(1, weight = 1)

       #sceny
       self.currentScene : scena = None


       #input
       self.root.bind("w", lambda e : self.CaptureInput("up"))
       self.root.bind("s", lambda e : self.CaptureInput("down"))
       self.root.bind("a", lambda e : self.CaptureInput("left"))
       self.root.bind("d", lambda e : self.CaptureInput("right"))
       self.root.bind("e", lambda e : self.CaptureInput("interact"))
       self.root.bind("q", lambda e : self.CaptureInput("back"))
       self.root.bind("<space>", lambda e : self.CaptureInput("shoot"))
       self.currentInput : str = None


       self.root.after(1000, self.update)
       self.root.mainloop()
   def update(self):
       self.inputUpdate()
       self.GameUpdate()
       self.WindowUpdate()
       self.root.after(100, self.update)
   def inputUpdate(self):
       if self.currentInput:

           match self.currentInput:
               case "up":
                   print("up")
               case "down":
                   print("down")
               case "left":
                   print("left")
               case "right":
                   print("right")
               case "interact":
                   print("interact")
               case "back":
                   print("back")
               case "shoot":
                   print("shoot")


       self.currentInput = None
       return
   def GameUpdate(self):
       #print("game")
       return
   def WindowUpdate(self):
       if not self.currentScene:
           self.currentScene = scena("Menu")
       if not self.currentScene.isloaded :
           self.currentScene.load()




   def CaptureInput(self, inputStr : str):
       self.currentInput = inputStr

hra()
