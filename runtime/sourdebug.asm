; *****************************************************************************
; *****************************************************************************
;
;		Name:		sourdebug.asm
;		Purpose:	Support routines (debugging)
;		Date: 		11th June 2020
;		Author:		Paul Robson (paul@robsons.org.uk)
;
; *****************************************************************************
; *****************************************************************************

; *****************************************************************************
;
;						Debugging console I/O routines
;
; *****************************************************************************

DebugPrintChar:		;; [PRINT.CHAR1]
		.byte 	CodeOpcode
		lda 	Vars+2 						; get R1
OSPrintChar:		
		jmp 	$FFD2 						; call output routine

DebugPrintString: 	;; [PRINT.STRING1]
		.byte 	CodeOpcode
		ldy 	#0
_DPSLoop:
		lda 	(Vars+2),y
		beq 	_DPSExit
		jsr 	OSPrintChar
		iny
		bra 	_DPSLoop
_DPSExit:
		rts

DebugPrintHex:		;; [PRINT.HEX1]
		.byte 	CodeOpcode
		lda 	#' '
		jsr 	OSPrintChar
		lda 	Vars+3
		jsr 	_DPH1
		lda 	Vars+2
_DPH1:	
		pha
		lsr 	a		
		lsr 	a		
		lsr 	a		
		lsr 	a		
		jsr 	_DPH2
		pla
_DPH2:	
		and 	#$0F
		cmp 	#$0A
		bcc 	_DPH3
		adc 	#6
_DPH3:		
		adc 	#48
		jmp 	OSPrintChar
		