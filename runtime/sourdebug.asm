; *****************************************************************************
; *****************************************************************************
;
;		Name:		sourdebug.asm
;		Purpose:	Support routines (debugging)
;		Date: 		4th June 2020
;		Author:		Paul Robson (paul@robsons.org.uk)
;
; *****************************************************************************
; *****************************************************************************

DebugPrintChar:		;; [PRINTCHAR1]
		.byte 	CodeOpcode
		.byte 	$FF
		lda 	Vars+2 						; get R1
		jmp 	$FFD2 						; call output routine