p# *****************************************************************************
# *****************************************************************************
#
#		Name:		types.py
#		Purpose:	Python enumerated types
#		Date: 		6th June 2020
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# *****************************************************************************
# *****************************************************************************

# *****************************************************************************
#
#							Expression/Term return type
#
# *****************************************************************************

class VType(object):
	pass
#
#		A constant integer, which can represent a number, address, string address
#		or character. This value is *not* on the expression register file, so can
#		be optimised e.g. +5 can use ADD Constant rather than Load/Add
#	
VType.CONST = 0
#
#		An evaluated value, stored on the expression register file at the
#		requested point.
#
VType.VALUE = 1
#
#		A variable reference. The value is the address of the variable. This value
#		is not on the expression register file.
#
VType.VARREF = 2
#
#		A general reference. The value, not the address is on the expression register
#		file at the requested point. This can be either a BYTE or a WORD reference.
#		(normally usage is for !x ?x x?y x!y)
#
VType.BYTEREF = 3
VType.WORDREF = 4
#
#		A condition. This is returned after a comparison (>= etc) to indicate that
#		there is an in-progress test state. The value returned is the test to 
#		indicate truth. This can either be used in a condition or converted to a 
#		true or false value depending on its usage.
#
VType.CONDITION = 5

# *****************************************************************************
#
#		 Conditional value. These are ennumerated so -x inverts the test
#
# *****************************************************************************

class Condition(object):
	pass

Condition.ZERO = 1
Condition.NONZERO = -1
Condition.POSITIVE = 2
Condition.NEGATIVE = -2
