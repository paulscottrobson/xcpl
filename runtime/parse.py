# *****************************************************************************
# *****************************************************************************
#
#		Name:		parse.py
#		Purpose:	Scan source/label listing for opcodes and routines
#		Date: 		4th June 2020
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# *****************************************************************************
# *****************************************************************************

import os,re,sys
#
#		Scan source to build keyword->label hash
#
keywords = {}
for root,dirs,files in os.walk("."):
	for f in [x for x in files if x.endswith(".asm")]:
		for l in open(root+os.sep+f).readlines():
			if l.find(";;") >= 0:
				m = re.match("^(.*?)\\:\\s+\\;\\;\\s*(.*)\\s*$",l)
				keyword = m.group(2).strip().lower()
				assert keyword not in keywords,"Duplicate "+keyword
				keywords[keyword] = m.group(1).strip()
#
#		Scan label file to get the physical address/values
#
labels = {}
for l in open("sour16.lbl").readlines():
	m = re.match("^(.*?)\\s*\\=\\s*(.*?)$",l)
	assert m is not None,"Label syntax"+l
	addr = m.group(2)
	labels[m.group(1)] = int(addr[1:],16) if addr[0] == '$' else int(addr)
#
#		Check keywords have a label value
#
for k in keywords:
	assert keywords[k] in labels,"No label for "+k
#
#		Generate Python constants for Sour16 class
#
constants = {}
disasm = {}
for k in keywords.keys():
	code = labels[keywords[k]]-labels["Sour16Base"]
	if k.startswith("["):
		constants[k] = labels[keywords[k]]
	else:
		opcode = (code & 0xF0) if code >= 256 else (code >> 4)
		constants[k.split()[0]] = opcode
		disasm[opcode] = k
#		
constants["loadaddr"] = labels["Sour16Base"]
#
#		Load the runtime as a binary
#
runTime = bytes(open("sour16.prg","rb").read(-1))[2:]
#
#		Output Runtime a Python class.
#
routines = {}
keys = [x for x in constants.keys()]
keys.sort(key = lambda x:constants[x])
h = open("sour16.py","w")
h.write("#\n#\tAutomatically generated.\n#\n")
h.write("class Sour16(object):\n\tpass\n\n")
for k in keys:
	s = k
	show = True
	if k.startswith("["):
		s = "X_"+k[1:-1] 
		if s[-1] >= '0' and s[-1] <= '9':
			routines[k[1:-1]] = constants[k]
			show = False
	if k == "loadaddr":
		h.write("\n")	
	if show:
		h.write("Sour16.{0} = 0x{1:02x}\n".format(s.upper(),constants[k]))

h.write("\nSour16.DECODE = {0}\n".format(str(disasm)))
r = ",".join(['"{0}":0x{1:04x}'.format(r,routines[r]) for r in routines.keys()])
h.write("\nSour16.ROUTINES = {{	 {0} }}\n".format(r))
h.write("\nSour16.RUNTIME = [ {0} ]\n".format(",".join(["0x{0:02x}".format(c) for c in runTime])))
h.close()
#
#		Create the code Generator wrapper class
#
h = open("codegen.py","w")
h.write("#\n#\tAutomatically generated wrapper class for code generator.\n#\n")
h.write("import sys\n")
h.write("class CodeGen(object):\n")
h.write("\tdef __init__(self,codeGen):\n")
h.write("\t\tself.cg = codeGen\n")
#
#		These are methods exported from the Code Generator Base Class in the compiler.
#		(You manually copy these in)
#
export = """
	def allocUninitialised(self,size):
	def writeDataMemory(self,data):
	def setExecuteAddress(self,address):
	def write(self,address,data):
	def assemble(self,opcode,operandSize = 0,operand = None):
	def setListHandle(self,handle = sys.stdout):
	def getCodePointer(self):
	def updateFreeMemory(self):
	def writeProgram(self,fileName):
""".strip().split(":")

for d in [x.strip() for x in export if x.strip() != ""]:
	m = re.match("^def\\s*(.*?)\\((.*?)\\)$",d)
	p = [x.split("=")[0].strip() for x in m.group(2).split(",")]
	assert m is not None
	h.write("\t{0}:\n".format(d))
	h.write("\t\treturn self.cg.{0}({1})\n".format(m.group(1),",".join(p[1:])))

for k in disasm.keys():
	parameters = []
	mnemonic = disasm[k]
	paramCount = 0
	opcode = "0x{0:02x}".format(k)
	if mnemonic.find("@") >= 0:
		parameters.append("reg")
		opcode = opcode + "+reg"
	if mnemonic.find("+") >= 0 or mnemonic.find("%") >= 0:
		paramCount = 1
		parameters.append("operand")		
	if mnemonic.find("#") >= 0:
		parameters.append("operand")
		paramCount = 2
	h.write("\tdef c_{0}(self,{1}):\n".format(mnemonic.split()[0],",".join(parameters)))
	h.write("\t\treturn self.cg.assemble({0},{1}{2})\n".format(opcode,paramCount,"" if paramCount == 0 else ",operand"))

h.write("\t")
h.close()
