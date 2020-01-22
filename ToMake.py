class CythanMachine():

  def __init__(self, data,**kwargs):

    self.data = data
    negDataSize = kwargs.get('negDataSize', 100)
    self.data += [1,1]*kwargs.get('dataAppend', 20)
    self.negdata = [-1]*negDataSize
    self.printlevel = kwargs.get('printLevel', 1)
    self.Following = kwargs.get('follow', [])
    Execute = kwargs.get('execute', True)
    self.exeception = None
    if Execute: self.execute()

  def execute(self):
    self.x = 1
    if self.printlevel>2:print("\n-----Next iteration "+str(self.x)+" -----")
    while self.exeception == None:
      self.x+=1
      returning = self.turn(1)
      if self.printlevel>2 and returning == None:print("\n-----Next iteration "+str(self.x)+" -----")
    print("["+str(returning)+"] "+self.exeception[0]+"\n"+self.exeception[1])


  def turn(self, nb):

    def combine(x,y):
      if x[0] == -1:r1=y[0]
      else:r1=x[0]
      if x[1] == -1:r2=y[1]
      else:r2=x[1]
      return [r1,r2]

    for _ in range(nb):
      try:PP = self.data[0][0]
      except:self.exeception = ["DATA","data[0][0] is not reachable"];return "ERROR"
      try:PPP = self.data[PP]
      except:self.exeception = ["DATA","PPP: data["+str(PP)+"] is not reachable"];return "ERROR"
      try:
        if PPP[0] == -1: dataToSet = [-1,-1]
        elif PPP[1] == -1:self.exeception = ["END","endcode: "+str(PPP[0])]; return "END"
      except:self.exeception = ["Hardware","PPP have a -1 rule problem."];return "ERROR"

      try:
        if PPP[0] >=0:dataToSet = self.data[PPP[0]]
        else: dataToSet = [self.negdata[PPP[0]*-1],self.negdata[PPP[0]*-1-1]]
      except:self.exeception = ["DATA","dataToSet: data["+str(PPP[0])+"] is not reachable"];return  "ERROR"

      try:
        if PPP[1] >=0:dataToEarse = self.data[PPP[1]]
        else:dataToEarse= [self.negdata[PPP[1]*-1],self.negdata[PPP[1]*-1-1]]
      except:self.exeception = ["DATA","dataToEarse: data["+str(PPP[1])+"] is not reachable"];return "ERROR"

      try: finaldata = combine(dataToSet, dataToEarse)
      except:self.exeception = ["COMBINE","finaldata: "+str(dataToSet)+" & "+str(dataToEarse)+" Have failed to combined."];return "ERROR"

      try:
        self.data[0][0] += self.data[0][1]
      except:self.exeception = ["ADD","Position of pointer can not be add: "+str(self.data[0])];return "ERROR"

      try:
        if PPP[1] >=0: self.data[PPP[1]] = finaldata
        else: self.negdata[-1*PPP[1]] = finaldata[0];self.negdata[-1*PPP[1]-1] = finaldata[1]
      except:self.exeception = ["SET","finaldata: module "+str(PPP)+" & "+str(finaldata)+" have failed to be set."];return "ERROR"

      if self.printlevel >2:print("Iteration: "+str(self.x)+", Pointer: "+str(PP)+", Execute: "+str(PPP)+", First case: "+str(dataToSet)+", Second: "+str(dataToEarse)+", FinalData:"+str(finaldata)+";")
      if len(self.Following)>0:
        FollowPrinting = "Follow: "
        for x in self.Following:
          try:
            FollowPrinting+=str(self.data[x][0])+":"+str(self.data[x][1])+", "
          except:
            self.exeception = ["FOLLOW","Could not print followed case: "+str(x)];return "ERROR"
        print(FollowPrinting[:-2])

class CythanCodeGenerator(): # FINI !

  def __init__(self,**kwargs):
    self.basicBackLine = kwargs.get('basicBackLine', ";")
    self.basicSeperator = kwargs.get('basicSeperator', ",")
    self.variableEntry = kwargs.get('variableEntry', "{")
    self.variableEnd = kwargs.get('variableEnd', "}")
    self.fonctionParaEntry = kwargs.get('fonctionParaEntry', "(")
    self.fonctionParaEnd = kwargs.get('fonctionParaEnd', ")") # inutile
    self.actualPos = kwargs.get('actualPos', "~")
    self.definition = kwargs.get('definition', "=")
    self.commentaire = kwargs.get('commentaire', "#")
    self.mark = kwargs.get('mark', ":")
    

  def Encode(self,content):
    Var=[];VarM=[];Pos=[];Ct = content
    CtMF = content.replace("\n","").replace(" ","")
    position = 0;Ct2 = "";avant = "";module = "";modules = []
    InVar = False;InVarM = False;InCom = False
    for i, char in enumerate(CtMF):
      if char == self.commentaire:
        InCom = not InCom
        continue
      if not InCom:
        avant+=char
        if char == self.mark:
          Pos.append([avant[:-1],position]);avant = ""
        elif char == self.definition and CtMF[i+1] == self.variableEntry: InVarM = True
        elif char == self.definition:InVar = True
        elif char == self.variableEnd and InVarM:
          VarM.append([(module+avant).split(self.definition)[0],(module+avant).split(self.definition)[1][1:-1]])
          InVarM = False;avant = ""; module = ""
        elif char == self.basicBackLine and not InVarM:
          if InVar:
            Var.append([(module+avant[:-1]).split(self.definition)[0],(module+avant[:-1]).split(self.definition)[1]])
            InVar = False
          else:
            modules.append(module+avant[:-1])
            position +=1
          module = "";avant = ""
        if char == self.basicSeperator and not InVarM:
          module += avant;avant = ""
    endModulesList = []
    Fct = []
    for x in VarM:
      if x[0].find(self.fonctionParaEntry) >0:
        Fct.append([x[0].split(self.fonctionParaEntry)[0],x[0].split(self.fonctionParaEntry)[1][:-1].split(self.basicSeperator),x[1]])
        VarM.remove(x)
    index = 0
    for module in modules:
      Mul = False
      for y in Pos:module = module.replace(y[0],str(y[1]))
      for y in Var:module = module.replace(y[0],y[1])
      for y in VarM:
        if module.find(y[0]) > -1:Mul = True;module = module.replace(y[0],y[1])
      for y in Fct:
        if module.find(y[0]) > -1:
          Mul = True;para = module.split(self.fonctionParaEntry)[1][:-1].split(self.basicSeperator);module = y[2]
          for i in range(len(y[1])):module = module.replace(y[1][i],para[i])
      
      if not Mul:
        module = module.replace(self.actualPos,str(index))
        endModulesList.append([eval(module.split(self.basicSeperator)[0]),eval(module.split(self.basicSeperator)[1])]);index+=1
      else:
        for z in module.split(self.basicBackLine):
          z = z.replace(self.actualPos,str(index))
          endModulesList.append([eval(z.split(self.basicSeperator)[0]),eval(z.split(self.basicSeperator)[1])]);index+=1
    return endModulesList


  def OldEncode(self,data,start="2,1"):# Old Methode 2, not working
    variables = [];variablesMultiple = [];CountLine = 0;Pointer=len(start)
    data = data.replace("\n","").replace(" ","")
    splittedData = data.split(";")
    recoverData = start
    returning = []

    for exe in splittedData:
      Pointer+=len(exe)+1
      IsCode = True
      HaveRecursion = False

      exe.replace("~",str(CountLine))
      if exe.find(':') != -1: variables.append([str(exe[:exe.find(':')]),CountLine]); exe = exe.split(":")[1]
      if exe.find('=') != -1:
        if exe[exe.find('=')] != '{':variables.append([str(exe[:exe.find('=')]),str(exe[exe.find('=')+1:])])
        else:
          text = data[Pointer-len(str(exe[exe.find('=')+1:])):]
          data = text.split("}",1)[0]
          variablesMultiple.append([str(exe[:exe.find('=')]),data])
        IsCode = False

      for x in variables:exe = exe.replace(x[0],str(x[1])) # Replace variable
      for x in variablesMultiple: # Replace multiple
        if exe.find(x[0]):
          HaveRecursion = True
          RecurtionData = ";"+x[1]

      if IsCode:
        if not HaveRecursion:
          add1 = exe.split(",")[0]
          add2 = exe.split(",")[1]

          recoverData+=";"+add1+","+add2
        else:
          recoverData+=RecurtionData
        CountLine+=1

    recoverDataSplitted = recoverData.split(";")

    for x in recoverDataSplitted:
      x = x.split(",")
      for y in range(len(x)):x[y] = int(x[y])
      returning.append(x)
    return returning

  def ToCythanCode(self,code): # Old Methode, not working
    variables = [];Count = 1;returning = [[1,1]]

    rawcode = code.replace("\n","")
    codeChange = ""
    for exe in rawcode.split(";"):
      IsCode = True

      exe.replace("~",str(Count))
      if exe.find(':') != -1: variables.append([str(exe[:exe.find(':')]),Count]); exe = exe.split(":")[1]
      if exe.find('=') != -1:
        if exe[exe.find('=')] != '{':variables.append([str(exe[:exe.find('=')]),str(exe[exe.find('=')+1:])])
        else:
          pointer = 5
          while rawcode[pointer] != "}":
            pointer+=1
        IsCode = False

      for x in variables:exe = exe.replace(x[0],str(x[1])) # Replace variable

      if IsCode:
        Count+=1
        for x in exe.split(";"):
          for y in exe.split(","):
            codeChange += y
          codeChange+=";"

    codeChange = codeChange.split(";")
    for x in codeChange:
      x = x.split(",")
      for y in range(len(x)):x[y] = int(x[y])
      returning.append(x)

    return returning



if __name__ == "__main__":
  CCG = CythanCodeGenerator()
  file = open("Code.txt","r")
  content = "".join(file.readlines())
  Data = CCG.Encode(content)
  print(Data)
  Machine = CythanMachine(Data,printLevel=3,follow=[0,1,2,3,4,5,6,7,8,9],dataAppend=50)
  # 888 is sucessful, 99 is not