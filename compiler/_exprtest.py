# *****************************************************************************
# *****************************************************************************
#
#		Name:		_exprtest.py
#		Purpose:	Expression test routine
#		Date: 		7th June 2020
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# *****************************************************************************
# *****************************************************************************

import re
from codegen import *
from ident import *
from x16codegen import *
from term import *
from sour16 import *
from expression import *

codeGen = CodeGen(X16CodeGen(1024,1024))		
idStore = TestIdentStore()
tc = TermCompiler(codeGen,idStore)				
ec = ExpressionCompiler(codeGen,idStore)

src = """
		12345+1000 => 13345
		12345-1000 => 11345
		12345&7531 => 4137
		12345^7531 => 11602
		12345|7531 => 15739
		12345<<2 => 49380
""".strip().split("\n")
src = [x.strip() for x in src if x.strip() != ""]
for i in range(0,len(src)):
	m = re.match("^\\s*(.*?)\\s*\\=\\>\\s*(.*?)\\s*$",src[i])
	assert m is not None,src[i]
	src[i] = "("+m.group(1)+")-"+m.group(2)

codeStart = codeGen.getCodePointer()
print("Code starts at ${0:04x}".format(codeStart))
codeGen.setExecuteAddress(codeStart)

stream = TextParser(src)
for i in range(0,len(src)):
	ec.test(stream,tc)
	codeGen.c_chz()
print("Patch XEQ ; JMP $FFFF")
codeGen.c_xeq()
p = codeGen.getCodePointer()
codeGen.c_lcw(0,0xFFFF)
codeGen.write(p,0x4C)
print("Code ends at ${0:04x}".format(codeGen.getCodePointer()))
codeGen.writeProgram("test.prg")
# TO Check: + - & | ^ <<