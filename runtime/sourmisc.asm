; *****************************************************************************
; *****************************************************************************
;
;		Name:		sourmisc.asm
;		Purpose:	Sour16 Miscellaneous functions
;		Date: 		4th June 2020
;		Author:		Paul Robson (paul@robsons.org.uk)
;
; *****************************************************************************
; *****************************************************************************

; *****************************************************************************
;
;							Conditional Tests
;					  (Set -1 if true, 0 if false)
;
; *****************************************************************************

TestVariable = Vars+2 						; we test on R1

		.align 	16
TestZero:				;; TZERO
		lda 	TestVariable		
		ora 	TestVariable+1
		beq 	TestTrue
TestFalse:
		stz 	TestVariable
		stz 	TestVariable+1
		jmp 	Sour16Next

		.align 	16
TestNonZero:			;; TNONZERO
		lda 	TestVariable		
		ora 	TestVariable+1
		beq 	TestFalse
TestTrue:
		lda 	#$FF		
		sta 	TestVariable
		sta 	TestVariable+1
		jmp 	Sour16Next

		.align 	16
TestNegative:			;; TMINUS
		lda 	TestVariable+1
		bmi 	TestTrue
		bra 	TestFalse

		.align 	16
TestPlus:				;; TPLUS
		lda 	TestVariable+1
		bpl 	TestTrue
		bra 	TestFalse

; *****************************************************************************
;
;							Conditional Branches
;					  (offset follows, set Y if false)
;
; *****************************************************************************

		.align 	16
BranchZero:				;; BRZERO +
		lda 	TestVariable		
		ora 	TestVariable+1
		beq 	BranchTrue
		bra 	BranchFalse

		.align 	16
BranchNonZero:			;; BRNONZERO +
		lda 	TestVariable		
		ora 	TestVariable+1
		bne 	BranchTrue
		bra 	BranchFalse

		.align 	16
BranchMinus:			;; BRMINUS +
		lda 	TestVariable+1	
		bmi 	BranchTrue
BranchFalse:
		inc 	pctr
		bcc 	BranchFalseNoCarry
		inc 	pctr+1
BranchFalseNoCarry:
		jmp 	Sour16Next

		.align 	16
BranchPlus:				;; BRPLUS +
		lda 	TestVariable+1	
		bmi 	BranchFalse
		bra 	BranchTrue

		.align 	16
BranchTrue:		;; BR +
		ldx 	#0 							; X is the sign extended offset
		lda 	(pctr) 						; get offset
		bpl 	BTPositive
		dex 								; if -ve make sign extended 255
BTPositive:
		clc 								; add to PCTR
		adc 	pctr 
		sta 	pctr
		;
		txa 
		adc 	pctr+1
		sta 	pctr+1
		jmp 	Sour16Next

; *****************************************************************************
;
;								Call subroutine
;
; *****************************************************************************

		.align 	16
CallSubroutine: 		;; CALL #
		lda 	pctr+1 						; save PCTR Hi
		pha
		lda 	pctr 						; save PCTR Lo
		pha
		lda 	(pctr) 						; read new PC low into X
		tax
		ldy 	#1
		lda 	(pctr),y 					; read new PC high into A
		sta 	pctr+1 						; update address
		stx 	pctr
		jmp 	Sour16Next 					; and execute from there.


; *****************************************************************************
;
;							Call following machine code.
;
;	This calls the code following the opcode, and when that code returns
;	it does a Subroutine Return.
;
; *****************************************************************************

		.align 	16
CallMachineCode:
		lda 	#Vars 						; address of variables in A
		jsr 	MachineCodeCaller 			; call the calling code.
		bra 	ReturnSubroutine 			; and do the return code.

; *****************************************************************************
;
;								Return code
;
; *****************************************************************************

		.align 	16
ReturnSubroutine:	;; RET
		pla 								; restore PC
		sta 	pctr
		pla 			
		sta 	pctr+1
		jmp 	Sour16NextSkip2 			; return, skipping the code.

; *****************************************************************************
;
;					Handler for miscellaneous code
;
; *****************************************************************************

MachineCodeCaller:
		jmp 	(pctr)

		* = Sour16Base+$F7

MiscellaneousHandler:
		asl 	a 							; on entry, 2 x the LSNibble of the word
		asl 	a 							; x 4
		asl 	a 							; x 16
		sta 	MHAddress+1 				; make the LSB of the jump address
MHAddress:		
		jmp 	MiscellaneousHandler

