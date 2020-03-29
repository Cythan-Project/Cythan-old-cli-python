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
com.Out.debug("Setting up Compiler")
CompilerManager = BCLcompiler()

# O---------------
# |  Basic Cythan commands
# O---------------

@CommandLine.addFunction()
def nextgen(nbGen:(int,1),machineID:(int,0),**kwargs) -> "next [INT] [MACHINE_ID]":
  """Execute the Cythan Code of the machine.
  MACHINE_ID: empty for the first machine, precize the machine number"""
  for x in range(nbGen):
    try:
      InstanceManager.next(machineID)
    except Errors.BreakPointMet as err:
      return "Breakpoint met at next "+str(x)+":"+err
    except AssertionError:
      return "No Cythan Machine have ID:"+str(machineID)
  return "Execution done."

@CommandLine.addFunction()
def compileBCL(subcommand:str,arg1:str,arg2:(str,""),**kwargs) -> "compiler (compile <input_path> [output_name]|configure (reset|<element> <character>))":
  """Compile a BCL language to Cythan code.
  compiler compile <input_path> <output_name>:
    Compile a file at the <input_path> path written in BCL to Cythan language usable by the 'start' command.
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
def startCythan(name:str,**kwargs) -> "start <name>":
  """Start the Cythan machine on a program compiled in cythan place in the 'program' folder"""
  f = open("program/"+name+".cyt","r")
  d = f.read()
  f.close()
  data = [[int(y) for y in x.split(",")] for x in d.split(";")]
  CythanInstanceManager.addInstance(data=data)
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
  '''
  To quit propely the command manager
  '''
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
  '''
  Print the help for a command
  '''
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