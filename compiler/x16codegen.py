# *****************************************************************************
# *****************************************************************************
#
#		Name:		x16codegen.py
#		Purpose:	Commander X16 Code Generator
#		Date: 		6th June 2020
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# *****************************************************************************
# *****************************************************************************

from error import *
from sour16 import *
from basecodegen import *

import sys
		
# *****************************************************************************
#
#							Code Generator (Commander X16)
#
# *****************************************************************************

class X16CodeGen(BaseCodeGenClass):
	def _setupMemoryUsage(self,freeMem,uninitSize,initSize):
		#
		self.iPointer = freeMem 												# initialised data
		self.iLimit = self.iPointer + initSize 									# space
		#
		self.uPointer = self.iLimit												# uninitialised data space
		self.uLimit = self.uPointer + uninitSize
		#
		self.codePtr = self.uLimit 												# where code actually goes.
		self.codeLimit = 0x9F00													# where it ends.
	#
	def getFreeMemoryAddress(self):
		return self.codePtr 													# free memory after code.

if __name__ == "__main__":
	cg = X16CodeGen(1024,1024)
	cg.assemble(16,2,32765)
	cg.assemble(48,0)
	cg.assemble(8,1,-2)
