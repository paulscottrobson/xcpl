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
;									Multiply
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

