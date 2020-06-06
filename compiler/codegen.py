# *****************************************************************************
# *****************************************************************************
#
#		Name:		codegen.py
#		Purpose:	Base Code Generator
#		Date: 		6th June 2020
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# *****************************************************************************
# *****************************************************************************

from error import *
from sour16 import *

# *****************************************************************************
#
#							Parses a text file
#
# *****************************************************************************

class CodeGen(object):
	#
	#		Initialisation. Copies the run time, and allocates uninitialised and initialised
	#		Data memory
	#
	def __init__(self,uninitSize,initSize):
		self.code = [x for x in Sour16.RUNTIME]									# code object
		self.base = Sour16.LOADADDR 											# the load address
		self.setupMemoryUsage(uninitSize,initSize)
		self.codeStart = self.codePtr
	#
	#		
	#
	def setupMemoryUsage(self,uninitSize,initSize):
		#
		self.iPointer = self.code[8]+self.code[9]*256 							# initialised data
		self.iLimit = self.iPointer + initSize 									# space
		#
		self.uPointer = self.iLimit												# uninitialised data space
		self.uLimit = self.uPointer + uninitSize
		#
		self.codePtr = self.uLimit 												# where code actually goes.
		self.codeLimit = 0x9F00													# where it ends.
	#
	#		Allocate Uninitialised Data Memory
	#
	def allocUninitialised(self,size):
		addr = self.uPointer
		self.uPointer += size
		if self.uPointer >= self.uLimit:
			raise XCPLException("Out of uninitialised data memory")
	#
	#		Write a byte to initialised data memory.
	#
	def writeDataMemory(self,data):
		if self.iPointer == self.iLimit:										# out of memory
			raise XCPLException("Out of initialised data Memory")
		self.write(self.iPointer,data)											# write and bump pointer
		self.iPointer += 1
		return self.iPointer-1
	#
	#		Set the execute address
	#
	def setExecuteAddress(self,address):
		assert address >= self.codeStart and address < self.codePtr
		self.code[4] = address & 0xFF
		self.code[5] = (address >> 8) & 0xFF
	#
	#		Write to the code base.
	#
	def write(self,address,data):
		assert address >= self.base and address < 0x10000
		assert data >= 0 and data < 0x100
		address = address - self.base 											# offset in data
		while len(self.code) < address+1: 										# pad it out if required
			self.code.append(0xFF)
		self.code[address] = data 	
	#
	#		Instruction writers.
	#
	def assemble(self,opcode,operandSize = 0,operand = None):
		addr = self.write(self.codePtr,opcode) 									# write to memory
		if operandSize == 1:
			self.write(self.codePtr+1,operand & 0xFF)
		if operandSize == 2:
			self.write(self.codePtr+2,(operand >> 8) & 0xFF)
		self.codePtr += self.operandSize 										# advance code pointer

if __name__ == "__main__":
	cg = CodeGen(1024,1024)
	print("{0:x}".format(cg.writeDataMemory(42)))
	print("{0:x}".format(len(cg.code)))
