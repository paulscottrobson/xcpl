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
	#
	#		Set a value
	#
	def set(self,isGlobal,identifier,value):
		identifier = identifier.strip().lower()
		st = self.globals if isGlobal else self.locals 
		if identifier in st:
			raise XCPLException("Duplicate identifier "+identifier)
		st[identifier] = value 
	#
	#		Get a value
	#
	def get(self,identifier):
		identifier = identifier.strip().lower()
		if identifier in self.locals:
			return self.locals[identifier]
		if identifier in self.globals:
			return self.globals[identifier]
		return None
	#
	#		Clear the locals
	#
	def clearLocals(self):
		self.locals = {}

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
		self.set(False,"count",100)
		self.set(False,"star",0x2A)