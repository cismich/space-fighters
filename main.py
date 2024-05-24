from random import randint
import tkinter as tk

#pro uchovavani informaci ktere jsou dostupne vsude
# u_ je zkratka pro "upgrade"
shared = {
   "vlna" : 1,
   "body" : 0,
   "u_dostrel" : 0,
   "u_poskozeni" : 0,
   "u_zivot" : 0
}


#
#
#  hra > scena > window > objekty
#
#
# hra (classa definovana na konci programu) zachytava input a spravuje sceny
# scena - ruzne napr. Menu, hra, obchod. kazda obsahuje window
# window - je tk.Frame vsechno ve scene se na tomto okne nachazi, tohle umoznuje rychle smazat vsechno ve scene
# objekty - vsechny objekty ve scene

#vetsina class obsahuje funkci "update" ktera bezi kazdy snimek

#tato classa obsahuje zakladni funkce ktere by sceny meli mit
class scena:
   def __init__(self, root, hra, nazev : str):

       #reference na hru a tk.root 
       self.hra = hra
       self.root = root
       

       self.window = tk.Frame(self.root, background = "black")
       self.window.grid(row=1, column=1, sticky="nsew")
       
       
       #aktualni input 
       self.input = None

       self.nazev = nazev
   def __del__(self):
      self.unload()
   def unload(self):
       
       #smaze vsechny objekty ve scene
       self.window.destroy()
   def update(self):
       
       #pokud je z najeko duvodu vytvorena tato zakladni classa ve ktere se nic nenachazi, nacteme hlavni menu abychom se nezasekli

       hra.LoadScene(self.hra, "Menu")
       return
   def updateInput(self, gameInput : str):
       #hra nam touto funkci preda posledni input ktery si ulozime
       match gameInput:
              case "up":
                self.input = "up"
              case "down":
                self.input = "down"
              case "left":
                self.input = "left"
              case "right":
                self.input = "right"
              case "shoot":
                self.input = "shoot"
              case "e":
                self.input = "e"
              case "r":
                self.input = "r"
              case "t":
                self.input = "t"
              case "f":
                self.input = "f"
              case "back":
                self.input = "back"

#zakladni classa pro objekt, obsahuje pozici a funkci pro zjisteni typu objektu
class Object:
  def __init__(self):
     self.x = 0
     self.y = 0
  def getType(self):
     return "Object"

  def Update(self, hraScena):
      return

# classa pro hrace
# mozna by bylo lepsi do teto classy presunout pohyb hrace, ktery se ted zpracovava v hlavni scene
class Player(Object):
  def __init__(self):
     super().__init__()
  def getType(self):
     return "Player"

# classa pro nepritele
# zpracovava pohyb nepritel
class Nepritel(Object):
    def __init__(self, lives = 1):
        super().__init__()
        self.lives = lives

        # aby se nepratele nepohybovali moc rychle tak se mohou pohnout jenom kdyz pocitadlo dosahne 0
        # nepratele maji v kazde dalsi vlne vice zivotu takze by se meli postupne zrychlovat
        self.Movecounter = 10 - lives

    def getType(self):
        return "Enemy"
    def hit(self, poskozeni = 1):
       #pri zasahu nepritele tato funkce odecte zivot
       self.lives -= poskozeni
    
    def Update(self, hraScena):
      #pohneme se nahodnym smerem kdyz (nahoru nemuzeme) pocitadlo dosahne 0
      if self.Movecounter <= 0:
         self.Movecounter = 10 - self.lives
         hraScena.ObjMoveToRelative(self, randint(-1,1),randint(0,1))
      self.Movecounter -= 1

      #pokud prekrocime caru tak odecteme zivot hraci
      if self.y > 13:
         hraScena.lives -= 1
         hraScena.pocetNepratel -= 1
         hraScena.ObjDestory(self)

          
#classa pro strely
#kazda strela po urcitem case (da se prodlouzit vylepsenim) zmizi
class Strela(Object):
    def __init__(self, maxTime : int):
        super().__init__()
        self.time = 0
        self.maxBulletTime = maxTime

    def getType(self):
        return "Bullet"

    def Update(self, hraScena):
        #pokud se nemuzeme pohnout tak jsme (snad) na konci herniho pole a strelu muzeme smazat
        if not hraScena.ObjMoveToRelative(self, 0, -1):
            hraScena.ObjDestory(self)

        self.time += 100
        if self.time >= self.maxBulletTime:
            hraScena.ObjDestory(self)

#hlavni scena pro hru
class HraScena(scena):
   def __init__(self, root, hra, nazev : str):
      scena.__init__(self, root, hra, nazev)
      self.window.columnconfigure(1, weight=1)

      #scena je rozdelena na 2 poloviny, na leve strane je hra a na prave info
      self.GameScreen = tk.Frame(self.window, background="black")
      self.GameScreen.grid(row=1, column=1, sticky="nsew")

      self.InfoScreen = tk.Frame(self.window, background="black")
      self.InfoScreen.grid(row=1, column=2, sticky="nsew")
      self.InfoScreen.columnconfigure(1, weight=1)


      #info
      self.levelInfo = tk.Label(self.InfoScreen, text= f"Vlna: {shared['vlna']}", background="black", foreground="white", font=("Cascadia Code", 24))
      self.pointInfo = tk.Label(self.InfoScreen, text= f"Body: {shared['body']}", background="black", foreground="white", font=("Cascadia Code", 24))
      self.zivotInfo = tk.Label(self.InfoScreen, text= "♡ " * (shared['u_zivot'] + 3), background="black", foreground="white", font=("Cascadia Code", 24))

      self.levelInfo.grid(row=1, column=1)
      self.pointInfo.grid(row=2, column=1)
      self.zivotInfo.grid(row=3, column=1)
      
      #hra
      
      #herni pole je 20*18, spaceX (nejedna se o firmu Elona Muska) je velikost pole na ose X, a spaceY je velikost na ose y.
      self.spaceX = 20
      self.spaceY = 18
      
      #Game je seznam prazdnych polich a class napr. hrac, strela, nepritel
      self.Game = [None] * (self.spaceX * self.spaceY)

      #GameObjects se pozdeji naplni tk.Label objekty, slouzi jako "zobrazeni" listu Game
      #napr. kdyz je na Game[3] classa strely tak se text GameObjects[3] zmeni na "|" 
      self.GameObjects = [None] * (self.spaceX * self.spaceY)
      
      self.pocetNepratel = 0 #pocet nepratel ktere prave zijou
      self.vlna = shared["vlna"]
      self.neprateleNaVlnu = self.vlna * 3 
      self.zabitiNepratele = 0

      #upgrady
      self.maxBulletTime = 500 + (shared["u_dostrel"] * 100)
      self.poskozeni = 1 + shared["u_poskozeni"]

      #na zacatku vezmeme dokoupene zivoty a pridame je k tem co dostaneme na zacatku kazde vlny
      self.lives = 3 + shared["u_zivot"]
      shared["u_zivot"] = 0
      
      
      #zaplneni listu GameObjects
      x = 0
      y = 1
      for i in range(self.spaceX * self.spaceY):
         self.GameObjects[i] = tk.Label(self.GameScreen, text=".", background="black", foreground="white")
         x += 1
         self.GameObjects[i].grid(row=y, column=x)
         if x >= self.spaceX:
            x = 0
            y += 1
      
      #vytvorime hrace a spawneme ho do sceny
      self.Player = Player()
      self.ObjSpawnAt(self.Player, 9, 16)

   def update(self):
       
       self.s_input()
       self.s_screenUpdate()

       #aktualizujeme kazdy objekt ve scene
       for i in self.Game:
           if i:
            i.Update(self)
      
       #snazime se udrzet pocet nepratel ve scene 
       for i in range(self.neprateleNaVlnu - self.pocetNepratel):
          obj = Nepritel(self.vlna)
          if self.ObjSpawnAt(obj, randint(0,19), randint(0, 5)):
            self.pocetNepratel += 1
       
       #pokud porazime vsechny nepratele ve vlne tak muzeme pokracovat do obchodu
       if self.zabitiNepratele >= self.neprateleNaVlnu:
          shared["vlna"] += 1

          #pokud mame vice jak 3 zivoty (to znamena ze jsme nejake minule koupili a nepouzili) tak je vratime
          if self.lives > 3:
             shared["u_zivot"] = self.lives - 3
          self.hra.LoadScene("Shop")

       #aktualizace textu
       self.pointInfo.configure(text= f"Body: {shared['body']}")
       self.zivotInfo.configure(text= "♡ " * self.lives)

       #kdyz dojdou zivoty, tak koncime
       if self.lives <= 0:
          self.hra.LoadScene("Konec")






   def s_input(self):
      #pohyb hrace
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
          self.ObjSpawnAt(newBullet, self.Player.x, self.Player.y - 1)

      #aby se vicekrat neopakoval input tak ho na konci nastavime na prazdnou hodnotu
      self.input = None
   def s_screenUpdate(self):
      #zobrazovani hry

      for i in range(self.spaceX * self.spaceY):
         
         #podle toho co je na Game[i] tak aktualizujeme text na GameObjects[i]

         if self.Game[i] == None:

            #vytvari caru, kterou kdyz nepratele prekroci tak hrac prijde o 1 zivot
            if i > 14*19-7 and i < 14*19+14:
               self.GameObjects[i].configure(text="-")
            else:
               self.GameObjects[i].configure(text=" ")

         elif self.Game[i].getType() == "Player":
            self.GameObjects[i].configure(text="Δ")
         elif self.Game[i].getType() == "Enemy":
            self.GameObjects[i].configure(text="∇")
         elif self.Game[i].getType() == "Bullet":
            self.GameObjects[i].configure(text="|")
   
   def ObjMoveTo(self, obj : Object, x, y):
       #posouva objekt na urcitou pozici x,y (moc nepouzivane)

       if x >= self.spaceX or y >= self.spaceY or x < 0 or y < 0:
           return
       objPos = obj.y * self.spaceX + obj.x
       newPos = y * self.spaceX + x
       self.Game[objPos] = None
       self.Game[newPos] = obj
   def ObjSpawnAt(self, obj : Object, x, y, force = False):
      #vytvori objekt na x,y

      #kontrola jestli se nachazime na hraci plose
      if x >= self.spaceX or y >= self.spaceY or x < 0 or y < 0:
       return
      
      pos = y * self.spaceX + x
      
      #strela muze poskozovat nepritele
      if self.Game[pos] and obj.getType() == "Bullet":
         if self.Game[pos].getType() == "Enemy":
            self.Game[pos].hit(self.poskozeni)
            if self.Game[pos].lives <= 0:
               self.ObjDestory(self.Game[pos])
               self.pocetNepratel -= 1
               self.zabitiNepratele += 1
               shared["body"] += 100
   
            return True
      
      #pokud je pole obsazene a neni dulezite ze se objekt nespawne
      if self.Game[pos] and not force:
          return
      
      #nikdy nemuzeme prepsat pole na kterem je hrac
      if self.Game[pos] and self.Game[pos].getType() == "Player":
          return
      
      obj.x = x
      obj.y = y
      self.Game[pos] = obj
      return True
   def ObjMoveToRelative(self, obj : Object, x, y, force = False):
      #posune objekt o x, y
      #napr. kdyz x = 1 tak se objekt posune o 1 pole doprava

      #vypocet nove pozice
      objPos = obj.y * self.spaceX + obj.x
      relPos = objPos + x
      relPos += y * self.spaceX

      #kontrola jestli je nova pozice na hraci plose
      if relPos < 0 or relPos >= (self.spaceX * self.spaceY):
       return
      
      #kontrola abychom nemohli prochazet steny hraciho pole na ose x
      if x < 0 and (obj.x % self.spaceX) <1:
         return
      
      #kontrola abychom nemohli prochazet steny hraciho pole na ose y
      if x > 0 and (obj.x % self.spaceX) > (self.spaceX - 2):
         return

      #strela muze poskozovat nepritele
      if self.Game[relPos] and obj.getType() == "Bullet":
         
         if self.Game[relPos].getType() == "Enemy":
            self.ObjDestory(obj)
            self.Game[relPos].hit(self.poskozeni)
            if self.Game[relPos].lives <= 0:
               self.ObjDestory(self.Game[relPos])
               self.pocetNepratel -= 1
               self.zabitiNepratele += 1
               shared["body"] += 100
   
            return True

      #pokud je pole obsazene a neni dulezite ze se objekt posune
      if self.Game[relPos] and not force:
          return
      
      #nikdy nemuzeme prepsat pole na kterem je hrac
      if self.Game[relPos] and self.Game[relPos].getType() == "Player":
          return
      
      self.Game[objPos] = None
      self.Game[relPos] = obj
      obj.x += x
      obj.y += y
      return True
   def ObjDestory(self, obj : Object):
       #smaze objekt
       objPos = obj.y * self.spaceX + obj.x
       self.Game[objPos] = None


#scena hlavniho menu
#pouze zobrazuje info a umoznuje zacit hru a nebo ji ukoncit 
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
        self.root.destroy() #pri spusteni teto funkce vznikne chyba a program spadne, to je ale uplne jedno protoze ho stejne chceme vypnout :) takze to vlastne funguje presne podle planu
      elif self.input == "shoot":
         self.hra.LoadScene("Game")

#scena obchodu
#slouzi pro nakup vylepseni
class ObchodScena(scena):
   def __init__(self, root, hra, nazev : str):
      scena.__init__(self, root, hra, nazev)
      self.window.columnconfigure(1, weight=1)

      #texty obchodu

      tk.Label(self.window, text= "Obchod", background="black", foreground="white", font=("Cascadia Code", 48)).grid(row=1, column=1, sticky="nsew")

      self.body = tk.Label(self.window, text= f"Body: {shared['body']}", background="black", foreground="white", font=("Cascadia Code", 18))
      self.body.grid(row=2, column=1, sticky="nsew")

      tk.Label(self.window, text= "Pokracovat [e]", background="black", foreground="white", font=("Cascadia Code", 18)).grid(row=3, column=1, sticky="nsew")

      self.dostrel = tk.Label(self.window, text= f"Vylepseni dostrelu ({(shared['u_dostrel'] + 1)*100}) [r]", background="black", foreground="white", font=("Cascadia Code", 18))
      self.dostrel.grid(row=4, column=1, sticky="nsew")

      self.poskozeni = tk.Label(self.window, text= f"Vylepseni poskozeni ({(shared['u_poskozeni'] + 1)*100}) [t]", background="black", foreground="white", font=("Cascadia Code", 18))
      self.poskozeni.grid(row=5, column=1, sticky="nsew")

      self.zivot = tk.Label(self.window, text= f"Koupit zivot navic (100) [f]", background="black", foreground="white", font=("Cascadia Code", 18))
      self.zivot.grid(row=6, column=1, sticky="nsew")

      tk.Label(self.window, text= "Ukoncit hru [q]", background="black", foreground="white", font=("Cascadia Code", 18)).grid(row=7, column=1, sticky="nsew")
      self.wait = True
   def update(self):
      #pro nakup pouzivam klavesy e, r, t, f
      #protoze kdyz jsem zkousel w, a, s, d tak se stavalo ze se neco koupilo samo protoze jsem mel klavesu stale zmacknutou z toho jak jsem hral


      if self.input == "back":
        self.root.destroy()
      elif self.input == "e":
         self.hra.LoadScene("Game")
      elif self.input == "r":
         self.koupit("u_dostrel")
      elif self.input == "t":
         self.koupit("u_poskozeni")
      elif self.input == "f":
         self.koupit("u_zivot")
      self.input = None

   def koupit(self, upgrade):
      if upgrade == 'u_zivot':
         cena = 100
      else:
         cena = (shared[upgrade] + 1) * 100
      if shared["body"] < cena:
         return
      
      shared["body"] -= cena
      shared[upgrade] += 1

      #misto toho abych aktualizoval texty tak proste znovu nactu obchod.
      #hrac si toho ani nevsimne
      self.hra.LoadScene("Shop")
      
#scena prohry
#zobrazuje finalni skore a moznost zacit znovu
class KonecScena(scena):
   def __init__(self, root, hra, nazev : str):
      scena.__init__(self, root, hra, nazev)
      self.window.columnconfigure(1, weight=1)
      
      #texty

      tk.Label(self.window, text= "Prohra :(", background="black", foreground="white", font=("Cascadia Code", 48)).grid(row=1, column=1, sticky="nsew")

      self.body = tk.Label(self.window, text= f"Skore: {shared['vlna'] * (shared['body'] )}", background="black", foreground="white", font=("Cascadia Code", 18))
      self.body.grid(row=2, column=1, sticky="nsew")

      tk.Label(self.window, text= "Dalsi pokus [e]", background="black", foreground="white", font=("Cascadia Code", 18)).grid(row=3, column=1, sticky="nsew")
      tk.Label(self.window, text= "ukoncit [q]", background="black", foreground="white", font=("Cascadia Code", 18)).grid(row=4, column=1, sticky="nsew")
   def update(self):
      if self.input == "back":
        self.root.destroy()
      elif self.input == "e":
         #pred nactenim hlavni sceny musime resetovat tyto hodnoty, jinak bychom stale pokracovali ve stejne hre

         shared["body"] = 0
         shared["u_dostrel"] = 0
         shared["u_poskozeni"] = 0
         shared["u_zivot"] = 0
         shared["vlna"] = 1
         self.hra.LoadScene("Game")


#hlavni classa
class hra:
  def __init__(self):
      
      #vytvoreni okna
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
      self.root.bind("e", lambda e : self.CaptureInput("e"))
      self.root.bind("r", lambda e : self.CaptureInput("r"))
      self.root.bind("t", lambda e : self.CaptureInput("t"))
      self.root.bind("f", lambda e : self.CaptureInput("f"))
      self.root.bind("q", lambda e : self.CaptureInput("back"))
      self.root.bind("<space>", lambda e : self.CaptureInput("shoot"))
      self.currentInput : str = None

      #nastavime aby se za 1000ms (nevim jestli je potreba 1000ms ale radsi pockam aby se vsechno stihlo nacist) spustila funkce update a spustime tkinter.
      self.root.after(1000, self.update)

      self.root.mainloop()
  def update(self):
      
      #update hry postupuje v tomto poradi
      
      self.inputUpdate() # zachytava input

      self.GameUpdate() # updatuje hru a vsecho
      
      self.WindowUpdate() # planoval jsem ze tato funkce bude delat neco dulezitejsiho ale zatim pouze nacte hlavni menu
      
      self.root.after(100, self.update)

  def inputUpdate(self):
      #pokud mame nejaky input predame ho funkci v aktualni scene
      if self.currentInput:
         self.currentScene.updateInput(self.currentInput)
      self.currentInput = None
      return
  
  def GameUpdate(self):
      #aktualizujeme aktualni scenu
      if self.currentScene:
         self.currentScene.update()
      return
  def WindowUpdate(self):
      #zatim pouze vytvari hlavni menu
      if not self.currentScene:
          self.currentScene = scena(self.root, self, "Main")

  def LoadScene(self, scene : str):
     #nacte vyzadanou scenu podle jmena, aktualni scena se sama smaze protoze implementuje __del__
     self.currentScene = None
     if scene == "Menu":
       self.currentScene = MenuScena(self.root, self, "Menu")
     elif scene == "Game":
        self.currentScene = HraScena(self.root, self, "Game")
     elif scene == "Shop":
        self.currentScene = ObchodScena(self.root, self, "Shop")
     elif scene == "Konec":
        self.currentScene = KonecScena(self.root, self, "Shop")


  def CaptureInput(self, inputStr : str):
      #zachytavani inputu, tato funkce je spoustena tkinterem protoze jsou klavesy na ni napojeny
      self.currentInput = inputStr






#Zacne hru
hra()
