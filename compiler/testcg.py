from codegen import *
from x16codegen import *
#
#		Test program for generated code generator
#
cg = CodeGen(X16CodeGen(1024,1024))
cg.assemble(16,2,32765)
cg.assemble(48,0)
cg.assemble(8,1,-2)

cg.c_ldi(0,32765)
cg.c_add(0)
n = cg.c_brplus(2)
