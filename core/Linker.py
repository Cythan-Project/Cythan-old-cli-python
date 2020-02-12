from core.Cythan import CythanMachine
from core import Errors

import core.com as com


class CythanInstanceManager():

  def __init__(self):
    self.instances = []


class CythanModuleManager():

  def __init__(self):
    self.modules = []


com.Out.debug("Linker imported")