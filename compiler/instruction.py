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

if __name__ == "__main__":
	ic = InstructionCompiler(X16CodeGen(1024,1024),TestIdentStore())
	stream = TextParser("""
		2&3-count+1
	""".strip().split("\n"))

	codeStart = ic.cg.getCodePointer()
	ic.cg.setExecuteAddress(codeStart)

	ic.exprCompiler.test(stream,ic.termCompiler)

	ic.cg.c_xeq()
	p = ic.cg.getCodePointer()
	ic.cg.c_lcw(0,0xFFFF)
	ic.cg.write(p,0xFF)
	ic.cg.writeProgram("test.prg")
