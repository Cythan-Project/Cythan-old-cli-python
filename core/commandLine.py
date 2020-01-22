import ..include.CommandLineGenerator
from random import randint, sample

CommandLine = CommandLineGenerator.CommandLine()
CommandLine.setVars(
	{
	}
)

@CommandLine.addFunction()
def credits(**kwargs) -> "credits":
	'''
	Les crédits.
	'''
	return "Projet de Cyprien BOUROTTE du Lycee La Trinite Neuilly sur seine.\nRéalisé sous le nom du studio 'Révolutions'."




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
def echo(name:str,**kwargs) -> "echo VAR_NAME":
	'''
	Affiche une variable enregister par set
	'''
	try:
		return CommandLine.vars[name]
	except KeyError:
		return "La variable "+name+" n'as pas été trouvé."


@CommandLine.addFunction()
def add(number1:float,number2:float,**kwargs) -> "add NUMBER NUMBER":
	'''
	Fais une addition
	'''
	return number1 + number2

@CommandLine.addFunction()
def mul(number1:float,number2:float,**kwargs) -> "mul NUMBER NUMBER":
	'''
	Fais une multiplication
	'''
	return number1 * number2


@CommandLine.addFunction()
def set(name:str,element: max,**kwargs) -> "set VAR_NAME ELE":
	'''
	Enregistre une variable comme element
	Essaie dans l'ordre : De convertir en bool (mettez T/F), int, float, string.
	'''
	if element == "T":CommandLine.vars[name] = True
	elif element == "F":CommandLine.vars[name] = False
	else:
		try:
			CommandLine.vars[name] = int(element)
		except ValueError:
			try:
				CommandLine.vars[name] = float(element)
			except ValueError:
				CommandLine.vars[name] = element
	print("SET: La variable '"+name+"' à été mise à '"+str(CommandLine.vars[name])+"'")

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

Exemple:
help;grab echo : renverra seulement la ligne de l'aide sur la commande echo.

	"""
	return "Commande inconnue.\nTapez 'help' pour la liste des commandes.\nTapez 'help cmd' pour les informations d'utillisation de la ligne de commandes."

if __name__ == '__main__' :
    CommandLine.menu()