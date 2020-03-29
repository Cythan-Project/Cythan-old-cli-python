import shlex

import core.com as com

# La classe de la ligne de commande
class CommandLine():

  def __init__(self,**kwargs):
    self.funct = []
    self.quit = False
    self.cmdReturn = ""
    self.vars = {}

    self.__msgStart = kwargs.get("start","Invite de commande par Cyprien Bourotte\nTapez 'help' pour la liste des commandes.")
    self.__msgWrgParam = kwargs.get("wrongParameter","Le parametre $ doit etre $$")
    self.__msgUnknow = kwargs.get("unknow","La commande est inconnue.\nTapez 'help' pour obtenir la liste des commandes")
    self.__paramList = kwargs.get("parameterList",["Vrai/Faux","du texte","un nombre","un float"])
    self.__haveMsgError = kwargs.get("commandErrorFeedback",True)
    self.__msgArguments = kwargs.get("argumentsError","Vous n'avez pas le bon nombre de paramètres.")

    self.__cmdErrorFeedback = kwargs.get("commandErrorFeedback",True)
    self.__debug = kwargs.get("debug",True)

    self.activeSymbol = kwargs.get("activeSymbol","=> ")
  
  def setVars(self,kwargs):
    self.vars = kwargs

  def addFunction(self,caller = None) -> "Methode de passage":
    def inner(funct) -> "retourne la nouvelle fonction":

      def newFunct(*arg,**kwargs) -> "Nouvelle fonction":
        # On rajoute le code de tester si les arguments sont bons
        new_args = []
        i = 0
        for annot in list(funct.__annotations__.values()):
          

          if annot == max:
            param = " ".join(list(arg)[i:])
            new_args.append(param)
            break
          try:
            param = arg[i]
          except:
            if isinstance(annot,tuple):
              try:
                if not isinstance(annot[0],arg[i]): param = annot[0]
                else:param = annot[1]
              except IndexError: param = annot[1]
            else: raise AssertionError(self.__msgArguments)
          if annot == "return": pass
          elif annot == None:
            pass
          
          # Oblige d'avoir un argument
          elif annot == bool:
            try: param = bool(param)
            except:raise AssertionError(self.__msgWrgParam.replace("$",param).replace("$$",self.__paramList[0]))
          elif annot == str:
            try: param = str(param)
            except:raise AssertionError(self.__msgWrgParam.replace("$",param).replace("$$",self.__paramList[1]))
          elif annot == int:
            try: param = int(param)
            except:raise AssertionError(self.__msgWrgParam.replace("$",param).replace("$$",self.__paramList[2]))
          elif annot == float:
            try: param = float(param)
            except: raise AssertionError(self.__msgWrgParam.replace("$",param).replace("$$",self.__paramList[3]))
          new_args.append(param)
          i+=1
        return funct(*tuple(new_args),**kwargs) # Si tout est bon, on execute la fonction


      # Ajout au dictionnaire de la fonction
      newFunct.caller = caller # ajout du contexte self
      self.funct.append(newFunct)
      self.funct[self.funct.index(newFunct)].__name__ = funct.__annotations__.pop("return")
      self.funct[self.funct.index(newFunct)].__doc__ = funct.__doc__
      
      if self.__debug: print("Called for "+funct.__name__+", arguments is "+", ".join([i+":"+str(x) for i,x in funct.__annotations__.items()]))
      return newFunct # On retourne notre meilleure fonction.
    return inner

  # Commande principale, menu du terminal
  def menu(self):
    if self.__debug: print("\n"*10)
    print(self.__msgStart)
    while not self.quit:
      commandes_raw = input(self.activeSymbol)
      #for x in commandes_raw.split("$"):
      #self.vars[commandes_raw.split("$")]
      # 
      self.execute(commandes_raw)

  def execute(self,commandes_raw):
    commandes = commandes_raw.split(";")
    for commande in commandes:
      trt_commande = shlex.split(commande)
      self.cmdReturn = self.__command(trt_commande)
    if self.cmdReturn != None: print(self.cmdReturn)


  # executer une commande
  def __command(self,execute):
    com.Out.debug("CMD:"+str(execute))
    if isinstance(execute,str):execute = shlex.split(execute)
    if execute == []: return None
    returning = None
    find = False
    for funct in self.funct:
      if funct.__name__.split(" ")[0] == execute[0]:
        try:
          if funct.caller: returning = funct(funct.caller,*execute[1:],**self.vars)
          else:returning = funct(*execute[1:],**self.vars)
        except AssertionError as err:
          returning ="Erreur d'argument:\n"+str(err)
        finally:
          find =True
    if not find:
      returning = self.__msgUnknow
    com.Out.debug("RET:"+str(returning))
    return returning
