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
		self.lastProcedure = None
	#
	#		Compile one file stream
	#
	def compile(self,stream):
		s = stream.get() 													# get first word
		while s != "":
			if s == "var":													# variable definition.
				self.ic.compileVariableDeclaration(stream,True)
			elif s == "const":												# constant definition
				self.ic.compileConstantDeclaration(stream,True)
			else:															# must be a proc defn.			
				if not self.ic.isIdentifier(s):
					raise XCPLException("Syntax Error")
				procAddr = self.cg.getCodePointer()							# start of procedure
				self.lastProcedure = procAddr
				self.ident.set(True,s,procAddr)								# set the definition.
				self.ident.clearLocals()									# no locals defined.
				self.ic.checkNext(stream,"(")								# parameter open.
				s = stream.get()											# get next
				if s != ")":												# process parameters.
					stream.put(s)											# put it back
					self.compileWriteParameters()							# write the parameters out.
				self.ic.compile(stream)										# compile the body.
				self.cg.c_ret()												
			s = stream.get()

if __name__ == "__main__":
	fc = FileCompiler(CodeGen(X16CodeGen(1024,1024)),IdentStore())
	stream = TextParser("""
		var n;
		const c = 43;	
		star() {
			n = c;
			print.char(42);
		}
		star2() { star();star(); }
	""".strip().split("\n"))

#	codeStart = fc.cg.getCodePointer()
	fc.ic.cg.setListHandle()
	fc.compile(stream)

	print("............")
	fc.ic.cg.setExecuteAddress(fc.ic.cg.getCodePointer())
	fc.ic.cg.c_call(fc.lastProcedure)
	fc.ic.cg.c_xeq()
	p = fc.ic.cg.getCodePointer()	
	fc.ic.cg.c_lcw(0,0xFFFF)
	fc.ic.cg.write(p+0,0xEA)
	fc.ic.cg.write(p+1,0x80)
	fc.ic.cg.write(p+2,0xFE)
	fc.ic.cg.writeProgram("test.prg")
