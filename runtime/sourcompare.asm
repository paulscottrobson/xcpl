; *****************************************************************************
; *****************************************************************************
;
;		Name:		sourcompare.asm
;		Purpose:	Support routines (comparison)
;		Date: 		8th June 2020
;		Author:		Paul Robson (paul@robsons.org.uk)
;
; *****************************************************************************
; *****************************************************************************

;
;		These routines generally pass the level into RF, so if RF = 4
;		The register involved is R4, or R4/R5.
;

; *****************************************************************************
;
;								Equality/Difference
;
; *****************************************************************************

Equals:		;; [EQUAL]
		.byte 	CodeOpcode
		clc 								; clc keeps the result, sec inverts it
		bra 	EqualMain
NotEqual: 	;; [NOTEQUAL]
		.byte 	CodeOpcode
		sec
EqualMain:
		php 								; save flip bit
		tax 								; save Base in X.
		clc
		adc 	15*2,X 						; add the base register in RF to it
		adc	 	15*2,X 						; twice.
		tax 	
		;
		lda		0,X 						; check if equals.
		cmp 	2,X
		bne 	CondFail
		lda 	1,x
		cmp 	3,x
		bne 	CondFail
;
;		Deal with true or false.	
;		
CondSucceed:
		lda 	#$FF 						; return true.
		plp
		bcc 	CondSaveExit
		lda 	#$00						; if flip return 00
CondSaveExit:
		sta 	0,x 						; write out 0 or -1
		sta 	1,x
		rts

CondFail:
		lda 	#$00 						; return false.
		plp
		bcc 	CondSaveExit
		lda 	#$FF
		bra 	CondSaveExit

; *****************************************************************************
;
;								GreaterEqual / Less
;
; *****************************************************************************

GreaterEquals:		;; [GREATEREQUAL]
		.byte 	CodeOpcode
		clc 								; clc keeps the result, sec inverts it
		bra 	GEqualMain
Less: 				;; [LESS]
		.byte 	CodeOpcode
		sec
GEqualMain:
		php 								; save flip bit
		tax 								; save Base in X.
		clc
		adc 	15*2,X 						; add the base register in RF to it
		adc	 	15*2,X 						; twice.
		tax 	

		sec 								; do the comparison
		lda 	0,X 	
		sbc 	2,x
		lda 	1,x
		sbc		3,x
		bcs 	CondSucceed 				; >= true
		bra 	CondFail 					; < false

; *****************************************************************************
;
;								Greater / LessEqual
;
; *****************************************************************************

Greater:		;; [GREATER]
		.byte 	CodeOpcode
		clc 								; clc keeps the result, sec inverts it
		bra 	GMain
LessEqual: 				;; [LESSEQUAL]
		.byte 	CodeOpcode
		sec
GMain:
		php 								; save flip bit
		tax 								; save Base in X.
		clc
		adc 	15*2,X 						; add the base register in RF to it
		adc	 	15*2,X 						; twice.
		tax 	

		sec 								; do the comparison
		lda 	2,X 	
		sbc 	0,x
		lda 	3,x
		sbc		1,x
		bcc 	CondSucceed 				; >= true
		bra 	CondFail 					; < false
