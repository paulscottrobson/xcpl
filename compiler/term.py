# *****************************************************************************
# *****************************************************************************
#
#		Name:		term.py
#		Purpose:	Term compiler
#		Date: 		6th June 2020
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# *****************************************************************************
# *****************************************************************************

from error import *
from xparser import *
from codegen import *
from ident import *
from x16codegen import *
from xtypes import *
from sour16 import *

# *****************************************************************************
#
#						Term compiler worker class
#
# *****************************************************************************
#
#	Terms can be:
#		a constant 		- returns as a constant, no code
#		an identifier 	- returns address as a variable reference (check exists)
#		a string 		- returns address as a constant, created in initialised data space
#		@identifier 	- returns a constant, the address of the identifier (check exists)
#		(expr) 			- returns a value
#		?term 			- returns a byte reference
#		!term 			- returns a word reference.
#		-term 			- returns a constant or a value.
#
class TermCompiler(object):
	def __init__(self,codeGenerator,identStore):
		self.cg = codeGenerator
		self.identStore = identStore
	#
	#		Compile a term at the given level from the given stream.
	#
	def compile(self,stream,regLevel,expressionCompiler):
		t = stream.get()														# get the term.
		if t == "":
			raise XCPLException("Missing term")
		#
		#		Integer constant
		#
		if t[0] >= '0' and t[0] <= '9':											# constant
			return [VType.CONST,int(t)]
		#
		#		Byte or word data.
		#
		elif t == "bytes" or t == "words":										# byte or word definition
			return [VType.CONST,self.createTable(stream,t == "bytes",expressionCompiler)]
		#
		#		Unary function
		#
		if t == "strlen" or t == "random" or t == "sign" or t == "abs":			# unary functions
			if t != "random":													# random doesn't take param
				value = self.compile(stream,regLevel,expressionCompiler) 		# what to negate ?
				self.convertToValue(value,regLevel)								# make it a value.
			else:
				c1 = stream.get()												# no parameters empty
				c2 = stream.get()
				if c1 != "(" or c2 != ")":
					raise XCPLException("Syntax Error")
			self.loadConstantCode(15,regLevel)									# RF to what we work on.
			self.cg.c_call(self.identStore.get("unary"+t))						# compile call.
			return [VType.VALUE]

		#
		#		Identifier
		#
		elif t[0] >= 'a' and t[0] <= 'z':
			addr = self.identStore.get(t)										# get the address
			if addr is None:													# it must exist
				raise XCPLException("Unknown variable "+t)
			return [VType.VARREF,addr]
		#
		#		String
		#
		elif t[0] == '"':			
			t = t[1:]+chr(0)													# string to write has $00 added
			addr = self.cg.writeDataMemory(ord(t[0]))							# first char - must be one
			for c in t[1:]:														# rest of string text/null
				self.cg.writeDataMemory(ord(c))	
			return [VType.CONST,addr]
		#
		#		Identifier address
		#
		elif t == '@':															# variable reference.
			t = self.compile(stream,regLevel,expressionCompiler) 				# get the term
			if t[0] != VType.VARREF:											# check a variable reference
				raise XCPLException("@ must be followed by an identifier")
			return [VType.CONST,t[1]]											# convert to constant
		#
		#		Parenthesised expression
		#
		elif t == '(':															# parenthesis
			t = expressionCompiler.compile(stream,regLevel,self)				# call expression compiler
			if stream.get() != ")":
				raise XCPLException("Missing closing parenthesis")
			return t
		#
		#		Byte or Word reference.
		#
		elif t == '!' or t == '?':
			addr = self.compile(stream,regLevel,expressionCompiler)				# get the address
			if t[0] == '!' and addr[0] == VType.CONST:							# !const is a variable ref
				return [VType.VARREF,addr[1]]
			self.convertToValue(addr,regLevel)									# make it actual value.
			return [VType.BYTEREF if t[0] == '?' else VType.WORDREF]			# return as reference.
		#
		#		Unary minus
		#
		elif t == "-":
			value = self.compile(stream,regLevel,expressionCompiler) 			# what to negate ?
			if value[0] == VType.CONST:											# - constant
				return [VType.CONST,(-value[1]) & 0xFFFF ]
			else:
				self.convertToValue(value,regLevel)								# make it a value.
				self.negateRegister(regLevel)
				return [VType.VALUE]
		else:
			raise XCPLException("Syntax error "+t)
	#
	#		Convert the potential value to an actual value, dereference or 
	#		concrete condition.
	#
	def convertToValue(self,e,regLevel):
		#
		#		Type is constant.
		#
		if e[0] == VType.CONST:
			self.loadConstantCode(regLevel,e[1])
		#
		#		Type is variable reference.
		#
		elif e[0] == VType.VARREF:
			self.cg.c_ldr(regLevel,e[1])
		#
		#		Type is byte reference
		#
		elif e[0] == VType.BYTEREF:
			self.cg.c_lbi(regLevel)
		#
		#		Type is word reference
		#
		elif e[0] == VType.WORDREF:
			self.cg.c_lwi(regLevel)
		#
		#		Type is condition
		#
		elif e[0] != VType.VALUE:
			assert False
	#
	#		Generate code to load constant
	#
	def loadConstantCode(self,reg,n):
		n = n & 0xFFFF
		if n >= 256:
			self.cg.c_lcw(reg,n)
		else:
			self.cg.c_lcb(reg,n)
	#
	#		Generate code to negate a register
	#
	def negateRegister(self,reg):
		self.loadConstantCode(15,reg)											# RF to what we negate
		self.cg.c_call(Sour16.X_NEGATE)											# negate it.
	#
	#		Create a table
	#
	def createTable(self,stream,isByte,expressionCompiler):
		if stream.get() != "(":													# check open bracket.
			raise XCPLException("Missing (")
		done = False
		addr = None
		while not done:
			t = self.compile(stream,1,expressionCompiler)						# get next
			if t[0] != VType.CONST:												# must be a constant of some sort
				raise XCPLException("Table entries can only be constants")
			if isByte and t[1] > 0xFF:											# word data in byte table
				raise XCPLException("Word data in byte table")
			a = self.cg.writeDataMemory(t[1] & 0xFF)							# write LSB
			addr = a if addr is None else addr 									# save addr of first if first
			if not isByte:
				self.cg.writeDataMemory(t[1] >> 8)
			s = stream.get()													# what follows , or )
			if s != ")" and s != ",":
				raise XCPLException("Syntax error")
			done = (s == ")")
		return addr
	#
	#		Test routine. Uses self for parenthesis, so (a+b) won't work.
	#
	def test(self,stream):
		s = stream.get()
		stream.put(s)
		print("\n*********** "+s+" ***********")
		self.cg.setListHandle()							
		r = self.compile(stream,2,self)				
		print("\nReturns [VType.{0}{1}]".format(VType.TOSTRING[r[0]],
								",${0:04x}".format(r[1]) if len(r) == 2 else ""))
		print("Complete-->")
		self.convertToValue(r,2)

if __name__ == "__main__":
	codeGen = CodeGen(X16CodeGen(1024,1024))		
	idStore = TestIdentStore()
	tc = TermCompiler(codeGen,idStore)					# we use this for the expression compiler.


	stream = TextParser("""
		42 $104 'X' 
		"Hello" ""
		@count
		count
		(42)
		!55 !count ?55 ?count ??4 !!4 !!count !?count
		-4 -count	
		!d
		?4096
		!4096
		bytes(1,2,3)
		words(4,9,12)
		len("hello")
	""".split("\n"))
	for i in range(0,24):
			tc.test(stream)
