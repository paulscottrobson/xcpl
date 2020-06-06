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

;
;		These routines generally pass the level into RF, so if RF = 4
;		The register involved is R4, or R4/R5.
;

CodeOpcode = (CallMachineCode-Sour16Base) >> 4

; *****************************************************************************
;
;									Multiply
;
; *****************************************************************************

Multiply:		;; [MULTIPLY]
		.byte 	CodeOpcode
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
		rts

; *****************************************************************************
;
;									Negate
;
; *****************************************************************************

Negate:		;; [NEGATE]
		.byte 	CodeOpcode
		tax 								; save Base in X.
		clc
		adc 	15*2,X 						; add the base register in RF to it
		adc	 	15*2,X 						; twice.
		tax 	
		;
		sec
		lda 	#0
		sbc 	0,x
		sta 	0,x
		lda 	#0
		sbc 	1,x
		sta 	1,x
		rts

; *****************************************************************************
;
;								Divide/Modulus
;
; *****************************************************************************

Divide:		;; [DIVIDE]
		.byte 	CodeOpcode
		sec
		bra 	DivideModulus
Modulus:	;; [MODULUS]
		.byte 	CodeOpcode
		clc
DivideModulus:
		php

		tax 								; save Base in X.
		clc
		adc 	15*2,X 						; add the base register in RF to it
		adc	 	15*2,X 						; twice.
		tax 	
		;
		;	Q/Dividend/Left in 0,X and 1,X
		;	M/Divisor/Right in 2,X and 3,X
		; 	A is temp0
		;
		phy 								; Y is the iteration counter
		ldy 	#16
		stz 	temp0 						; zero A
		stz 	temp0+1
_DivideLoop:		
		asl 	0,x 						; shift AQ left
		rol 	1,x
		rol 	temp0
		rol 	temp0+1
		;
		sec
		lda 	temp0 						; do A-M calculation
		sbc 	2,x 					
		pha 								; saved on stack
		lda 	temp0+1
		sbc 	3,x
		bcc 	_DivideNoAdd 
		;
		sta 	temp0+1 					; A-M >= 0
		pla 								; so save the subtraction
		sta 	temp0
		inc		0,x 						; set the LSB
		bra 	_DivideNext
		;
_DivideNoAdd:
		pla 								; throw the interim result
_DivideNext:
		dey 								; do the correct number of iterations
		bne 	_DivideLoop
		ply 								; restore Y
		;
		plp 								; return div (CS) mod (CC)
		bcs 	_DivideExit

		lda 	temp0
		sta 	0,x
		lda 	temp0+1
		sta 	1,x

_DivideExit:		
		rts				