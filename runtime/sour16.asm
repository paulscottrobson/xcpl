; *****************************************************************************
; *****************************************************************************
;
;		Name:		sour16.asm
;		Purpose:	Sour16 is the XCPL Runtime
;					It borrows some ideas, not code, from Apple ][ Sweet 16.
;		Date: 		4th June 2020
;		Author:		Paul Robson (paul@robsons.org.uk)
;
; *****************************************************************************
; *****************************************************************************

		* = $00

Vars:	.fill 	16*2 						; registers in low/high byte pairs
pctr:	.fill 	2							; address of current routine.

; *****************************************************************************
;
;								Entry point
;
; *****************************************************************************

		* = 	$1000
Sour16Base:		 							; starts with jump to run code/
		jmp 	RunProgram
		nop

StartVector:								; +4 is the start of the Sour16 code.
		.word 	TestCode,0 					

RunProgram:
		ldx 	#$FF 						; reset stack
		txs
		lda 	StartVector 				; load the initial program counter value.
		sta 	pctr
		lda 	StartVector+1
		sta 	pctr+1
		ldy 	#0

Sour16Next:
		.byte 	$FF
		lda 	(pctr),y 					; get the opcode 
		and 	#$F0
		sta 	S16NJmp+1 					; modify the jump address
		lda 	(pctr),y  					; get the opcode
		and 	#15 						; point to the register , this value
		asl 	a 							; (reg# x 2) is also in A. 
		tax
		iny 								; skip the opcode.
S16NJmp:
		jmp 	Sour16RootCommandSet


;
;	jsr ret word->byte tests and branches code caller
;
		* = $10F0
MiscellaneousHandler:
		.word 	$ABCD

; *****************************************************************************
;
;				Main codes. These are at 16 byte intervals
;
; *****************************************************************************

		* = Sour16Base+$100

Sour16RootCommandSet:

; *****************************************************************************
;
;							Handle Miscellaneous Opcodes
;
; *****************************************************************************

Command_Miscellaneous:
		bra 	MiscellaneousHandler

; *****************************************************************************
;
;							Load Constant to Register
;
; *****************************************************************************

		.align 	16

Command_LoadConst:		;; LDI @,#
		lda 	(pctr),y 					; copy the first byte in
		sta 	Vars,X
		iny
		lda 	(pctr),y 					; copy the second byte in
		sta 	Vars+1,X
Command_IncYNext:		
		iny
		jmp 	Sour16Next

; *****************************************************************************
;
;							Add Constant to Register
;
; *****************************************************************************

		.align 	16

Command_AddConst:		;; ADI @,#
		clc
		lda 	(pctr),y 					; first calculation, LSB
		adc 	Vars,X
		sta 	Vars,X
		iny
		lda 	(pctr),y 					; second calculation, LSB
		adc 	Vars+1,X
		sta 	Vars+1,X
		bra 	Command_IncYNext			; co-opt the end of load const.

; *****************************************************************************
;
;						Add Next Register to Register
;
; *****************************************************************************

		.align 	16

Command_AddRegister:	;; ADD @
		clc
		lda 	Vars,x
		adc 	Vars+2,x
		sta		Vars,x
		lda 	Vars+1,x
		adc 	Vars+3,x
		sta		Vars+1,x
		jmp 	Sour16Next

; *****************************************************************************
;
;						Sub Next Register from Register
;
; *****************************************************************************

		.align 	16

Command_SubRegister:	;; SUB @
		sec
		lda 	Vars,x
		sbc 	Vars+2,x
		sta		Vars,x
		lda 	Vars+1,x
		sbc 	Vars+3,x
		sta		Vars+1,x
		jmp 	Sour16Next

; *****************************************************************************
;
;						And Next Register into Register
;
; *****************************************************************************

		.align 	16

Command_AndRegister:	;; AND @
		lda 	Vars,x
		and 	Vars+2,x
		sta		Vars,x
		lda 	Vars+1,x
		and 	Vars+3,x
		sta		Vars+1,x
		jmp 	Sour16Next

; *****************************************************************************
;
;						Or Next Register into Register
;
; *****************************************************************************

		.align 	16

Command_OrRegister:	;; ORR @
		lda 	Vars,x
		ora 	Vars+2,x
		sta		Vars,x
		lda 	Vars+1,x
		ora 	Vars+3,x
		sta		Vars+1,x
		jmp 	Sour16Next

; *****************************************************************************
;
;						Xor Next Register into Register
;
; *****************************************************************************

		.align 	16

Command_XorRegister:	;; XOR @
		lda 	Vars,x
		eor 	Vars+2,x
		sta		Vars,x
		lda 	Vars+1,x
		eor 	Vars+3,x
		sta		Vars+1,x
		jmp 	Sour16Next

; 	00 Miscellaneous
;	01 Load Constant
;	02 Add Constant
; 	03 Add Register
; 	04 Sub Register
; 	05 And Register
; 	06 Or Register
; 	07 Xor Register

;	* Save Byte Indirect
; 	* Load Direct
;	* Store Word Indirect
;	* Load Word Indirect 
;	* Bidirectional shift.
;	*   Misc 
; 	* External Multiply, Divide, Negate.

TestCode:
		.byte 	$12,$09,$47
		.byte 	$13,$FE,$FF
		.byte 	$42

; Expr returns : Reference, Calculated value, Constant (one only), Test Result.
; Code passes base address of registers in A.
