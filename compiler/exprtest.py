# *****************************************************************************
# *****************************************************************************
#
#		Name:		exprtest.py
#		Purpose:	Expression test routine
#		Date: 		7th June 2020
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# *****************************************************************************
# *****************************************************************************

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
		0
""".strip().split("\n")

codeStart = codeGen.getCodePointer()
print("Code starts at ${0:04x}".format(codeStart))
codeGen.setExecuteAddress(codeStart)

stream = TextParser(src)
for i in range(0,len(src)):
	ec.test(stream,tc)
	codeGen.c_chz()
print("")
codeGen.c_lcw(1,-1)
codeGen.c_chz()
print("Code ends at ${0:04x}".format(codeGen.getCodePointer()))
codeGen.writeProgram("test.prg")
# TO Check: + - & | ^ <<