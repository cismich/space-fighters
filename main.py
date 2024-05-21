from random import randint, choice
import math
import time
import tkinter as tk
import os

shared = {
   "vlna" : 1,
   "body" : 0,
   "u_dostrel" : 0,
   "u_poskozeni" : 0,
   "u_zivot" : 0
}

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
class Object:
  def __init__(self):
     self.x = 0
     self.y = 0
  def getType(self):
     return "Object"

  def Update(self, hraScena):
      return

class Player(Object):
  def __init__(self):
     super().__init__()
  def getType(self):
     return "Player"

class Nepritel(Object):
    def __init__(self, lives = 1):
        super().__init__()
        self.lives = lives

    def getType(self):
        return "Enemy"
    def hit(self, poskozeni = 1):
       self.lives -= poskozeni
          

class Strela(Object):
    def __init__(self, maxTime : int):
        super().__init__()
        self.time = 0
        self.maxBulletTime = maxTime

    def getType(self):
        return "Bullet"

    def Update(self, hraScena):
        hraScena.ObjMoveToRelative(self, 0, -1)

        if self.time >= self.maxBulletTime:
            hraScena.ObjDestory(self)
        self.time += 100


class HraScena(scena):
   def __init__(self, root, hra, nazev : str):
      scena.__init__(self, root, hra, nazev)
      self.window.columnconfigure(1, weight=1)
      #self.window.rowconfigure(1, weight=1)
      self.GameScreen = tk.Frame(self.window, background="black")
      self.InfoScreen = tk.Frame(self.window, background="black")
      self.GameScreen.grid(row=1, column=1, sticky="nsew")
      self.InfoScreen.grid(row=1, column=2, sticky="nsew")
      self.InfoScreen.rowconfigure(3,weight=1)
      self.InfoScreen.columnconfigure(1, weight=1)
      #info
      self.levelInfo = tk.Label(self.InfoScreen, text= "Level: 1", background="black", foreground="white", font=("Cascadia Code", 12))
      self.levelInfo.grid(row=1, column=1)
      self.pointInfo = tk.Label(self.InfoScreen, text= "Points: 0", background="black", foreground="white", font=("Cascadia Code", 12))
      self.pointInfo.grid(row=2, column=1)
      self.pointInfo = tk.Label(self.InfoScreen, text= "♡ ♡ ♡", background="black", foreground="white", font=("Cascadia Code", 12))
      self.pointInfo.grid(row=3, column=1)

      #hra
      self.spaceX = 20
      self.spaceY = 18
      self.Game = [None] * (self.spaceX * self.spaceY)
      self.GameObjects = [None] * (self.spaceX * self.spaceY)
      
      self.pocetNepratel = 0
      self.vlna = shared["vlna"]
      self.neprateleNaVlnu = self.vlna * 3
      self.zabitiNepratele = 0

      #nastaveni
      self.maxBulletTime = 500 + (shared["u_dostrel"] * 100)
      self.lives = 3 + shared["u_zivot"]
      self.poskozeni = 1 + shared["u_poskozeni"]

      x = 0
      y = 1
      for i in range(self.spaceX * self.spaceY):
         self.GameObjects[i] = tk.Label(self.GameScreen, text=".", background="black", foreground="white")
         x += 1
         self.GameObjects[i].grid(row=y, column=x)
         if x >= self.spaceX:
            x = 0
            y += 1
      self.Player = Player()
      self.ObjSpawnAt(self.Player, 9, 16)

   def update(self):
       self.s_input()
       self.s_screenUpdate()

       for i in self.Game:
           if i:
            i.Update(self)
      
      #vlny atd
       
       for i in range(self.neprateleNaVlnu - self.pocetNepratel):
          obj = Nepritel(self.vlna)
          if self.ObjSpawnAt(obj, randint(0,19), randint(0, 5)):
            self.pocetNepratel += 1
       
       if self.zabitiNepratele >= self.neprateleNaVlnu:
          shared["vlna"] += 1
          self.hra.LoadScene("Shop")






   def s_input(self):
      if self.input == "right":
         self.ObjMoveToRelative(self.Player, 1, 0)
      elif self.input == "left":
         self.ObjMoveToRelative(self.Player, -1, 0)
      elif self.input == "up":
         self.ObjMoveToRelative(self.Player, 0, -1)
      elif self.input == "down":
         self.ObjMoveToRelative(self.Player, 0, 1)

      if self.input == "shoot":
          newBullet = Strela(self.maxBulletTime)
          self.GameObjects.append(newBullet)
          self.ObjSpawnAt(newBullet, self.Player.x, self.Player.y - 1)
      self.input = None
   def s_screenUpdate(self):
      for i in range(self.spaceX * self.spaceY):
         if self.Game[i] == None:
            self.GameObjects[i].configure(text=".")
         elif self.Game[i].getType() == "Player":
            self.GameObjects[i].configure(text="P")
         elif self.Game[i].getType() == "Enemy":
            self.GameObjects[i].configure(text="E")
         elif self.Game[i].getType() == "Bullet":
            self.GameObjects[i].configure(text="B")
   def ObjMoveTo(self, obj : Object, x, y):
       if x >= self.spaceX or y >= self.spaceY or x < 0 or y < 0:
           return
       objPos = obj.y * self.spaceX + obj.x
       newPos = y * self.spaceX + x
       self.Game[objPos] = None
       self.Game[newPos] = obj
   def ObjSpawnAt(self, obj : Object, x, y, force = False):
      if x >= self.spaceX or y >= self.spaceY or x < 0 or y < 0:
       return
      pos = y * self.spaceX + x
      if self.Game[pos] and not force:
          return
      if self.Game[pos] and self.Game[pos].getType() == "Player":
          return
      obj.x = x
      obj.y = y
      self.Game[pos] = obj
      return True
   def ObjMoveToRelative(self, obj : Object, x, y, force = False):
      objPos = obj.y * self.spaceX + obj.x
      relPos = objPos + x
      relPos += y * self.spaceX
      if relPos < 0 or relPos >= (self.spaceX * self.spaceY):
       return

      if self.Game[relPos] and obj.getType() == "Bullet":
         if self.Game[relPos].getType() == "Player":
            self.ObjDestory(obj)
            self.lives -= 1
            return True
         
         if self.Game[relPos].getType() == "Enemy":
            self.ObjDestory(obj)
            self.Game[relPos].hit(self.poskozeni)
            if self.Game[relPos].lives <= 0:
               self.ObjDestory(self.Game[relPos])
               self.pocetNepratel -= 1
               self.zabitiNepratele += 1
               shared["body"] += 100
   
            return True


      if self.Game[relPos] and not force:
          return
      if self.Game[relPos] and self.Game[relPos].getType() == "Player":
          return
      
      self.Game[objPos] = None
      self.Game[relPos] = obj
      obj.x += x
      obj.y += y
      return True
   def ObjDestory(self, obj : Object):
       objPos = obj.y * self.spaceX + obj.x
       self.Game[objPos] = None


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

class ObchodScena(scena):
   def __init__(self, root, hra, nazev : str):
      scena.__init__(self, root, hra, nazev)
      #self.window.rowconfigure(5, weight=1)
      self.window.columnconfigure(1, weight=1)
      tk.Label(self.window, text= "Obchod", background="black", foreground="white", font=("Cascadia Code", 48)).grid(row=1, column=1, sticky="nsew")
      tk.Label(self.window, text= f"Body: {shared['body']}", background="black", foreground="white", font=("Cascadia Code", 18)).grid(row=2, column=1, sticky="nsew")
      tk.Label(self.window, text= "Pokracovat [Mezernik]", background="black", foreground="white", font=("Cascadia Code", 18)).grid(row=3, column=1, sticky="nsew")
      tk.Label(self.window, text= f"Vylepseni dostrelu ({(shared['u_dostrel'] + 1)*100}) [d]", background="black", foreground="white", font=("Cascadia Code", 18)).grid(row=4, column=1, sticky="nsew")
      tk.Label(self.window, text= f"Vylepseni poskozeni ({(shared['u_poskozeni'] + 1)*100}) [a]", background="black", foreground="white", font=("Cascadia Code", 18)).grid(row=5, column=1, sticky="nsew")
      tk.Label(self.window, text= f"Vylepseni zivotu ({(shared['u_zivot'] + 1)*100}) [w]", background="black", foreground="white", font=("Cascadia Code", 18)).grid(row=6, column=1, sticky="nsew")
      tk.Label(self.window, text= "Ukoncit hru [q]", background="black", foreground="white", font=("Cascadia Code", 18)).grid(row=7, column=1, sticky="nsew")
      self.wait = True
   def update(self):
      if self.wait == True:
         time.sleep(0.5)
         self.wait = False
         self.input = None
         return
      if self.input == "back":
        self.root.destroy()
      elif self.input == "shoot":
         self.hra.LoadScene("Game")
      elif self.input == "right":
         self.koupit("u_dostrel")
      elif self.input == "left":
         self.koupit("u_poskozeni")
      elif self.input == "up":
         self.koupit("u_zivot")
      self.input = None
   def koupit(self, upgrade):
      cena = ((shared[upgrade] * 2) + 1) * 100
      if shared["body"] < cena:
         return
      
      shared["body"] -= cena
      shared[upgrade] += 1
      self.hra.LoadScene("Shop")

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
     elif scene == "Shop":
        self.currentScene = ObchodScena(self.root, self, "Shop")


  def CaptureInput(self, inputStr : str):
      self.currentInput = inputStr
hra()
