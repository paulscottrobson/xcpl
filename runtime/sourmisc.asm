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
BranchZero:				;; BZERO
		lda 	TestVariable		
		ora 	TestVariable+1
		beq 	BranchTrue
BranchFalse:
		iny
		jmp 	Sour16Next


		.align 	16
BranchNonZero:			;; BNONZERO
		lda 	TestVariable		
		ora 	TestVariable+1
		beq 	BranchFalse
BranchTrue:
		lda 	(pctr),y
		tay	
		jmp 	Sour16Next

		.align 	16
BranchMinus:			;; BMINUS
		lda 	TestVariable+1	
		bmi 	BranchTrue
		bra 	BranchFalse

		.align 	16
BranchPlus:				;; BPLUS
		lda 	TestVariable+1	
		bmi 	BranchTrue
		bra 	BranchFalse

; *****************************************************************************
;
;								Call subroutine
;
; *****************************************************************************

		.align 	16
CallSubroutine: 		;; CALL #
		phy 								; save offset before incrementing
		lda 	pctr+1 						; save PCTR Hi
		pha
		lda 	pctr 						; save PCTR Lo
		pha
		lda 	(pctr),y 					; read new PC low into X
		tax
		iny
		lda 	(pctr),y 					; read new PC high into A
		sta 	pctr+1 						; update address
		stx 	pctr
		ldy 	#0 							; start of that routine
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
		tya 								; work it out make PCTR the actual address
		clc
		adc 	pctr
		sta 	pctr
		bcc 	CMCNoCarry
		inc 	pctr+1
CMCNoCarry:
		lda 	#Vars 						; address of variables in A
		jsr 	MachineCodeCaller 			; call the calling code.
		nop 								; and fall through to return.

; *****************************************************************************
;
;								Return code
;
; *****************************************************************************

		.align 	16
ReturnSubroutine:
		pla 								; restore PC
		sta 	pctr
		pla 			
		sta 	pctr+1
		ply 								; restore offset
		iny 								; skip over the call address
		iny
		jmp 	Sour16Next

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

