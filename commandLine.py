from core.Cythan import CythanMachine
from core.Linker import CythanInstanceManager, CythanModuleManager
from core.compiler import BCLcompiler
from core import Errors

import core.com as com

import include.commandLineGenerator


import os
from random import randint, sample

com.Out.debug("Setting up Command")
CommandLine = include.commandLineGenerator.CommandLine(debug=False)
com.Out.debug("Setting up Linker")
InstanceManager = CythanInstanceManager()
ModuleManager = CythanModuleManager()
com.Out.debug("Setting up Compiler")
CompilerManager = BCLcompiler()

# O---------------
# |  Basic Cythan commands
# O---------------

# To add:
# set X to Y
# read X
# follow X (print for every next)

# to do:
# simplified next to n and break to b and compile to c (shortcut)
# log command
# log errors + print position in debug mode

@CommandLine.addFunction()
def nextgen(machineName:str,nbGen:(int,1),**kwargs) -> "next <MACHINE_NAME> [INT]":
  """Execute the Cythan Code of the machine."""
  try:
    InstanceManager.advance(machineName,nbGen)
  except Errors.BreakPointMet as err:
    return "Breakpoint met at next "+str(x)+":"+err
  except KeyError:
    return AssertionError("No Cythan Machine have name: '"+str(machineName)+"'")
  return "Execution done."

@CommandLine.addFunction()
def debug(machineName:str,**kwargs) -> "debug <MACHINE_NAME>":
  """Print information about the machine <MACHINE_NAME>"""
  try:
    def section(name,dictio):
      returning = "-"*60+"\n"+name+"\n"+"-"*60+"\n"
      for x,y in dictio.items(): returning += x+":"+str(y)+"\n"
      return returning
    data = InstanceManager.instances[machineName].machine.data
    negdata = InstanceManager.instances[machineName].machine.negdata
    bp = InstanceManager.instances[machineName].breakpoints
    mod = InstanceManager.instances[machineName].modules
    printable = "DEBUGS INFOS :\n"
    printable += section("DATA",{"pointer":data[0][0],"adding unit":data[0][1],"positive length":len(data),"negative length":len(negdata)})
    if data[0][0] >=0: printable += "pointed:"+str(data[data[0][0]])+"\n"
    else: printable += "pointed:"+str(negdata[-data[0][0]])
    printable += section("BREAKPOINTS",{"value = "+str(x[0]):"position = "+str(x[1]) for x in bp})
    printable += section("MODULES",{})
    printable += "Module manager is still in devellopement !"+"\n"
    return printable
    
  except KeyError:
    return AssertionError("No Cythan Machine have name: '"+str(machineName)+"'")
  return "Execution done."

@CommandLine.addFunction()
def listCythan(typeToFind:str,**kwargs) -> "list (machine|program)":
  """ - 'list machine' list all the loaded machine.
 - 'list program' list all the compiled program in 'program' folder.
Use the 'debug' command for more informations"""
  if typeToFind == "machine":
    return "list of machines:\n - "+"\n - ".join(InstanceManager.instances.keys())
  elif typeToFind == "program":
    return "list of programs:\n - "+"\n - ".join([ x for x in os.listdir("program/") if x.split(".")[-1] =="cyt"])
  raise AssertionError("Second Argument must be 'machine' or 'program'")


@CommandLine.addFunction()
def addBreak(machineName:str,value:int,position:int,subPosition:(int,0),**kwargs) -> "break <MACHINE_NAME> <VALUE> <MEMORY_POSITION> [0|1]":
  """Add a breakpoint to the machine of the program called <MACHINE_NAME>.
If no memory position is set, it will take data[0][0] (pointer position).
Break will stop the machine once the memory at MEMORY_POSITION is <VALUE>.
You can precise for positive number if it is on the first or second memory cell.
Exemple:
 - 'break machine 20' will stop once the pointer position get to 20
 - 'break machine -5 3' will stop once -5 is in the 3:0 position
 - 'break machine -7 75 1' will stop once -7 is in the 75:1 position
"""
  if position < 0:isneg = True
  else:isneg = False
  try:
    if isneg:InstanceManager.addBreak(machineName,value,position)
    else:InstanceManager.addBreak(machineName,value,position,subPosition)
  except KeyError:
    return AssertionError("No Cythan Machine have name: '"+str(machineID)+"'")
  return "Breakpoint added to "+machineName+". It will activate when value "+str(value)+" will be in "+str(position)+":"+str(subPosition)



@CommandLine.addFunction()
def compileBCL(subcommand:str,arg1:str,arg2:(str,""),**kwargs) -> "compiler (compile <input_path> [output_name]|configure (reset|<element> <character>))":
  """Compile a BCL language to Cythan code.
  compiler compile <input_path> <output_name>:
    Compile a file at the <input_path> path (from main.py) written in BCL to Cythan language usable by the 'start' command.
    The output file will be at program/<output_name> in the cythan project.
    By default it is "[input_file_name].cyt". It will earse if already exist.
    BCL language syntax can be found in the cythan github page README
  configure (reset|<element> <character>):
    Setup the differtents character mapping to others syntax element.
    Reset reset the compiler."""
  if subcommand == "compile":
    com.Out.debug("loading BCL file at: '"+arg1)
    f = open(arg1,"r")
    content = f.read()
    f.close()
    cycode = CompilerManager.CYcompile(content)
    if arg2 == "": arg2 = ".".join(arg1.split("/")[-1].split("\\")[-1].split(".")[:-1])
    com.Out.debug("saving cyt at: '"+"program/"+arg2+".cyt'")
    f = open("program/"+arg2+".cyt","w")
    f.write(";".join([str(x[0])+","+str(x[1]) for x in cycode]))
    f.close()
    return "Compiled succesfully at '"+"program/"+arg2+".cyt'"
  elif subcommand == "configure":
    if arg1 == "reset": CompilerManager = BCLcompiler()
    elif arg1 == "basicBackLine": CompilerManager.basicBackLine = arg2
    elif arg1 == "basicSeperator":CompilerManager.basicSeperator = arg2
    elif arg1 == "variableEntry":CompilerManager.variableEntry = arg2
    elif arg1 == "variableEnd":CompilerManager.variableEnd = arg2
    elif arg1 == "fonctionArgEntry":CompilerManager.fonctionParaEntry = arg2
    elif arg1 == "fonctionArgEnd":CompilerManager.fonctionParaEnd = arg2
    elif arg1 == "actualPos":CompilerManager.actualPos = arg2
    elif arg1 == "definition":CompilerManager.definition = arg2
    elif arg1 == "comment":CompilerManager.commentaire = arg2
    elif arg1 == "mark":CompilerManager.mark = arg2
    else: return AssertionError("Syntax Error : second argument must be one in the list:\nreset,basicBackLine,basicSeperator,variableEntry,variableEnd,fonctionArgEntry,actualPos,definition,comment,mark")
  else: return AssertionError("Syntax Error : first argument must be 'compile' or 'configure'")


@CommandLine.addFunction()
def loadCythan(name:str,**kwargs) -> "load <fileName>":
  """Load the Cythan machine on a program compiled in cythan place in the 'program' folder.
The name dosn't count the extention.
Exemple: 'load myprog' will get the file at 'program/myprog.cyt'"""
  try:
    f = open("program/"+name+".cyt","r")
  except FileNotFoundError:
    return AssertionError("Program not found at: 'program/"+name+".cyt'")
  d = f.read()
  f.close()
  data = [[int(y) for y in x.split(",")] for x in d.split(";")]
  try:
    InstanceManager.addInstance(name,data=data)
  except KeyError:
    raise AssertionError("No machine called "+name)
  return "done"





# O---------------
# |  General Commands
# O---------------

@CommandLine.addFunction()
def logs(command:str,param:(str,None),**kwargs) -> "logs (read [COUNT]|setlevel [NAME])":
  """Setup logs informations.
 - Use logs read to print the log file.
Indicate the number of line. -1 for the entire file. Default is 20
 - Use logs setlevels to set you're console debuging logs levels.
In the order : DEBUG, INFO, TEST, WARNING, ERRORS. You can use custom log type name. Default is ["INFO","TEST","WARNING","ERROR"].
"""
  if command == "read":
    if param == None:param = 20
    else: 
      try:
        param = int(param)
      except ValueError:
        raise AssertionError("logs read [COUNT], Count must be a integrer")
    return "".join(com.Out.read(param))
  elif command == "setlevel":
    if param == None:
      com.Out.log_levels = ["INFO","TEST","WARNING","ERROR"]
      return 'Parameter reset to default.'
    if param.upper() in com.Out.log_levels:
      com.Out.log_levels.remove(param)
      return "You may not see "+param.upper()+" logs."
    else:
      com.Out.log_levels.append(param.upper())
      return "You can now see "+param.upper()+" logs."
  else: raise AssertionError("logs "+command+" is not defined.")




@CommandLine.addFunction()
def quit(**kwargs) -> "quit":
  '''To quit propely the command manager'''
  CommandLine.quit = True
  return "Bye !"

@CommandLine.addFunction()
def clear(**kwargs) -> "clear":
  '''
  Clear the screen
  '''
  print("\n"*100)

@CommandLine.addFunction()
def help(info:(str,""),**kwargs) -> "help [command]":
  '''Print the help for a command'''
  if info == "": return "Command list :\n\n"+"\n".join([fct.__name__ for fct in CommandLine.funct])+"\n\nWrite 'help COMMAND' for more information about a command.\nWrite 'help cmd' for more information about the command line."

  for funct in CommandLine.funct:
    if funct.__name__.split(" ")[0] == info:return "AIDE pour "+funct.__name__.split(" ")[0]+":\nSyntaxe: "+funct.__name__+"\n"+"\n"+str(funct.__doc__)
  if info == "cmd": return """
You can execute multiples command withe the character ';.

Exemple:
help;grab echo : show only the help for the echo command.

  """
  return "Unknow command.\nWrite 'help' for command list.\nWrite 'help cmd' for more information about the command line."


com.Out.info("Launching Commands menu")
if __name__ == '__main__' :
  CommandLine.menu()