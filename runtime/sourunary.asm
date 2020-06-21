; *****************************************************************************
; *****************************************************************************
;
;		Name:		sourunary.asm
;		Purpose:	Sour16 unary routines
;		Date: 		21st June 2020
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
;								String Length
;
; *****************************************************************************

StringLength:	;; [unarystrlen1]
		.byte 	CodeOpcode
		tax 								; save Base in X.
		clc
		adc 	15*2,X 						; add the base register in RF to it
		adc	 	15*2,X 						; twice.
		tax 	

		lda 	0,x 						; string pos to temp0
		sta 	temp0
		lda 	1,x 			
		sta 	temp0+1

		ldy 	#255 						; get length (max 255)
_SLLoop:
		iny 								; pre increment
		lda 	(temp0),y		
		bne 	_SLLoop
		sty 	0,x 						; write result out and exit.
		stz 	1,x
		rts

; *****************************************************************************
;
;								Absolute value
;
; *****************************************************************************

Absolute:	 ;; [unaryabs1]		
		.byte 	CodeOpcode
		tax 								; save Base in X.
		clc
		adc 	15*2,X 						; add the base register in RF to it
		adc	 	15*2,X 						; twice.
		tax 	
		bit 	1,x
		bpl 	_AbsExit
		sec
		lda 	#0							; negate
		sbc 	0,x
		sta 	0,x
		lda 	#0
		sbc 	1,x
		sta 	1,x
_AbsExit:		
		rts

; *****************************************************************************
;
;								Sign of value
;
; *****************************************************************************

SignInteger:	 ;; [unarysign1]		
		.byte 	CodeOpcode
		tax 								; save Base in X.
		clc
		adc 	15*2,X 						; add the base register in RF to it
		adc	 	15*2,X 						; twice.
		tax 	

		ldy 	#0 							; return value
		lda 	0,x
		ora		1,x
		beq 	_SIWrite 					; 0 if zero
		dey  								; now return -1
		bit 	1,x 						; if -ve return that
		bmi 	_SIWrite
		stz 	1,x 						; return 1
		lda 	#1
		sta 	0,x
		rts

_SIWrite:
		sty 	0,x
		sty 	1,x
		rts		

; *****************************************************************************
;
;								Random Integer
;
; *****************************************************************************

RndInteger:	 ;; [unaryrandom1]		
		.byte 	CodeOpcode
		tax 								; save Base in X.
		clc
		adc 	15*2,X 						; add the base register in RF to it
		adc	 	15*2,X 						; twice.
		tax 	

		lda 	0,x 						; seed cannot be zero
		ora 	1,x
		bne 	_RINotZero
		dec 	0,x
_RINotZero:

		lda 	1,x 						; 16 bit xorshift rng
		lsr 	a
		lda 	0,x
		ror 	a
		eor 	1,x
		sta 	1,x 
		ror 	a
		eor 	0,x
		sta 	0,x 
		eor 	1,x
		sta 	1,x 
		rts