#
#	Automatically generated wrapper class for code generator.
#
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
	def c_ldi(self,reg,operand):
		return self.cg.assemble(0x10+reg,2,operand)
	def c_adi(self,reg,operand):
		return self.cg.assemble(0x20+reg,2,operand)
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
	def c_tzero(self,):
		return self.cg.assemble(0x01,0)
	def c_tnonzero(self,):
		return self.cg.assemble(0x02,0)
	def c_tminus(self,):
		return self.cg.assemble(0x03,0)
	def c_tplus(self,):
		return self.cg.assemble(0x04,0)
	def c_brzero(self,operand):
		return self.cg.assemble(0x05,1,operand)
	def c_brnonzero(self,operand):
		return self.cg.assemble(0x06,1,operand)
	def c_brminus(self,operand):
		return self.cg.assemble(0x07,1,operand)
	def c_brplus(self,operand):
		return self.cg.assemble(0x08,1,operand)
	def c_br(self,operand):
		return self.cg.assemble(0x09,1,operand)
	def c_call(self,operand):
		return self.cg.assemble(0x0b,2,operand)
	def c_ret(self,):
		return self.cg.assemble(0x0e,0)
	