; *****************************************************************************
; *****************************************************************************
;
;		Name:		sourrun.asm
;		Purpose:	Execution code
;		Date: 		4th June 2020
;		Author:		Paul Robson (paul@robsons.org.uk)
;
; *****************************************************************************
; *****************************************************************************

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

		lda 	StartUninitialised 			; erase uninitialised data.
		sta 	temp0
		lda 	StartUninitialised+1
		sta 	temp0+1
RPClearMem:
		lda 	EndUninitialised 			; check reached end
		cmp 	temp0
		bne 	RPEraseNext
		lda 	EndUninitialised+1
		cmp 	temp0+1
		beq 	Sour16Next 					; reached end, exit.
RPEraseNext:		
		lda 	#0 							; clear meemory.
		sta 	(temp0)
		inc 	temp0 						; go to next byte
		bne 	RPClearMem
		inc 	temp0+1
		bra 	RPClearMem

; *****************************************************************************
;
;					Return here to execute next command
;
; *****************************************************************************

Sour16NextSkip2:							; come back here to skip word operand
		clc
		lda 	pctr
		adc 	#2
		sta 	pctr
		bcc 	Sour16Next
		inc 	pctr+1

Sour16Next:									; come back here for next.
		lda 	(pctr) 						; get the opcode 
		inc 	pctr 						; skip the opcode.
		bne 	Sour16NoCarry
		inc 	pctr+1
Sour16NoCarry:		
		tax 								; save in X
		and 	#$F0
		sta 	S16NJmp+1 					; modify the jump address
		txa 			 					; get the opcode back from X
		and 	#15 						; index into the register block.
		asl 	a 							; (reg# x 2) is also in A. 
		tax
S16NJmp:
		jmp 	Sour16RootCommandSet

