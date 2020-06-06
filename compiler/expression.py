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
	#		Does not convert to a final value.
	#
	def compile(self,stream,regLevel,termCompiler):
		firstTerm = stream.get()
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
#
#		This is the precedence level of the operators.
#
ExpressionCompiler.OPERATORS = {
	"&":1,	"|":1,	"^":1,
	"<":2,	"<=":2,	">":2,	">=":2,	"==":2,	"<>":2,
	"+":3,	"-":3,
	"*":4,	"/":4,	">>":4,	"<<":4,
	"!":5,	"?":5
}

if __name__ == "__main__":
	codeGen = CodeGen(X16CodeGen(1024,1024))		
	idStore = TestIdentStore()
	tc = TermCompiler(codeGen,idStore)				
	ec = ExpressionCompiler(codeGen,idStore)

	src = """
		42
		count
		""
	""".strip().split("\n")

	stream = TextParser(src)
	for i in range(0,len(src)):
		ec.test(stream,tc)
