import shlex

class CommandLine():

	def __init__(self):
		self.funct = []
		self.quit = False
		self.cmdReturn = ""
		self.vars = {}
	
	def setVars(self,kwargs):
		self.vars = kwargs

	def addFunction(self,caller = None) -> "Methode de passage":
		def inner(funct) -> "retourne la nouvelle fonction":


			def newFunct(*arg,**kwargs) -> "Nouvelle fonction":
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
					except:
						if isinstance(annot,tuple):
							try:
								if not isinstance(annot[0],arg[i]): param = annot[0]
								else:param = annot[1]
							except IndexError: param = annot[1]
						else: raise AssertionError("Vous n'avez pas le bon nombre d'arguments.")
					if annot == "return": pass
					elif annot == None:
						pass
					
						# Oblige d'avoir un argument
					elif isinstance(annot,bool):
						try: param = bool(param)
						except:raise AssertionError("Le parametre "+param+" doit etre un booléen")
					elif isinstance(annot,str):
						try: param = str(param)
						except:raise AssertionError("Le parametre "+param+" doit etre un string")
					elif isinstance(annot,int):
						try: param = int(param)
						except:raise AssertionError("Le parametre "+param+" doit etre un entier")
					elif isinstance(annot,float):
						try: param = float(param)
						except: raise AssertionError("Le parametre "+param+" doit etre un float")
					new_args.append(param)
					i+=1
				return funct(*tuple(new_args),**kwargs) # Si tout est bon, on execute la fonction


			# Ajout au dictionnaire de la fonction
			newFunct.caller = caller
			self.funct.append(newFunct)
			self.funct[self.funct.index(newFunct)].__name__ = funct.__annotations__.pop("return")
			self.funct[self.funct.index(newFunct)].__doc__ = funct.__doc__
			

			return newFunct # On retourne notre meilleure fonction.
		return inner


	def menu(self):
		print("Tapez 'help' pour la liste des commandes.")
		print("Tapez 'help cmd' pour les informations d'utillisation de la ligne de commandes.")

		while not self.quit:
			commandes_raw = input("=> ")
			#for x in commandes_raw.split("$"):
			#self.vars[commandes_raw.split("$")]
			# 
			commandes = commandes_raw.split(";")
			for commande in commandes:
				trt_commande = shlex.split(commande)
				self.cmdReturn = self.execute(trt_commande)
			if self.cmdReturn != None: print(self.cmdReturn)


	def execute(self,execute):
		if isinstance(execute,str):execute = shlex.split(execute)
		if execute == []: return None
		returning = None
		find = False
		for funct in self.funct:
			if funct.__name__.split(" ")[0] == execute[0]:
				try:
					if funct.caller: returning = funct(funct.caller,*execute[1:],**self.vars)
					else:returning = funct(*execute[1:],**self.vars)
				except AssertionError as err:
					print("Erreur d'argument: "+str(err))
				finally:
					find =True
		if not find:
			returning = "Aucune commande trouver. Tapez 'help' pour la liste des commandes."
		return returning
