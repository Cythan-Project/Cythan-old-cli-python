import inspect
from time import gmtime, strftime

class Log():

    def __init__(self,**kwargs):
        self.__log_file = kwargs.get("log_file","core/com/log.txt")
        self.last = ""
        self.log_levels = kwargs.get("log_level",[])
        with open(self.__log_file,"a") as f:
            f.write("\n["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"]"+" Start\n")
        self.last = "\n["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"]"+" Start\n"
        
    
    def __out(self,message,log_type):
        stack = inspect.stack()
        modCaller = inspect.getmodule(stack[2][0])
        try:
            classCaller = str(stack[2][0].f_locals["self"].__class__)
        except KeyError:
            classCaller = ""
        if classCaller != "": classCaller +=" "
        methodCaller = stack[2][0].f_code.co_name
        log = log_type+" - ["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"] {"+str(modCaller.__name__)+"} "+str(classCaller)+str(methodCaller)+": "+str(message)
        if log_type in self.log_levels or "ALL" in self.log_levels:
            print(("["+log_type+"] "+str(methodCaller)+": "+str(message)).replace("\n","\\n"))
        with open(self.__log_file,"a") as f:
            f.write(log+"\n")
        self.last += log+"\n"

    def read(self,nbLines):
        f = open(self.__log_file,"r")
        ret = f.readlines()
        f.close()
        return ret[-nbLines:-1]
        

    def debug(self,message):self.__out(message,"DEBUG")
    def info(self,message):self.__out(message,"INFO")
    def test(self,message):self.__out(message,"TEST")
    def warning(self,message):self.__out(message,"WARNING")
    def error(self,message):self.__out(message,"ERROR")
    def custom(self,message,logName):self.__out(message,logName)


