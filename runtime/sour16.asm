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
		.word 	TestCode,0 					

		.include 	"sourmisc.asm"			; miscellaneous functions.
		.include 	"sourcore.asm"			; core operations
		.include 	"sourrun.asm" 			; main execution functions
		.include	"sourextras.asm" 		; extra functionality

Sour16End:

; Expr returns : Reference, Calculated value, Constant (one only), Test Result.
; Code passes base address of registers in A.


