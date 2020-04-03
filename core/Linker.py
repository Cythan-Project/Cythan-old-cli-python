from core.Cythan import CythanMachine
from core import Errors

import core.com as com

class CythanInstance():
  
  def __init__(self,data=[]):
    self.machine = CythanMachine(data)
    self.breakpoints = []
    self.modules = []
  
  def execute(self,nb):
    print(nb)
    for x in range(nb):
      self.machine.turn(1)
      for x in self.breakpoints:
        if len(x) == 3 and self.machine.data[x[1]][x[2]] == x[0]: self.breakpoints.remove(x);raise Errors.BreakPointMet("At position "+str(x[1])+":"+str(x[2])+" for value "+str(x[0]))
        if len(x) == 2 and self.machine.negdata[-x[1]] == x[0]: self.breakpoints.remove(x);raise Errors.BreakPointMet("At position "+str(x[1]))


  


class CythanInstanceManager():

  def __init__(self):
    self.instances = {}
  
  def addInstance(self,name,data=[]):
    self.instances[name] = CythanInstance(data)
  
  def advance(self,instanceName,number):
    self.instances[instanceName].execute(number)

  def addBreak(self,machineName,value,position,subPosition=None):
    try:
      if (position >= 0 and position >= len(self.instances[machineName].machine.data)) or (position < 0 and position <= -len(self.instances[machineName].machine.negdata)): raise AssertionError("Invalid position, program shorter than asked")
      if subPosition != None and position < 0: raise AssertionError("Negative position doesn't have a second integers")
      if subPosition == None:
        if [value,position] in self.instances[machineName].breakpoints: self.instances[machineName].breakpoints.remove([value,position]);return False
        else:self.instances[machineName].breakpoints.append([value,position]);return True
      else:
        if [value,position,subPosition] in self.instances[machineName].breakpoints: self.instances[machineName].breakpoints.remove([value,position,subPosition]);return False
        else:self.instances[machineName].breakpoints.append([value,position,subPosition]);return True
    except KeyError:
      raise AssertionError()



class CythanModuleManager():

  def __init__(self):
    self.modules = []


com.Out.debug("Linker imported")