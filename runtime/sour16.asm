; *****************************************************************************
; *****************************************************************************
;
;		Name:		sour16.asm
;		Purpose:	Sour16 is the XCPL Runtime
;		Date: 		4th June 2020
;		Author:		Paul Robson (paul@robsons.org.uk)
;
; *****************************************************************************
; *****************************************************************************

		* = $00

Vars:	.fill 	16*2
temp0:	.fill 	2
pctr:	.fill 	2

; *****************************************************************************
;
;								Entry point
;
; *****************************************************************************

		* = 	$1000
Sour16Base:		
		lda 	#TestCode & $FF
		sta 	pctr
		lda 	#TestCode >> 8
		sta 	pctr+1
		ldy 	#0

Sour16Next:
		.byte 	$FF
		lda 	(pctr),y 					; get the opcode 
		and 	#$F0
		sta 	S16NJmp+1 					; modify the jump address
		lda 	(pctr),y  					; get the opcode
		and 	#15 						; point to the register , this value
		asl 	a 							; (reg# x 2) is also in A. 
		tax
		iny 								; skip the opcode.
S16NJmp:
		jmp 	Sour16RootCommandSet


;
;	jsr ret word->byte tests and branches code caller
;

; *****************************************************************************
;
;				Main codes. These are at 16 byte intervals
;
; *****************************************************************************

		* = Sour16Base+$100

Sour16RootCommandSet:
		nop
		.align 	16
		nop
		.align 	16
		nop
		.align 	16
		nop
		.align 	16
		nop
		.align 	16
		nop
		.align 	16
		nop
		.align 	16
		nop
		.align 	16
		nop


; *****************************************************************************
;
;							Load Constant to Register
;
; *****************************************************************************

		.align 	16

Command_LoadConst:		;; LDI @,#
		lda 	(pctr),y 					; copy the first byte in
		sta 	Vars,X
		iny
		lda 	(pctr),y 					; copy the second byte in
		sta 	Vars+1,X
Command_IncYNext:		
		iny
		jmp 	Sour16Next

; *****************************************************************************
;
;							Add Constant to Register
;
; *****************************************************************************

		.align 	16

Command_AddConst:		;; ADI @,#
		clc
		lda 	(pctr),y 					; first calculation, LSB
		adc 	Vars,X
		sta 	Vars,X
		iny
		lda 	(pctr),y 					; second calculation, LSB
		adc 	Vars+1,X
		sta 	Vars+1,X
		bra 	Command_IncYNext			; co-opt the end of load const.

;	*00 	  Misc 
;	*01-04 4 x Arithmetic 
;	*05-07 3 x Logical
;	*08 Save Byte Indirect
;	09 Load Constant
;	0A Add Constant
; 	0B Load Direct
;	0D Store Word Indirect
;	0F Load Word Indirect 


TestCode:
		.byte 	$92,$09,$47
		.byte 	$A2,$FE,$01
		.byte 	$A0,$FF,$FF