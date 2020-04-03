import shlex
from core import Errors
import core.com as com

# La classe de la ligne de commande
class CommandLine():

  def __init__(self,**kwargs):
    self.funct = []
    self.quit = False
    self.cmdReturn = ""
    self.vars = {}

    self.__msgStart = kwargs.get("start","Cythan machine project by <discursif/>\nWrite 'help' for command list.")
    self.__msgWrgParam = kwargs.get("wrongParameter","Parameter $ muyst be $$")
    self.__msgUnknow = kwargs.get("unknow","Unknow command.\nWrite 'help' for command list.")
    self.__paramList = kwargs.get("parameterList",["True/False","some text","a number","a float"])
    self.__haveMsgError = kwargs.get("commandErrorFeedback",True)
    self.__msgArguments = kwargs.get("argumentsError","You don't have the right number of parameters")

    self.__cmdErrorFeedback = kwargs.get("commandErrorFeedback",True)

    self.activeSymbol = kwargs.get("activeSymbol","=> ")
  
  def setVars(self,kwargs):
    self.vars = kwargs

  def addFunction(self,caller = None,**topKwargs) -> "Methode de passage":
    def inner(funct) -> "retourne la nouvelle fonction":

      def newFunct(*arg,**kwargs) -> "New function":

        def convert(typeIn,element):
          if typeIn == bool:
            try: element = bool(element)
            except:raise AssertionError(self.__msgWrgParam.replace("$",element).replace("$$",self.__paramList[0]))
          elif typeIn == str:
            try: element = str(element)
            except:raise AssertionError(self.__msgWrgParam.replace("$",element).replace("$$",self.__paramList[1]))
          elif typeIn == int:
            try: element = int(element)
            except:raise AssertionError(self.__msgWrgParam.replace("$",element).replace("$$",self.__paramList[2]))
          elif typeIn == float:
            try: element = float(element)
            except: raise AssertionError(self.__msgWrgParam.replace("$",element).replace("$$",self.__paramList[3]))
          else:
            com.Out.warning("Argument type not in standard converting sytem:"+str(typeIn)+" to convert :"+element+", keeping as string")
          return element
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
          except IndexError:
            if isinstance(annot,tuple):
              new_args.append(annot[1])
              i+=1
              continue
            else: raise AssertionError(self.__msgArguments)
          if annot == "return" or annot == None:pass
          elif isinstance(annot,tuple):
            try:
              new_args.append(convert(annot[0],param))
            except AssertionError:
              new_args.append(annot[1])
          # Oblige d'avoir un argument
          else:new_args.append(convert(annot,param))
          i+=1
        return funct(*tuple(new_args),**kwargs) # Si tout est bon, on execute la fonction


      # Ajout au dictionnaire de la fonction
      newFunct.caller = caller # ajout du contexte self
      names = topKwargs.get("aliases",[])
      self.funct.append(newFunct)
      self.funct[self.funct.index(newFunct)].__name__ = funct.__annotations__.pop("return")
      self.funct[self.funct.index(newFunct)].__doc__ = funct.__doc__
      self.funct[self.funct.index(newFunct)].aliases = names
      
      com.Out.debug("Called for "+funct.__name__+", arguments is "+", ".join([i+":"+str(x) for i,x in funct.__annotations__.items()]))
      if names == []:com.Out.info("No alises found")
      if names == []:com.Out.info("Aliases = "+",".join(names))
      return newFunct # On retourne notre meilleure fonction.
    return inner

  # Commande principale, menu du terminal
  def menu(self):
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
    else:com.Out.debug("No print: non returning");


  # executer une commande
  def __command(self,execute):
    com.Out.debug("CMD:"+str(execute))
    if isinstance(execute,str):execute = shlex.split(execute)
    if execute == []: return None
    returning = None
    find = False
    for funct in self.funct:
      if execute[0] in [funct.__name__.split(" ")[0]]+funct.aliases:
        try:
          if funct.caller: com.Out.debug("function have caller");returning = funct(funct.caller,*execute[1:],**self.vars)
          else:com.Out.debug("function doesn't have caller");returning = funct(*execute[1:],**self.vars)
        except AssertionError as err:
          returning ="Argument Error:\n"+str(err)
        except Errors.BreakPointMet as err:
          returning ="Breakpoint met:\n"+str(err)
        except Errors.EndPoint as err:
          returning ="Machine ended:\n"+str(err)
        except Errors.CythanError as err:
          returning ="Cythan Error:\n"+str(err)
        except BaseException as err:
          returning = "Unhandle Error:\n"+str(err)+"\nIf this is not your fault, please type make an GItHub issue with the content of 'log read 50'"
        finally:
          find =True
    if not find:
      returning = self.__msgUnknow
      com.Out.error("Unfind command");
    if returning != None:com.Out.debug("RET:"+str(returning))
    return returning
