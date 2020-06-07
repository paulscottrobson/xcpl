#
#	Automatically generated.
#
class Sour16(object):
	pass

Sour16.BRZ = 0x01
Sour16.BRNZ = 0x02
Sour16.BR = 0x03
Sour16.CALL = 0x05
Sour16.RET = 0x08
Sour16.LDI = 0x10
Sour16.ADD = 0x20
Sour16.SUB = 0x30
Sour16.AND = 0x40
Sour16.ORR = 0x50
Sour16.XOR = 0x60
Sour16.SBI = 0x70
Sour16.LWI = 0x80
Sour16.LBI = 0x90
Sour16.SHF = 0xa0
Sour16.LDR = 0xb0
Sour16.SIA = 0xd0

Sour16.LOADADDR = 0x1000
Sour16.X_MULTIPLY = 0x122c
Sour16.X_NEGATE = 0x1262
Sour16.X_DIVIDE = 0x1278
Sour16.X_MODULUS = 0x127c

Sour16.DECODE = {1: 'brz +', 2: 'brnz +', 3: 'br +', 5: 'call #', 8: 'ret', 16: 'ldi @,#', 32: 'add @', 48: 'sub @', 64: 'and @', 80: 'orr @', 96: 'xor @', 112: 'sbi @', 128: 'lwi @', 144: 'lbi @', 160: 'shf @', 176: 'ldr @,#', 208: 'sia @'}

Sour16.RUNTIME = [ 0x4c,0xfc,0x11,0xea,0x00,0x00,0x00,0x00,0xbb,0x12,0x00,0x00,0x00,0x00,0x00,0x00,0xa5,0x0a,0x05,0x0b,0xf0,0x1a,0x80,0x0e,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xa5,0x0a,0x05,0x0b,0xd0,0x0a,0xe6,0x28,0x90,0x02,0xe6,0x29,0x4c,0x16,0x12,0x00,0xa2,0x00,0xb2,0x28,0x10,0x01,0xca,0x18,0x65,0x28,0x85,0x28,0x8a,0x65,0x29,0x85,0x29,0x4c,0x16,0x12,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xa5,0x29,0x48,0xa5,0x28,0x48,0xb2,0x28,0xaa,0xa0,0x01,0xb1,0x28,0x85,0x29,0x86,0x28,0x4c,0x16,0x12,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xa9,0x08,0x20,0x89,0x10,0x80,0x09,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x68,0x85,0x28,0x68,0x85,0x29,0x4c,0x0b,0x12,0x6c,0x28,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x0a,0x0a,0x0a,0x8d,0xfe,0x10,0x4c,0xf7,0x10,0x80,0xf5,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xb2,0x28,0x95,0x08,0xa0,0x01,0xb1,0x28,0x95,0x09,0x4c,0x0b,0x12,0x00,0x00,0x00,0x18,0xb5,0x08,0x75,0x0a,0x95,0x08,0xb5,0x09,0x75,0x0b,0x95,0x09,0x4c,0x16,0x12,0x38,0xb5,0x08,0xf5,0x0a,0x95,0x08,0xb5,0x09,0xf5,0x0b,0x95,0x09,0x4c,0x16,0x12,0xb5,0x08,0x35,0x0a,0x95,0x08,0xb5,0x09,0x35,0x0b,0x95,0x09,0x4c,0x16,0x12,0x00,0xb5,0x08,0x15,0x0a,0x95,0x08,0xb5,0x09,0x15,0x0b,0x95,0x09,0x4c,0x16,0x12,0x00,0xb5,0x08,0x55,0x0a,0x95,0x08,0xb5,0x09,0x55,0x0b,0x95,0x09,0x4c,0x16,0x12,0x00,0xb5,0x08,0x92,0x08,0x4c,0x16,0x12,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x8e,0x84,0x11,0xa0,0x01,0xb1,0x00,0xa8,0x80,0x08,0x00,0x00,0x00,0x00,0x00,0x00,0xa0,0x00,0x8e,0x96,0x11,0xb2,0x00,0x95,0x08,0x94,0x09,0x4c,0x16,0x12,0x00,0x00,0xb5,0x0a,0xf0,0x04,0x30,0x4c,0x80,0x40,0x4c,0x16,0x12,0x00,0x00,0x00,0x00,0x00,0xb2,0x28,0x85,0x2a,0xa0,0x01,0xb1,0x28,0x85,0x2b,0xb2,0x2a,0x95,0x08,0xb1,0x2a,0x95,0x09,0x4c,0x0b,0x12,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xb5,0x08,0x92,0x08,0xb5,0x09,0xa0,0x01,0x91,0x08,0x18,0xa5,0x08,0x69,0x02,0x85,0x08,0x90,0x02,0xe6,0x09,0x4c,0x0b,0x12,0x16,0x08,0x36,0x09,0x3a,0xd0,0xf9,0x4c,0x16,0x12,0x56,0x09,0x76,0x08,0x1a,0xd0,0xf9,0x4c,0x16,0x12,0xa2,0xff,0x9a,0xad,0x04,0x10,0x85,0x28,0xad,0x05,0x10,0x85,0x29,0x80,0x0b,0x18,0xa5,0x28,0x69,0x02,0x85,0x28,0x90,0x02,0xe6,0x29,0xb2,0x28,0xe6,0x28,0xd0,0x02,0xe6,0x29,0xaa,0x29,0xf0,0x8d,0x2a,0x12,0x8a,0x29,0x0f,0x0a,0xaa,0x4c,0x00,0x11,0x07,0xaa,0x18,0x75,0x1e,0x75,0x1e,0xaa,0x64,0x2a,0x64,0x2b,0xb5,0x00,0x29,0x01,0xf0,0x0d,0x18,0xa5,0x2a,0x75,0x02,0x85,0x2a,0xa5,0x2b,0x75,0x03,0x85,0x2b,0x56,0x01,0x76,0x00,0x16,0x02,0x36,0x03,0xb5,0x00,0x15,0x01,0xd0,0xdf,0xa5,0x2a,0x95,0x00,0xa5,0x2b,0x95,0x01,0x60,0x07,0xaa,0x18,0x75,0x1e,0x75,0x1e,0xaa,0x38,0xa9,0x00,0xf5,0x00,0x95,0x00,0xa9,0x00,0xf5,0x01,0x95,0x01,0x60,0x07,0x38,0x80,0x02,0x07,0x18,0x08,0xaa,0x18,0x75,0x1e,0x75,0x1e,0xaa,0x5a,0xa0,0x10,0x64,0x2a,0x64,0x2b,0x16,0x00,0x36,0x01,0x26,0x2a,0x26,0x2b,0x38,0xa5,0x2a,0xf5,0x02,0x48,0xa5,0x2b,0xf5,0x03,0x90,0x09,0x85,0x2b,0x68,0x85,0x2a,0xf6,0x00,0x80,0x01,0x68,0x88,0xd0,0xdf,0x7a,0x28,0xb0,0x08,0xa5,0x2a,0x95,0x00,0xa5,0x2b,0x95,0x01,0x60 ]
