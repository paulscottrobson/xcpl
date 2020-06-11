# *****************************************************************************
# *****************************************************************************
#
#		Name:		Instruction.py
#		Purpose:	Instruction compiler
#		Date: 		8th June 2020
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# *****************************************************************************
# *****************************************************************************

from error import *
from xparser import *
from ident import *
from codegen import *
from x16codegen import *
from xtypes import *
from term import *
from expression import *

# *****************************************************************************
#
#						Instruction compiler worker class
#
# *****************************************************************************

class InstructionCompiler(object):
	def __init__(self,codeGenerator,identStore = None):
		assert codeGenerator is not None
		self.cg = CodeGen(codeGenerator) 										# Wrap provided code generator
		self.ident = identStore if identStore is not None else IdentStore()		# Create identifier store if reqd
		self.termCompiler = TermCompiler(self.cg,self.ident)					# Create term/expression compiler
		self.exprCompiler = ExpressionCompiler(self.cg,self.ident)				# workers.
	#
	#		Compile one Instruction
	#
	def compile(self,stream):
		s = stream.get()														# get next token.
		if s == "":																# check something.
			return False
		elif s == "{":															# code group.
			self.compileBlock(stream)
		elif s == "var":
			self.compileVariableDeclaration(stream,False)
		else:																	# don't recognise it.
			stream.put(s)														# put it back
			self.compileIdentifier(stream)										# assume it's an identifier.
		return True
	#
	#		Compile a block.
	#
	def compileBlock(self,stream):
		cmd = stream.get()
		while cmd != "}":
			stream.put(cmd)
			self.compile(stream)
			cmd = stream.get()
	#
	#		Compile a variable declaration.
	#
	def compileVariableDeclaration(self,stream,isGlobal):
		cont = ","
		while cont == ",":														# keep going while more
			ident = stream.get()												# new name
			if not self.isIdentifier(ident):
				raise XCPLException("Missing variable name")
			cont = stream.get()													# what follows
			if cont == "[":														# uninitialised data ?
				size = self.termCompiler.compile(stream,0,self.exprCompiler)	# get amount
				if size[0] != VType.CONST or size[1] == 0:						# bad array size
					raise XCPLException("Bad array size")
				self.checkNext(stream,"]")
				cont = stream.get()
				array = self.cg.allocUninitialised(size[1])						# allocate memory
				addr = self.cg.writeDataMemory(array & 0xFF) 					# create reference to it
				self.cg.writeDataMemory(array >> 8)
			else:
				addr = self.cg.allocUninitialised(2)							# just a word
			self.ident.set(isGlobal,ident,addr)									# define it.
		#
		if cont != ";":															# must end with ;
			raise XCPLException("Missing ; on variable definition")
	#
	#		Compile when an identifier is the first element. Can be an assignment, procedure call.
	#	
	def compileIdentifier(self,stream):
		r = self.exprCompiler.compile(stream,0,self.termCompiler)				# compile the address as l-expr
		s = stream.get()														# what follows ?
		#
		#		Handle assignment
		#
		if s == "=":
			if r[0] == VType.VARREF:											# variable reference.
				self.termCompiler.loadConstantCode(0,r[1])						# load variable addr -> R0
				r = [VType.WORDREF] 											# it's now a word reference.
			self.exprCompiler.compileValue(stream,1,self.termCompiler) 			# do the right hand side -> R1
			if r[0] == VType.WORDREF:
				self.cg.c_sia(1) 												# save word indirect 												
			else:
				self.cg.c_sbi(1)												# save byte indirect
			self.checkNext(stream,";")
		#
		#		Procedure invocation
		#
		elif s == "(":	
			# Must be VARREF.														
			assert False,"TODO"
		else:
			raise XCPLException("Syntax Error")
	#
	#		Check next token
	#		
	def checkNext(self,stream,t):
		if stream.get() != t:
			raise XCPLException("Missing '"+t+"'")
	#
	#		Check if token is identifier
	#
	def isIdentifier(self,t):
		return t[0] >= 'a' and t[0] <= 'z'






if __name__ == "__main__":
	ic = InstructionCompiler(X16CodeGen(1024,1024))
	stream = TextParser("""
		 { 
		 	var test1,test2[12];
		 	test1 = $ABCD;
		 	test2!2 = $1357;
		 }
	""".strip().split("\n"))

	codeStart = ic.cg.getCodePointer()
	ic.cg.setExecuteAddress(codeStart)
	ic.cg.setListHandle()

	ic.compile(stream)
	ic.compile(stream)

	print("............")
	ic.cg.c_xeq()
	p = ic.cg.getCodePointer()
	ic.cg.c_lcw(0,0xFFFF)
	ic.cg.write(p,0xFF)
	ic.cg.write(p+1,0x80)
	ic.cg.write(p+2,0xFE)
	ic.cg.writeProgram("test.prg")
