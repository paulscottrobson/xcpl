# *****************************************************************************
# *****************************************************************************
#
#		Name:		expression.py
#		Purpose:	Expression compiler
#		Date: 		6th June 2020
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# *****************************************************************************
# *****************************************************************************

from error import *
from xparser import *
from codegen import *
from ident import *
from x16codegen import *
from types import *
from term import *
from sour16 import *

# *****************************************************************************
#
#						Expression compiler worker class
#
# *****************************************************************************
#
class ExpressionCompiler(object):
	def __init__(self,codeGenerator,identStore):
		self.cg = codeGenerator
		self.identStore = identStore
	#
	#		Compile an expression at the given level from the given stream.
	#
	def compile(self,stream,regLevel,termCompiler):
		return [0,0]
	#
	#		Test routine. 
	#
	def test(self,stream,termCompiler):
		s = stream.get()
		stream.put(s)
		print("\n*********** "+s+" ***********")
		self.cg.setListHandle()							
		r = self.compile(stream,2,termCompiler)				
		print("\nReturns [VType.{0}{1}]".format(VType.TOSTRING[r[0]],
								",${0:04x}".format(r[1]) if len(r) == 2 else ""))
		print("Complete-->")
		termCompiler.convertToValue(r,2)

if __name__ == "__main__":
	codeGen = CodeGen(X16CodeGen(1024,1024))		
	idStore = TestIdentStore()
	tc = TermCompiler(codeGen,idStore)				
	ec = ExpressionCompiler(codeGen,idStore)

	stream = TextParser("""
		42
	""".split("\n"))
	for i in range(0,1):
		ec.test(stream,tc)
