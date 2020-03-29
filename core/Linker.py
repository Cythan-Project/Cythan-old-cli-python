from core.Cythan import CythanMachine
from core import Errors

import core.com as com

class CythanInstance():
  
  def __init__(self,data=[]):
    self.machine = CythanMachine(data)
    self.breakpoints = []



class CythanInstanceManager():

  def __init__(self):
    self.instances = []
  
  def addInstance(self,data=[]):
    self.instances.append(CythanInstance(data))
  
  def next(self,instanceNB):
    self.instances[instanceNB].turn(nbTurn)
  




class CythanModuleManager():

  def __init__(self):
    self.modules = []


com.Out.debug("Linker imported")