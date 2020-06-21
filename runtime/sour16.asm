; *****************************************************************************
; *****************************************************************************
;
;		Name:		sour16.asm
;		Purpose:	Sour16 is the XCPL Runtime
;					It borrows some ideas, not code, from Apple ][ Sweet 16.
;					(It is useless as a general purpose 16 bit VM)
;		Date: 		4th June 2020
;		Author:		Paul Robson (paul@robsons.org.uk)
;
; *****************************************************************************
; *****************************************************************************

		* = $08

Vars:	.fill 	16*2 						; registers in low/high byte pairs
pctr:	.fill 	2							; address of current routine.
temp0:	.fill 	2

; *****************************************************************************
;
;								Entry point
;
; *****************************************************************************

		* = 	$1000
Sour16Base:		 							; starts with jump to run code/
		jmp 	RunProgram
		nop 								; pad to 4 bytes.

StartVector:								; +4 is the start of the Sour16 code.
		.word 	0,0 					
HighMemory:									; +8 is the first free byte.
		.word 	Sour16End
StartUninitialised:							; +10 is the start of uninitialised memory
		.word 	0
EndUninitialised:							; +12 is the end of uninitialised memory
		.word 	0

		.include 	"sourmisc.asm"			; miscellaneous functions.
		.include 	"sourcore.asm"			; core operations
		.include 	"sourrun.asm" 			; main execution functions
		.include	"sourmath.asm" 			; arithmetic
		.include 	"sourcompare.asm"		; comparisons
		.include 	"sourunary.asm"			; unary functions.
		.include 	"sourdebug.asm"			; debug helper stuff.		

Sour16End:

; Expr returns : Reference, Calculated value, Constant (one only), Test Result.
; Code passes base address of registers in A.


