from core.Cythan import CythanMachine
from core.Linker import CythanInstanceManager, CythanModuleManager
from core.compiler import BCLcompiler
from core import Errors

import core.com as com

from random import randint, sample

import include.commandLineGenerator

com.Out.debug("Setting up Command")
CommandLine = include.commandLineGenerator.CommandLine()
com.Out.debug("Setting up Linker")
InstanceManager = CythanInstanceManager()
ModuleManager = CythanModuleManager()



# O---------------
# |  Basic Cythan commands
# O---------------

@CommandLine.addFunction()
def nextgen(nbGen:(int,1),machineID:(int,0),**kwargs) -> "next [INT] [MACHINE_ID]":
  """Yes"""
  for x in range(nbGen):
    try:
      InstanceManager.next(machineID)
    except Errors.BreakPointMet as err:
      return "Breakpoint met at next "+str(x)+":"+err
    except AssertionError:
      return "No Cythan Machine have ID:"+str(machineID)
  return "Execution done."


@CommandLine.addFunction()
def config(machineID:(int,0),configs:max,**kwargs) -> "configure [MACHINE_ID] [*KWARGS]":
  """Yes"""
  try:
    InstanceManager.configure(machineID,configs)
  except AssertionError as err:
    return "Configuration failed :"+err
  return "Configuration done."


@CommandLine.addFunction()
def infos(machineID:(int,0),**kwargs) -> "infos [MACHINE_ID] [DATA_START] [NUMBER_OF_BYTE]":
  """Yes"""
  return 'Not yet implemanted'


# O---------------
# |  General Commands
# O---------------

@CommandLine.addFunction()
def logs(command:str,param:(int,10),**kwargs) -> "logs (read [COUNT]|setlevel [VWXYZ])":
  """Yes"""
  if command == "read":
    return "no u"
  elif command == "setlevel":
    return "no u"
  else: raise AssertionError("logs "+command+" is not defined.")




@CommandLine.addFunction()
def quit(**kwargs) -> "quit":
  '''
  Pour quitter l'invite de commande.
  '''
  CommandLine.quit = True
  return "Bye !"

@CommandLine.addFunction()
def clear(**kwargs) -> "clear":
  '''
  Efface l'écran
  '''
  print("\n"*100)

@CommandLine.addFunction()
def help(info:(str,""),**kwargs) -> "help [command]":
  '''
  Affiche l'aide d'une commande
  '''
  if info == "": return "Liste des fonctions :\n\n"+"\n".join([fct.__name__ for fct in CommandLine.funct])+"\n\nTapez 'help COMMANDE' pour plus d'informations sur une commande en particulier.\nTapez 'help cmd' pour les informations d'utillisation de la ligne de commandes."

  for funct in CommandLine.funct:
    if funct.__name__.split(" ")[0] == info:return "AIDE pour "+funct.__name__.split(" ")[0]+":\nSyntaxe: "+funct.__name__+"\n"+"\n"+str(funct.__doc__)
  if info == "cmd": return """
Vous pouvez aussi executer plusieurs commandes à la suite en utillisant le séparateur ';'.
De cette manière, vous pouvez les combiner.
Celement le retour de la dernière commande est affiché.

Exemple:
help;grab echo : renverra seulement la ligne de l'aide sur la commande echo.

  """
  return "Commande inconnue.\nTapez 'help' pour la liste des commandes.\nTapez 'help cmd' pour les informations d'utillisation de la ligne de commandes."


com.Out.info("Launching Commands menu")
if __name__ == '__main__' :
  CommandLine.menu()