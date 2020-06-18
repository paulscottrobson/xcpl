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
				paramCount = 0
				self.lastProcedure = procAddr
				self.ident.clearLocals()									# no locals defined.
				self.ic.checkNext(stream,"(")								# parameter open.
				sn = stream.get()											# get next
				if sn != ")":												# process parameters.
					stream.put(sn)											# put it back
					paramCount = self.compileWriteParameters(stream)		# write the parameters out.
					print(paramCount)
				self.ic.defineProcedure(s,procAddr,paramCount)					
				self.ic.compile(stream)										# compile the body.
				self.cg.c_ret()												
			s = stream.get()
	#
	#		Handle parameters
	#
	def compileWriteParameters(self,stream):
		paramList = []														# list of param names
		s = ","														
		while s == ",":														# repeat loop :)
			ident = stream.get()
			if not self.ic.isIdentifier(ident):
				raise XCPLException("Bad parameter")
			paramList.append(ident)
			s = stream.get()
		if s != ")":														# check closing )
			raise XCPLException("Syntax Error")
		paramBlock = self.cg.allocUninitialised(len(paramList)*2)			# allocate memory
		self.cg.c_lcw(0,paramBlock)											# load into R0
		for i in range(0,len(paramList)):									# for each param
			self.ident.set(False,paramList[i],paramBlock+i*2)				# save address
			self.cg.c_sia(i+1)												# save param from reg
		return len(paramList)

if __name__ == "__main__":
	fc = FileCompiler(CodeGen(X16CodeGen(1024,1024)),IdentStore())
	stream = TextParser("""
		var n;
		const c = 43;	
		star() {
			n = c;
			print.char(42);
		}
		double(cz) {
			print.char(cz);print.char(cz);
		}
		star2() { star();star();double(64); }

		twoChar(c1,c2) { print.char(c1);print.char(c2); }

		lotsChar(n,c) { do(n) { print.char(c); } }

		main() {
			var n;
			do(20,n) {
			lotsChar(n+1,42);
			print.char(13); }
		}
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
