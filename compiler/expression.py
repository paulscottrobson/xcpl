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
		return self.compileAtPrecedenceLevel(0,stream,regLevel,termCompiler)
	#
	def compileAtPrecedenceLevel(self,precedence,stream,regLevel,termCompiler):
		current = termCompiler.compile(stream,regLevel,self)
		operator = stream.get()
		while operator in ExpressionCompiler.OPERATORS and ExpressionCompiler.OPERATORS[operator] > precedence:
			rightSide = self.compileAtPrecedenceLevel(ExpressionCompiler.OPERATORS[operator],stream,regLevel+1,termCompiler)
			current = self.doBinaryCalculation(current,operator,rightSide,regLevel,termCompiler)
			operator = stream.get()
		stream.put(operator)
		return current
	#
	#		Perform a binary operation.
	#
	def doBinaryCalculation(self,current,operator,rightSide,regLevel,termCompiler):
		#
		#		Try short cuts - numeric constants, adding/sub constants, shifts for multiply.
		#
		optimise = self.optimiseCalculation(current,operator,rightSide,regLevel,termCompiler)
		if optimise is not None:
			return optimise
		#
		#		Cannot short cut, so convert the left and right to values
		#
		termCompiler.convertToValue(current,regLevel)
		termCompiler.convertToValue(rightSide,regLevel+1)
		#
		#		Generate the appropriate code and return the value. There are four types here
		#			(i) 	those supported by the opcodes directly (+ - & | ^ <<)
		#			(ii) 	those supported by utility functions (* / %)
		#			(iii)	conditions.
		#			(iv) 	those with special code (>>)
		#
		# BODGE FOR TESTING
		if operator == "-":
			self.cg.c_sub(regLevel)  
		elif operator == "+":
			self.cg.c_add(regLevel)  
		elif operator == "&":
			self.cg.c_and(regLevel)  

		return [VType.VALUE]
	#
	#		Short cut calculations.
	#
	def optimiseCalculation(self,current,operator,rightSide,regLevel,termCompiler):
		return None
	#
	#		Test routine. 
	#
	def test(self,stream,termCompiler):
		s = stream.get()
		stream.put(s)
		print("\n*********** "+s+" ***********")
		self.cg.setListHandle()							
		r = self.compile(stream,1,termCompiler)				
		print("\nReturns [VType.{0}{1}]".format(VType.TOSTRING[r[0]],
								",${0:04x}".format(r[1]) if len(r) == 2 else ""))
		print("Complete-->")
		termCompiler.convertToValue(r,1)
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
		1-(2+3)+4
		a&b+c-d
		count+1
	""".strip().split("\n")

	stream = TextParser(src)
	for i in range(0,len(src)):
		ec.test(stream,tc)
