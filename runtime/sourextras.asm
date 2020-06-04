; *****************************************************************************
; *****************************************************************************
;
;		Name:		sourextras.asm
;		Purpose:	Support routine
;		Date: 		4th June 2020
;		Author:		Paul Robson (paul@robsons.org.uk)
;
; *****************************************************************************
; *****************************************************************************

CodeOpcode = (CallMachineCode-Sour16Base) >> 4

; *****************************************************************************
;
;								Multiply
;
; *****************************************************************************

Multiply:		;; [MULTIPLY]
		.byte 	CodeOpcode
		.byte 	$FF

		tax 								; save Base in X.
		clc
		adc 	15*2,X 						; add the base register in RF to it
		adc	 	15*2,X 						; twice.
		tax 	
		;
		stz 	temp0 						; clear result
		stz 	temp0+1

_MultLoop:
		lda 	0,X 						; check LSB of lower byte
		and 	#1
		beq 	_MultNoAdd

		clc 								; add in.
		lda 	temp0
		adc 	2,x
		sta 	temp0
		lda 	temp0+1
		adc 	3,x
		sta 	temp0+1

_MultNoAdd:
		lsr 	1,x 						; shift one right and one left
		ror 	0,x
		asl 	2,x
		rol 	3,x
		;
		lda 	0,x 						; check if done
		ora 	1,x
		bne 	_MultLoop

		lda 	temp0 						; copy result back.
		sta 	0,x
		lda 	temp0+1
		sta 	1,x

		.byte 	$FF
		rts

