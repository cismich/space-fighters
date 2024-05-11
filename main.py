from random import randint, choice
import math
import time
import tkinter as tk
import os

class scena:

    def __init__(self, root, hra, nazev : str):
        self.hra = hra
        self.root = root
        self.window = tk.Frame(self.root, background = "black")
        self.window.grid(row=1, column=1, sticky="nsew")
        self.isloaded = False
        self.input = None

        self.nazev = nazev
    
    def __del__(self):
       self.unload()

    def load(self):
        self.isloaded = True
        return

    def unload(self):
        self.window.destroy()

    def update(self):
        hra.LoadScene(self.hra, "Menu")
        return
    def updateInput(self, gameInput : str):
        match gameInput:
               case "up":
                 self.input = "up"
               case "down":
                 self.input = "down"
               case "left":
                 self.input = "left"
               case "right":
                 self.input = "right"
               case "interact":
                 self.input = "interact"
               case "back":
                 self.input = "back"
               case "shoot":
                 self.input = "shoot"




class HraScena(scena):
    def __init__(self, root, hra, nazev : str):
       scena.__init__(self, root, hra, nazev)
       self.window.columnconfigure(2, weight=1)
       self.window.rowconfigure(1, weight=1)

       self.GameScreen = tk.Frame(self.window, background="white").grid(row=1, column=1, sticky="nsew")
       self.InfoScreen = tk.Frame(self.window, background="black").grid(row=1, column=2, sticky="nsew")



    def update(self):
        print("america ya >:P")

class MenuScena(scena):
    def __init__(self, root, hra, nazev : str):
       scena.__init__(self, root, hra, nazev)
       
       self.window.rowconfigure(5, weight=1)
       self.window.columnconfigure(1, weight=1)
       tk.Label(self.window, text= "Space Fighters", background="black", foreground="white", font=("Cascadia Code", 48)).grid(row=1, column=1, sticky="nsew")
       tk.Label(self.window, text= "Start [Mezernik]", background="black", foreground="white", font=("Cascadia Code", 18)).grid(row=2, column=1, sticky="nsew")
       tk.Label(self.window, text= "odejit [q]", background="black", foreground="white", font=("Cascadia Code", 18)).grid(row=3, column=1, sticky="nsew")

    def update(self):
       if self.input == "back":
         self.root.destroy()
       elif self.input == "shoot":
          self.hra.LoadScene("Game")
          
        


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
          self.currentScene.updateInput(self.currentInput)

       self.currentInput = None
       return
   def GameUpdate(self):
       if self.currentScene:
          self.currentScene.update()
       return
   def WindowUpdate(self):
       if not self.currentScene:
           self.currentScene = scena(self.root, self, "Main")
       if not self.currentScene.isloaded :
           self.currentScene.load()

   def LoadScene(self, scene : str):
      self.currentScene = None
      if scene == "Menu":
        self.currentScene = MenuScena(self.root, self, "Menu")
      elif scene == "Game":
         self.currentScene = HraScena(self.root, self, "Game")




   def CaptureInput(self, inputStr : str):
       self.currentInput = inputStr

hra()
