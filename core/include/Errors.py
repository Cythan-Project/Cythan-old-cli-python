class CythanError(Exception):
   """Base class for other exceptions"""
   pass

# --- CYTHAN MACHINE ERRORS ---
class MinusOneRuleError(CythanError):
	"""Error when the -1 rule is not respected"""
	pass

class DataUnreachable(CythanError):
	"""Error when Data[x][y] is not correct"""	
	pass

class DataCombine(CythanError):
	"""Error when dataToSet and dataToOverwrite is not combinable"""	
	pass

class DataPointer(CythanError):
	"""Error when pointer could not be add"""	
	pass

class EndPoint(CythanError):
	"""Machine ended."""
	pass