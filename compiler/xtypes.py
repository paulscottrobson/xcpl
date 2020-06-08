# *****************************************************************************
# *****************************************************************************
#
#		Name:		xtypes.py
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

VType.TOSTRING = [ "Const","Value","VarRef","ByteRef","WordRef"]
