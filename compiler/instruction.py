# *****************************************************************************
# *****************************************************************************
#
#		Name:		instruction.py
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
		self.ident = identStore if identStore is not None else Ident()			# Create identifier store if reqd
		self.termCompiler = TermCompiler(self.cg,self.ident)					# Create term/expression compiler
		self.exprCompiler = ExpressionCompiler(self.cg,self.ident)				# workers.
	#
	#		Compile one instruction
	#
	def compile(self,str):
		s = str.get()															# get next token.
		if False:
			pass
		else:																	# don't recognise it.
			str.put(s)															# put it back
			self.compileIdentifier(str)											# assume it's an identifier.
	#
	#		Compile when an identifier is the first element. Can be an assignment, procedure call.
	#	
	def compileIdentifier(self,str):
		r = self.exprCompiler.compile(str,0,self.termCompiler)					# compile the address as l-expr
		s = str.get()															# what follows ?
		#
		#		Handle assignment
		#
		if s == "=":
			if r[0] == VType.VARREF:											# variable reference.
				self.termCompiler.loadConstantCode(0,r[1])						# load variable addr -> R0
				r = [VType.WORDREF] 											# it's now a word reference.
			self.exprCompiler.compileValue(str,1,self.termCompiler) 			# do the right hand side -> R1
			if r[0] == VType.WORDREF:
				self.cg.c_sia(1) 												# save word indirect 												
			else:
				self.cg.c_sbi(1)												# save byte indirect
		#
		#		Procedure invocation
		#
		elif s == "(":	
			# Must be VARREF.														
			assert False,"TODO"
		else:
			raise XCPLException("Syntax Error")



if __name__ == "__main__":
	ic = InstructionCompiler(X16CodeGen(1024,1024),TestIdentStore())
	stream = TextParser("""
		count!2242 = 4
	""".strip().split("\n"))

	codeStart = ic.cg.getCodePointer()
	ic.cg.setExecuteAddress(codeStart)
	ic.cg.setListHandle()

	ic.compile(stream)

	print("............")
	ic.cg.c_xeq()
	p = ic.cg.getCodePointer()
	ic.cg.c_lcw(0,0xFFFF)
	ic.cg.write(p,0xFF)
	ic.cg.writeProgram("test.prg")
