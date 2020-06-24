# *****************************************************************************
# *****************************************************************************
#
#		Name:		compiler.py
#		Purpose:	Compiler Main Program
#		Date: 		22nd June 2020
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# *****************************************************************************
# *****************************************************************************

from error import *
from ident import *
from codegen import *
from x16codegen import *
from filecomp import *
import os,sys,re

# *****************************************************************************
#
#							Class manages compilation
#
# *****************************************************************************

class CompilerManager(object):
	def __init__(self):
		self.sources = []													# list of source files/binary files etc.
		self.targetFile = "out.prg"										# final object file.
		self.uninitDataSize = 2048 											# uninitialise data space
		self.initDataSize = 1024 											# initialised data.
		self.listing = False
	#
	#		Load a list of sources/controls in.
	#
	def loadControls(self,ctrl):
		while len(ctrl) != 0:												# keep going till all processed
			s = ctrl.pop(0)													# get keyword
			if s.startswith("-"):											# operator.
				s = s.lower()
				if s == "-lv":
					self.listing = True
					self.listHandle = sys.stdout
				elif s == "-l":
					self.listing = True
					self.listHandle = open(self.getParam(ctrl),"w")
				elif s == "-o":
					self.targetFile = self.getParam(ctrl)
				elif s == "-p":
					self.loadProject(self.getParam(ctrl))
				elif s == "-i" or s == "-u":
					size = self.getParam(ctrl)
					if re.match("^\\d+$",size) is None or int(size) < 0 or int(size) > 16384:
						raise XCPLException("Bad Data Size")
					if s == "-i":
						self.initDataSize = int(size)
					else:
						self.uninitDataSize = int(size)
				else:
					raise XCPLException("Unknown option "+s)
			else:
				self.sources.append(s)
	#
	#		Get a parameter
	#
	def getParam(self,ctrl):
		if len(ctrl) == 0:
			raise XCPLException("Missing parameter")
		return ctrl.pop(0)
	#
	#		Load in a project
	#
	def loadProject(self,projectFile):
		if not os.path.isfile(projectFile):
			raise XCPLException("Bad project file")
		src = [x for x in open(projectFile).readlines() if not x.strip().startswith("#")]
		self.loadControls(" ".join(src).split())
	#
	#		Build the program.
	#
	def build(self):
		fc = FileCompiler(CodeGen(X16CodeGen(self.uninitDataSize,self.initDataSize)),IdentStore())
		if self.listing:
			fc.setListHandle(self.listHandle)
		if len(self.sources) == 0:
			raise XCPLException("No source files.")
		for s in self.sources:
			mainProgram = fc.compileFile(s)
		fc.writeStartCode()
		fc.writeProgram(self.targetFile)
	#
	#		Display the help file
	#
	def showHelp(self):
		print("xc <files> -l <listfile> -lv -o <program file> -p <project file> -i <init data> -u <unint data>")
		print("\tXCPL Compiler v0.11 (alpha) 22-Jun-2020.\n\tWritten by Paul Robson 2020. MIT License.")

def run():
	XCPLException.LINE = 0
	try:
		cm = CompilerManager()												# create instance
		if len(sys.argv) == 1:
			cm.showHelp()
			sys.exit(1)
		cm.loadControls(sys.argv[1:])										# load files/flags/etc.
		cm.build()															# build the program
		sys.exit(0)															# exit without error.
	except XCPLException as xe:
		msg = str(xe)
		if XCPLException.LINE != 0:
			msg = "{0}({1}) {2}".format(XCPLException.FILE,XCPLException.LINE,msg)
		print(msg)
		sys.exit(1)


if __name__ == "__main__":
	run()
