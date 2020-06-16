# *****************************************************************************
# *****************************************************************************
#
#		Name:		filecomp.py
#		Purpose:	File compiler
#		Date: 		16th June 2020
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# *****************************************************************************
# *****************************************************************************

from error import *
from xparser import *
from ident import *
from codegen import *
from x16codegen import *
from instruction import *

# *****************************************************************************
#
#						File compiler worker class
#
# *****************************************************************************

class FileCompiler(object):
	def __init__(self,codeGenerator,identStore):
		self.cg = codeGenerator
		self.ident = identStore
		self.ic = InstructionCompiler(codeGenerator,identStore)


if __name__ == "__main__":
	fc = FileCompiler(X16CodeGen(1024,1024),IdentStore())
	stream = TextParser("""
		 { 
		 	var c,d[128];
		 	print.char(42);
		 	do (100,c) {
		 		print.hex(c);
		 	} print.char(42);
		 }
	""".strip().split("\n"))

	codeStart = fc.cg.getCodePointer()
	fc.ic.cg.setExecuteAddress(codeStart)
	fc.ic.cg.setListHandle()

	fc.ic.compile(stream)

	print("............")
	fc.ic.cg.c_xeq()
	p = fc.ic.cg.getCodePointer()
	fc.ic.cg.c_lcw(0,0xFFFF)
	fc.ic.cg.write(p+0,0xEA)
	fc.ic.cg.write(p+1,0x80)
	fc.ic.cg.write(p+2,0xFE)
	fc.ic.cg.writeProgram("test.prg")
