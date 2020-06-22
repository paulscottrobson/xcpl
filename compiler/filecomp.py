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
				h = self.cg.getListHandle()
				if h is not None:
					h.write(";\n;\t\t{0}()\n;\n".format(s))
				procAddr = self.cg.getCodePointer()							# start of procedure
				paramCount = 0
				self.lastProcedure = procAddr
				self.ident.clearLocals()									# no locals defined.
				self.ic.checkNext(stream,"(")								# parameter open.
				sn = stream.get()											# get next
				if sn != ")":												# process parameters.
					stream.put(sn)											# put it back
					paramCount = self.compileWriteParameters(stream)		# write the parameters out.
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
	#
	#		Write the start program.
	#
	def writeStartCode(self):
		self.cg.setExecuteAddress(self.cg.getCodePointer())					# we run to this point
		self.cg.c_call(self.lastProcedure)									# call last defined procedure
		self.cg.c_br(0xFF)													# compile branch loop
	#
	#		Support pass-through functions
	#
	def setListHandle(self,handle = sys.stdout):
		self.cg.setListHandle(handle)
	def writeProgram(self,fileName):
		self.cg.writeProgram(fileName)

if __name__ == "__main__":
	fc = FileCompiler(CodeGen(X16CodeGen(1024,1024)),IdentStore())
	fc.setListHandle()
	mainProgram = fc.compileFile("test.x")
	print("............")
	fc.writeStartCode()
	fc.writeProgram("test.prg")
