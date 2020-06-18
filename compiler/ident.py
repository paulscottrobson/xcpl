# *****************************************************************************
# *****************************************************************************
#
#		Name:		ident.py
#		Purpose:	Identifier Storage
#		Date: 		6th June 2020
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# *****************************************************************************
# *****************************************************************************

from error import *

# *****************************************************************************
#
#							Identifier Storage
#
# *****************************************************************************

class IdentStore(object):
	def __init__(self):
		self.locals = {}
		self.globals = {}
		self.assoc = {}
	#
	#		Set a value
	#
	def set(self,isGlobal,identifier,value,assoc = None):
		identifier = identifier.strip().lower()
		st = self.globals if isGlobal else self.locals 
		if identifier in st:
			raise XCPLException("Duplicate identifier "+identifier)
		st[identifier] = [value,assoc]
	#
	#		Get a value/associated value
	#
	def get(self,identifier,assoc = False):
		index = 1 if assoc else False
		identifier = identifier.strip().lower()
		if identifier in self.locals:
			return self.locals[identifier][index]
		if identifier in self.globals:
			return self.globals[identifier][index]
		return None
	#
	#		Clear the locals
	#
	def clearLocals(self):
		self.locals = {}
	#
	#		Get/Set associated values
	#
	def getAssoc(self,k):
		return self.assoc[k] if k in self.assoc else None
	def setAssoc(self,k,v):
		self.assoc[k] = v

# *****************************************************************************
#
#						Debugging identifier store
#
# *****************************************************************************

class TestIdentStore(IdentStore):
	def __init__(self):
		IdentStore.__init__(self)
		self.set(True,"a",0xAA)
		self.set(True,"b",0xBB)
		self.set(True,"c",0xCC)
		self.set(True,"d",0xDD)
		self.set(True,"minus1",-1)
		self.set(False,"count",32)
		self.set(False,"star",0x2A)