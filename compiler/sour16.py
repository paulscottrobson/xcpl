#
#	Automatically generated.
#
class Sour16(object):
	pass

Sour16.BRZ = 0x01
Sour16.BRNZ = 0x02
Sour16.BR = 0x03
Sour16.CHZ = 0x05
Sour16.CALL = 0x06
Sour16.RET = 0x08
Sour16.XEQ = 0x0f
Sour16.LCW = 0x10
Sour16.LCB = 0x20
Sour16.ADD = 0x30
Sour16.SUB = 0x40
Sour16.AND = 0x50
Sour16.ORR = 0x60
Sour16.XOR = 0x70
Sour16.SBI = 0x80
Sour16.LWI = 0x90
Sour16.LBI = 0xa0
Sour16.SHF = 0xb0
Sour16.LDR = 0xc0
Sour16.SIA = 0xe0

Sour16.LOADADDR = 0x1000
Sour16.X_MULTIPLY = 0x125e
Sour16.X_NEGATE = 0x1294
Sour16.X_DIVIDE = 0x12aa
Sour16.X_MODULUS = 0x12ae
Sour16.X_INCLOAD = 0x12ed
Sour16.X_DECLOAD = 0x12f4
Sour16.X_EQUAL = 0x130b
Sour16.X_NOTEQUAL = 0x130f
Sour16.X_GREATEREQUAL = 0x133a
Sour16.X_LESS = 0x133e
Sour16.X_GREATER = 0x1355
Sour16.X_LESSEQUAL = 0x1359

Sour16.DECODE = {16: 'lcw @,#', 32: 'lcb @,%', 48: 'add @', 64: 'sub @', 80: 'and @', 96: 'orr @', 112: 'xor @', 128: 'sbi @', 144: 'lwi @', 160: 'lbi @', 176: 'shf @', 192: 'ldr @,#', 224: 'sia @', 1: 'brz +', 2: 'brnz +', 3: 'br +', 5: 'chz', 6: 'call #', 8: 'ret', 15: 'xeq'}

Sour16.ROUTINES = {	 "unarystrlen1":0x1370,"unaryabs1":0x138c,"unarysign1":0x13a6,"unaryrandom1":0x13c7,"print.char1":0x13eb,"print.string1":0x13f1,"print.hex1":0x13ff }

Sour16.RUNTIME = [ 0x4c,0x0c,0x12,0xea,0x00,0x00,0x00,0x00,0x22,0x14,0x00,0x00,0x00,0x00,0x00,0x00,0xa5,0x0a,0x05,0x0b,0xf0,0x1a,0x80,0x0e,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xa5,0x0a,0x05,0x0b,0xd0,0x0a,0xe6,0x28,0xd0,0x02,0xe6,0x29,0x4c,0x48,0x12,0x00,0xa2,0x00,0xb2,0x28,0x10,0x01,0xca,0x18,0x65,0x28,0x85,0x28,0x8a,0x65,0x29,0x85,0x29,0x4c,0x48,0x12,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xa5,0x0a,0x05,0x0b,0xf0,0x01,0xff,0x4c,0x48,0x12,0x00,0x00,0x00,0x00,0x00,0x00,0xa5,0x29,0x48,0xa5,0x28,0x48,0xb2,0x28,0xaa,0xa0,0x01,0xb1,0x28,0x85,0x29,0x86,0x28,0x4c,0x48,0x12,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x68,0x85,0x28,0x68,0x85,0x29,0x4c,0x3d,0x12,0x6c,0x28,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xa9,0x08,0x20,0x89,0x10,0x80,0x89,0x0a,0x0a,0x0a,0x8d,0xfe,0x10,0x4c,0xf7,0x10,0x80,0xf5,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xb2,0x28,0x95,0x08,0xa0,0x01,0xb1,0x28,0x95,0x09,0x4c,0x3d,0x12,0x00,0x00,0x00,0xb2,0x28,0x95,0x08,0x74,0x09,0xe6,0x28,0x90,0x02,0xe6,0x29,0x4c,0x48,0x12,0x00,0x18,0xb5,0x08,0x75,0x0a,0x95,0x08,0xb5,0x09,0x75,0x0b,0x95,0x09,0x4c,0x48,0x12,0x38,0xb5,0x08,0xf5,0x0a,0x95,0x08,0xb5,0x09,0xf5,0x0b,0x95,0x09,0x4c,0x48,0x12,0xb5,0x08,0x35,0x0a,0x95,0x08,0xb5,0x09,0x35,0x0b,0x95,0x09,0x4c,0x48,0x12,0x00,0xb5,0x08,0x15,0x0a,0x95,0x08,0xb5,0x09,0x15,0x0b,0x95,0x09,0x4c,0x48,0x12,0x00,0xb5,0x08,0x55,0x0a,0x95,0x08,0xb5,0x09,0x55,0x0b,0x95,0x09,0x4c,0x48,0x12,0x00,0xb5,0x08,0x92,0x08,0x4c,0x48,0x12,0xa0,0x01,0xb1,0x2a,0x95,0x09,0x4c,0x48,0x12,0xb5,0x08,0x85,0x2a,0xb5,0x09,0x85,0x2b,0xb2,0x2a,0x95,0x08,0x80,0xe9,0x00,0x00,0xa1,0x08,0x95,0x08,0x74,0x09,0x4c,0x48,0x12,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xb5,0x0a,0xf0,0x04,0x30,0x4c,0x80,0x40,0x4c,0x48,0x12,0x00,0x00,0x00,0x00,0x00,0xb2,0x28,0x85,0x2a,0xa0,0x01,0xb1,0x28,0x85,0x2b,0xb2,0x2a,0x95,0x08,0xb1,0x2a,0x95,0x09,0x4c,0x3d,0x12,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xb5,0x08,0x92,0x08,0xb5,0x09,0xa0,0x01,0x91,0x08,0x18,0xa5,0x08,0x69,0x02,0x85,0x08,0x90,0x02,0xe6,0x09,0x4c,0x48,0x12,0x16,0x08,0x36,0x09,0x3a,0xd0,0xf9,0x4c,0x48,0x12,0x56,0x09,0x76,0x08,0x1a,0xd0,0xf9,0x4c,0x48,0x12,0xa2,0xff,0x9a,0xad,0x04,0x10,0x85,0x28,0xad,0x05,0x10,0x85,0x29,0xad,0x0a,0x10,0x85,0x2a,0xad,0x0b,0x10,0x85,0x2b,0xad,0x0c,0x10,0xc5,0x2a,0xd0,0x07,0xad,0x0d,0x10,0xc5,0x2b,0xf0,0x17,0xa9,0x00,0x92,0x2a,0xe6,0x2a,0xd0,0xea,0xe6,0x2b,0x80,0xe6,0x18,0xa5,0x28,0x69,0x02,0x85,0x28,0x90,0x02,0xe6,0x29,0xb2,0x28,0xe6,0x28,0xd0,0x02,0xe6,0x29,0xaa,0x29,0xf0,0x8d,0x5c,0x12,0x8a,0x29,0x0f,0x0a,0xaa,0x4c,0x00,0x11,0x0f,0xaa,0x18,0x75,0x1e,0x75,0x1e,0xaa,0x64,0x2a,0x64,0x2b,0xb5,0x00,0x29,0x01,0xf0,0x0d,0x18,0xa5,0x2a,0x75,0x02,0x85,0x2a,0xa5,0x2b,0x75,0x03,0x85,0x2b,0x56,0x01,0x76,0x00,0x16,0x02,0x36,0x03,0xb5,0x00,0x15,0x01,0xd0,0xdf,0xa5,0x2a,0x95,0x00,0xa5,0x2b,0x95,0x01,0x60,0x0f,0xaa,0x18,0x75,0x1e,0x75,0x1e,0xaa,0x38,0xa9,0x00,0xf5,0x00,0x95,0x00,0xa9,0x00,0xf5,0x01,0x95,0x01,0x60,0x0f,0x38,0x80,0x02,0x0f,0x18,0x08,0xaa,0x18,0x75,0x1e,0x75,0x1e,0xaa,0x5a,0xa0,0x10,0x64,0x2a,0x64,0x2b,0x16,0x00,0x36,0x01,0x26,0x2a,0x26,0x2b,0x38,0xa5,0x2a,0xf5,0x02,0x48,0xa5,0x2b,0xf5,0x03,0x90,0x09,0x85,0x2b,0x68,0x85,0x2a,0xf6,0x00,0x80,0x01,0x68,0x88,0xd0,0xdf,0x7a,0x28,0xb0,0x08,0xa5,0x2a,0x95,0x00,0xa5,0x2b,0x95,0x01,0x60,0x0f,0xa9,0x01,0xa2,0x00,0x80,0x04,0x0f,0xa9,0xff,0xaa,0x18,0x72,0x0a,0x92,0x0a,0x48,0x8a,0xa0,0x01,0x71,0x0a,0x91,0x0a,0x85,0x0b,0x68,0x85,0x0a,0x60,0x0f,0x18,0x80,0x02,0x0f,0x38,0x08,0xaa,0x18,0x75,0x1e,0x75,0x1e,0xaa,0xb5,0x00,0xd5,0x02,0xd0,0x12,0xb5,0x01,0xd5,0x03,0xd0,0x0c,0xa9,0xff,0x28,0x90,0x02,0xa9,0x00,0x95,0x00,0x95,0x01,0x60,0xa9,0x00,0x28,0x90,0xf6,0xa9,0xff,0x80,0xf2,0x0f,0x18,0x80,0x02,0x0f,0x38,0x08,0xaa,0x18,0x75,0x1e,0x75,0x1e,0xaa,0x38,0xb5,0x00,0xf5,0x02,0xb5,0x01,0xf5,0x03,0xb0,0xd2,0x80,0xdc,0x0f,0x18,0x80,0x02,0x0f,0x38,0x08,0xaa,0x18,0x75,0x1e,0x75,0x1e,0xaa,0x38,0xb5,0x02,0xf5,0x00,0xb5,0x03,0xf5,0x01,0x90,0xb7,0x80,0xc1,0x0f,0xaa,0x18,0x75,0x1e,0x75,0x1e,0xaa,0xb5,0x00,0x85,0x2a,0xb5,0x01,0x85,0x2b,0xa0,0xff,0xc8,0xb1,0x2a,0xd0,0xfb,0x94,0x00,0x74,0x01,0x60,0x0f,0xaa,0x18,0x75,0x1e,0x75,0x1e,0xaa,0x34,0x01,0x10,0x0d,0x38,0xa9,0x00,0xf5,0x00,0x95,0x00,0xa9,0x00,0xf5,0x01,0x95,0x01,0x60,0x0f,0xaa,0x18,0x75,0x1e,0x75,0x1e,0xaa,0xa0,0x00,0xb5,0x00,0x15,0x01,0xf0,0x0c,0x88,0x34,0x01,0x30,0x07,0x74,0x01,0xa9,0x01,0x95,0x00,0x60,0x94,0x00,0x94,0x01,0x60,0x0f,0xaa,0x18,0x75,0x1e,0x75,0x1e,0xaa,0xb5,0x00,0x15,0x01,0xd0,0x02,0xd6,0x00,0xb5,0x01,0x4a,0xb5,0x00,0x6a,0x55,0x01,0x95,0x01,0x6a,0x55,0x00,0x95,0x00,0x55,0x01,0x95,0x01,0x60,0x0f,0xa5,0x0a,0x4c,0xd2,0xff,0x0f,0xa0,0x00,0xb1,0x0a,0xf0,0x06,0x20,0xee,0x13,0xc8,0x80,0xf6,0x60,0x0f,0xa9,0x20,0x20,0xee,0x13,0xa5,0x0b,0x20,0x0c,0x14,0xa5,0x0a,0x48,0x4a,0x4a,0x4a,0x4a,0x20,0x15,0x14,0x68,0x29,0x0f,0xc9,0x0a,0x90,0x02,0x69,0x06,0x69,0x30,0x4c,0xee,0x13 ]
