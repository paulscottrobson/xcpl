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

		* = $00

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

; *****************************************************************************
;
;							Run main program
;
; *****************************************************************************

RunProgram:
		ldx 	#$FF 						; reset stack
		txs
		lda 	StartVector 				; load the initial program counter value.
		sta 	pctr
		lda 	StartVector+1
		sta 	pctr+1
		ldy 	#0

; *****************************************************************************
;
;					Return here to execute next command
;
; *****************************************************************************

Sour16Next:
		.byte 	$FF
		lda 	(pctr),y 					; get the opcode 
		iny 								; skip the opcode.
		tax 								; save in X
		and 	#$F0
		sta 	S16NJmp+1 					; modify the jump address
		txa 			 					; get the opcode back from X
		and 	#15 						; index into the register block.
		asl 	a 							; (reg# x 2) is also in A. 
		tax
S16NJmp:
		jmp 	Sour16RootCommandSet



; 	0x Miscellaneous
;			jsr ret tests and branches code caller

;	1x Load Constant
;	2x Add Constant
; 	3x Add Register
; 	4x Sub Register
; 	5x And Register
; 	6x Or Register
; 	7x Xor Register
;	8x Store byte indirect
; 	9x Load Word Indirect
; 	Ax Load Byte Indirect
; 	Bx Shift bidirectional.
; 	Cx Load Direct
;	Dx Unused (at present)
; 	Ex Store Word Indirect Advance 
;	Fx Unused (at present)

TODO:

Implement:
;	* Misc 
; 	* External Multiply, Divide, Negate.

TestCode:
		.byte 	$10,$E0,$10
		.byte 	$12,$34,$FE
		.byte 	$E2


; Expr returns : Reference, Calculated value, Constant (one only), Test Result.
; Code passes base address of registers in A.


