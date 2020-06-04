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
for k in keywords.keys():
	code = labels[keywords[k]]-labels["Sour16Base"]
	if k.startswith("["):
		constants[k] = labels[keywords[k]]
	else:
		constants[k.split()[0]] = (code & 0xF0) if code >= 256 else (code >> 4)
constants["loadaddr"] = labels["Sour16Base"]
constants["endaddr"] = labels["Sour16End"]
#
#		Load the runtime as a binary
#
runTime = bytes(open("sour16.prg","rb").read(-1))[2:]
#
#		Output as a Python class.
#
keys = [x for x in constants.keys()]
keys.sort(key = lambda x:constants[x])
h = open("sour16.py","w")
h.write("#\n#\tAutomatically generated.\n#\n")
h.write("class Sour16(object):\n\tpass\n\n")
for k in keys:
	s = "X_"+k[1:-1] if k.startswith("[") else k
	if k == "loadaddr":
		h.write("\n")
	h.write("Sour16.{0} = 0x{1:02x}\n".format(s.upper(),constants[k]))
h.write("\nSour16.RUNTIME = [ {0} ]\n".format(",".join(["0x{0:02x}".format(c) for c in runTime])))
h.close()