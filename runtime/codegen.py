#
#	Automatically generated wrapper class for code generator.
#
import sys
class CodeGen(object):
	def __init__(self,codeGen):
		self.cg = codeGen
	def allocUninitialised(self,size):
		return self.cg.allocUninitialised(size)
	def writeDataMemory(self,data):
		return self.cg.writeDataMemory(data)
	def setExecuteAddress(self,address):
		return self.cg.setExecuteAddress(address)
	def write(self,address,data):
		return self.cg.write(address,data)
	def assemble(self,opcode,operandSize = 0,operand = None):
		return self.cg.assemble(opcode,operandSize,operand)
	def getListHandle(self):
		return self.cg.getListHandle()
	def setListHandle(self,handle = sys.stdout):
		return self.cg.setListHandle(handle)
	def getCodePointer(self):
		return self.cg.getCodePointer()
	def updateFreeMemory(self):
		return self.cg.updateFreeMemory()
	def writeProgram(self,fileName):
		return self.cg.writeProgram(fileName)
	def c_lcw(self,reg,operand):
		return self.cg.assemble(0x10+reg,2,operand)
	def c_lcb(self,reg,operand):
		return self.cg.assemble(0x20+reg,1,operand)
	def c_add(self,reg):
		return self.cg.assemble(0x30+reg,0)
	def c_sub(self,reg):
		return self.cg.assemble(0x40+reg,0)
	def c_and(self,reg):
		return self.cg.assemble(0x50+reg,0)
	def c_orr(self,reg):
		return self.cg.assemble(0x60+reg,0)
	def c_xor(self,reg):
		return self.cg.assemble(0x70+reg,0)
	def c_sbi(self,reg):
		return self.cg.assemble(0x80+reg,0)
	def c_lwi(self,reg):
		return self.cg.assemble(0x90+reg,0)
	def c_lbi(self,reg):
		return self.cg.assemble(0xa0+reg,0)
	def c_shf(self,reg):
		return self.cg.assemble(0xb0+reg,0)
	def c_ldr(self,reg,operand):
		return self.cg.assemble(0xc0+reg,2,operand)
	def c_sia(self,reg):
		return self.cg.assemble(0xe0+reg,0)
	def c_brz(self,operand):
		return self.cg.assemble(0x01,1,operand)
	def c_brnz(self,operand):
		return self.cg.assemble(0x02,1,operand)
	def c_br(self,operand):
		return self.cg.assemble(0x03,1,operand)
	def c_chz(self):
		return self.cg.assemble(0x05,0)
	def c_call(self,operand):
		return self.cg.assemble(0x06,2,operand)
	def c_ret(self):
		return self.cg.assemble(0x08,0)
	def c_xeq(self):
		return self.cg.assemble(0x0f,0)
	