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
import os

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
	#		Compile one stream
	#
	def compileStream(self,stream):
		XCPLException.LINE = 1												# reset line #
		s = stream.get() 													# get first word
		while s != "":
			if s == "var":													# variable definition.
				self.ic.compileVariableDeclaration(stream,True)
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
		return self.lastProcedure
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
	#
	#		Compile one file
	#
	def compileFile(self,fileName):
		XCPLException.FILE = fileName										# set up for error.
		XCPLException.LINE = 0
		if not os.path.isfile(fileName):									# check file exists.
			raise XCPLException("Missing file "+fileName)
		stream = TextParser(open(fileName).readlines())						# make a stream
		self.compileStream(stream)											# compile it.
		return self.lastProcedure

if __name__ == "__main__":
	fc = FileCompiler(CodeGen(X16CodeGen(1024,1024)),IdentStore())
	fc.ic.cg.setListHandle()
	mainProgram = fc.compileFile("test.x")

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
