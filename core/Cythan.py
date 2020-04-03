from core import Errors

class CythanMachine():

  def __init__(self, data, negdata=[-1]*100):

    self.data = data
    self.negdata = negdata

  def turn(self, nb):
    
    def combine(x,y):
      if x[0] == -1:r1=y[0]
      else:r1=x[0]
      if x[1] == -1:r2=y[1]
      else:r2=x[1]
      return [r1,r2]

    for _ in range(nb):
      try:PP = self.data[0][0]
      except:raise Errors.DataUnreachable("Data[0][0] is not reachable")
      try:PPP = self.data[PP]
      except:raise Errors.DataUnreachable("PPP: Data["+str(PP)+"] is not reachable")
      try:
        if PPP[0] == -1: dataToSet = [-1,-1]
        elif PPP[1] == -1:raise Errors.EndPoint("Machine Ended with code "+str(self.data[PPP[0]]))
      except Errors.EndPoint:raise
      except IndexError:
        raise Errors.EndPoint("Machine Ended with code from unreadable data positionned at cell "+str(PPP[0]))
      except BaseException:
        raise Errors.MinusOneRuleError("HARDWARE got a -1 rule problem.")

      try:
        if PPP[0] >=0:dataToSet = self.data[PPP[0]]
        else: dataToSet = [self.negdata[PPP[0]*-1],self.negdata[PPP[0]*-1-1]]
      except:raise Errors.DataUnreachable("DataToSet: Data["+str(PPP[0])+"] is not reachable")

      try:
        if PPP[1] >=0:dataToEarse = self.data[PPP[1]]
        else:dataToEarse= [self.negdata[PPP[1]*-1],self.negdata[PPP[1]*-1-1]]
      except:raise Errors.DataUnreachable("DataToOverWrite: Data["+str(PPP[1])+"][0] is not reachable")

      try: finaldata = combine(dataToSet, dataToEarse)
      except:raise Errors.DataCombine("HARWARE: Combine has failed.")

      try:
        self.data[0][0] += self.data[0][1]
      except:raise Errors.DataPointer("Pointer could not be add.")

      try:
        if PPP[1] >=0: self.data[PPP[1]] = finaldata
        else: self.negdata[-1*PPP[1]] = finaldata[0];self.negdata[-1*PPP[1]-1] = finaldata[1]
      except: raise Errors.DataCombine("finaldata: module "+str(PPP)+" & "+str(finaldata)+" have failed to be set.")


